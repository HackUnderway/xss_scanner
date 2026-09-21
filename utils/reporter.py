import json
import os
from datetime import datetime
from urllib.parse import quote, urlparse, parse_qs, urlencode, urlunparse
from fpdf import FPDF
from jinja2 import Environment, FileSystemLoader
from config.constants import (
    INFO, WARN, ERROR, SUCCESS, RESET, 
    Fore, Style, REPORT_DIR
)

class ReportGenerator:
    def __init__(self, target_url, payloads_count, method=None, waf_type=None):
        self.target_url = target_url
        self.payloads_count = payloads_count
        self.method = method
        self.waf_type = waf_type
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.report_base = os.path.join(REPORT_DIR, f"xss_scan_{self.timestamp}")
        
        os.makedirs(REPORT_DIR, exist_ok=True)
        os.makedirs(os.path.join('templates'), exist_ok=True)

    def _prepare_vulnerabilities_data(self, vulnerabilities):
        """Add complete URLs to vulnerabilities data"""
        processed = []
        for vuln in vulnerabilities:
            vuln_data = vuln.copy()
            if self.method == 'GET':
                vuln_data['complete_url'] = self._generate_complete_url(vuln['payload'])
            processed.append(vuln_data)
        return processed

    def _generate_complete_url(self, payload):
        """Generate complete exploit URL"""
        parsed = urlparse(self.target_url)
        query = parse_qs(parsed.query)
        
        if not query:
            return f"{self.target_url}{quote(payload)}"
        
        injected_params = {}
        for param, values in query.items():
            injected_params[param] = [payload]
        
        new_query = urlencode(injected_params, doseq=True)
        return urlunparse(parsed._replace(query=new_query))

    def generate_json(self, vulnerabilities):
        """Generate JSON report"""
        try:
            report_data = {
                "metadata": {
                    "scan_date": datetime.now().isoformat(),
                    "target_url": self.target_url,
                    "method": self.method,
                    "waf_type": self.waf_type,
                    "payloads_tested": self.payloads_count,
                    "vulnerabilities_found": len(vulnerabilities)
                },
                "vulnerabilities": self._prepare_vulnerabilities_data(vulnerabilities)
            }
            
            json_path = f"{self.report_base}.json"
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(report_data, f, ensure_ascii=False, indent=2)
            return json_path
        except Exception as e:
            print(f"{ERROR}🚨 Error generating JSON report: {e}{RESET}")
            return None

    def generate_pdf(self, vulnerabilities):
        """Generate PDF report with clean formatting"""
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", size=12)

            # Título
            pdf.set_font("Helvetica", 'B', 16)
            pdf.cell(0, 10, "XSS Scan Report", 0, 1, 'C')
            pdf.ln(5)

            # Metadatos
            pdf.set_font("Helvetica", '', 12)
            pdf.cell(0, 10, f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1)
            pdf.cell(0, 10, f"Target URL: {self.target_url}", 0, 1)
            pdf.cell(0, 10, f"Method: {self.method}", 0, 1)
            pdf.cell(0, 10, f"WAF: {self.waf_type or 'None'}", 0, 1)
            pdf.cell(0, 10, f"Payloads Tested: {self.payloads_count}", 0, 1)
            pdf.ln(10)

            if vulnerabilities:
                pdf.set_font("Helvetica", 'B', 14)
                pdf.cell(0, 10, "Vulnerabilities Found", 0, 1)
                pdf.set_font("Helvetica", '', 10)

                available_width = pdf.w - pdf.l_margin - pdf.r_margin

                for i, vuln in enumerate(self._prepare_vulnerabilities_data(vulnerabilities), 1):
                    # Salto de página si es necesario
                    if pdf.get_y() > 250:
                        pdf.add_page()
                        pdf.set_font("Helvetica", 'B', 14)
                        pdf.cell(0, 10, "Vulnerabilities Found (continued)", 0, 1)
                        pdf.set_font("Helvetica", '', 10)

                    # Número y tipo
                    pdf.ln(5)
                    pdf.set_font("Helvetica", 'B')
                    pdf.cell(0, 8, f"{i}. {vuln['type']} via {vuln['method']}", 0, 1)
                    pdf.set_font("Helvetica", '')

                    # Exploit URL
                    if 'complete_url' in vuln:
                        pdf.cell(0, 6, "  Exploit URL:", 0, 1)  # etiqueta con sangría
                        pdf.set_x(pdf.l_margin + 4)  # sangría extra para el contenido
                        pdf.multi_cell(available_width - 4, 6, vuln['complete_url'])
                        pdf.set_x(pdf.l_margin)  # resetear a margen izquierdo

                    # Payload (siempre se imprime)
                    pdf.cell(0, 6, "  Payload:", 0, 1)
                    pdf.set_x(pdf.l_margin + 4)
                    payload_text = vuln['payload'] if vuln['payload'] else "(empty payload)"
                    pdf.multi_cell(available_width - 4, 6, payload_text)
                    pdf.set_x(pdf.l_margin)

                    # Context (si existe)
                    if vuln.get('context'):
                        pdf.cell(0, 6, "  Context:", 0, 1)
                        pdf.set_x(pdf.l_margin + 4)
                        pdf.multi_cell(available_width - 4, 6, vuln['context'])
                        pdf.set_x(pdf.l_margin)

                    # Separación entre vulnerabilidades
                    pdf.ln(2)

            else:
                pdf.set_font("Helvetica", 'B', 14)
                pdf.cell(0, 10, "No Vulnerabilities Found", 0, 1)

            # Pie de página
            pdf.set_y(-15)
            pdf.set_font("Helvetica", 'I', 8)
            pdf.cell(0, 10, "Generated by XSS Scanner", 0, 0, 'C')

            pdf_path = f"{self.report_base}.pdf"
            pdf.output(pdf_path)
            return pdf_path
        except Exception as e:
            print(f"{ERROR}🚨 Error generating PDF report: {e}{RESET}")
            return None

    def generate_html(self, vulnerabilities):
        """Generate HTML report using Jinja2 template"""
        try:
        # Define the correct template path
            template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
            env = Environment(loader=FileSystemLoader(template_dir))
            
            template = env.get_template('report.html')
            
            html_content = template.render(
                scan_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                target_url=self.target_url,
                method=self.method,
                waf_type=self.waf_type,
                payloads_count=self.payloads_count,
                vulnerabilities=self._prepare_vulnerabilities_data(vulnerabilities)
            )
            
            html_path = f"{self.report_base}.html"
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            return html_path
        except Exception as e:
            print(f"{ERROR}🚨 Error generating HTML report: {e}{RESET}")
            return None

    def generate_all_reports(self, vulnerabilities):
        """Generate all report formats"""
        reports = []
        
        json_path = self.generate_json(vulnerabilities)
        if json_path:
            reports.append(f"{SUCCESS}✔ JSON report saved to {json_path}{RESET}")
        
        pdf_path = self.generate_pdf(vulnerabilities)
        if pdf_path:
            reports.append(f"{SUCCESS}✔ PDF report generated: {pdf_path}{RESET}")
        
        html_path = self.generate_html(vulnerabilities)
        if html_path:
            reports.append(f"{SUCCESS}✔ HTML report generated: {html_path}{RESET}")
        
        return "\n".join(reports)
