import asyncio
import os
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode, parse_qsl, quote
from config.constants import (
    INFO, WARN, ERROR, SUCCESS, RESET, 
    Fore, Style, NAVIGATION_TIMEOUT
)
from core.payloads import PayloadManager
from core.browser import BrowserManager
from core.detection import XSSDetector
from utils.validator import is_valid_url, has_injection_point
from utils.reporter import ReportGenerator
from utils.helpers import print_progress, clear_line

class XSSScanner:
    def __init__(
        self, 
        target_url, 
        payload_file=None, 
        waf_type=None,
        method='GET',  # Ahora siempre será GET
        headless=True,
        smart_payloads=True
    ):
        self.original_url = target_url
        self.target_url = target_url
        self.method = 'GET'  # Forzado a GET
        self.payload_manager = PayloadManager(
            payload_file=payload_file,
            waf_type=waf_type,
            context_aware=smart_payloads
        )
        self.headless = headless
        self.smart_payloads = smart_payloads
        self.found_vulnerabilities = []
        self.waf_type = waf_type
    
    async def scan(self):
        """Main scanning method (solo GET)"""
        if not is_valid_url(self.target_url):
            print(f"{ERROR}🚨 Invalid URL provided{RESET}")
            return False
        
        if not has_injection_point(self.target_url):
            print(f"{WARN}⚠️ No injection point found in URL (add '?param=' for GET){RESET}")
            return False
        
        payloads = await self.payload_manager.load_payloads()
        if not payloads:
            return False
        
        browser_manager = BrowserManager()
        try:
            page = await browser_manager.setup(headless=self.headless)
            detector = XSSDetector(page)
            await detector.setup_detection()
            
            print(f"\n{INFO}🔍 Starting GET scan on: {self.original_url}{RESET}")
            print(f"{WARN}• Payloads loaded: {len(payloads)}")
            print(f"• Headless mode: {'on' if self.headless else 'off'}")
            print(f"• Smart payloads: {'enabled' if self.smart_payloads else 'disabled'}")
            if self.waf_type:
                print(f"• WAF bypass: {self.waf_type}")
            print(RESET)
            
            total_payloads = len(payloads)
            for index, payload in enumerate(payloads, 1):
                print_progress(index, total_payloads, "Testing payloads")
                
                test_url = self._prepare_get_url(payload)
                detection_results = await self._test_get_payload(page, detector, test_url, payload)
                
                if any([detection_results['dialog'], 
                       detection_results['dom_injection'], 
                       detection_results['script_execution']]):
                    self._log_vulnerability(
                        test_url,
                        payload, 
                        detection_results,
                        'GET'  # Método fijo
                    )
            
            clear_line()
            await self._generate_reports(len(payloads))
            return True
        
        except Exception as e:
            print(f"\n{ERROR}🚨 Critical error during scanning: {e}{RESET}")
            return False
        finally:
            await browser_manager.close()
    
    def _prepare_get_url(self, payload):
        """Prepare test URL with injected payload (único método necesario ahora)"""
        parsed = urlparse(self.target_url)
        query = parse_qs(parsed.query)
        
        if not query:
            return f"{self.target_url}{self.payload_manager.get_encoded_payload(payload)}"
        
        injected_params = {}
        for param, values in query.items():
            injected_params[param] = [self.payload_manager.get_encoded_payload(payload)]
        
        new_query = urlencode(injected_params, doseq=True)
        return urlunparse(parsed._replace(query=new_query))
    
    async def _test_get_payload(self, page, detector, test_url, payload):
        """Test a single payload with GET (único método de prueba ahora)"""
        try:
            await page.goto(test_url, wait_until="networkidle", timeout=NAVIGATION_TIMEOUT)
            await asyncio.sleep(2)
            return await detector.detect_xss(payload)
        except Exception as e:
            print(f"\n{WARN}⚠️ Error testing payload: {payload[:50]}...{RESET}")
            print(f"{ERROR}• Details: {e}{RESET}")
            return {'dialog': False, 'dom_injection': False, 'script_execution': False}
    
    def _log_vulnerability(self, url, payload, detection_results, method):
        """Log a found vulnerability (method siempre será GET ahora)"""
        vuln_type = "Dialog" if detection_results['dialog'] else \
                   "DOM Injection" if detection_results['dom_injection'] else \
                   "Script Execution"
        
        complete_url = self._generate_complete_url(payload)

        vulnerability = {
            "url": url,
            "payload": payload,
            "complete_url": complete_url,
            "type": vuln_type,
            "method": 'GET',  # Fijo
            "context": detection_results.get('context'),
            "message": detection_results.get('message'),
            "waf": self.waf_type
        }
        
        clear_line()
        print(f"{SUCCESS}🎯 [{vuln_type}] XSS vulnerability found!")
        print(f"{WARN}• Method: {Style.BRIGHT}{Fore.WHITE}GET")
        print(f"• Exploit URL: {Style.BRIGHT}{Fore.WHITE}{complete_url}")
        print(f"• Payload: {Style.BRIGHT}{Fore.WHITE}{payload}")
        
        if vulnerability['message']:
            print(f"• Message: {Style.BRIGHT}{Fore.WHITE}{vulnerability['message']}")
        if vulnerability['context']:
            print(f"• Context: {Style.BRIGHT}{Fore.WHITE}{vulnerability['context']}")
        if self.waf_type:
            print(f"• WAF Bypass: {Style.BRIGHT}{Fore.WHITE}{self.waf_type}")
        
        print(RESET)
        self.found_vulnerabilities.append(vulnerability)
    
    def _generate_complete_url(self, payload):
        """Generate complete exploit URL (solo para GET)"""
        parsed = urlparse(self.original_url)
        query = parse_qs(parsed.query)
        
        if not query:
            return f"{self.original_url}{quote(payload)}"
        
        injected_params = {}
        for param, values in query.items():
            injected_params[param] = [payload]
        
        new_query = urlencode(injected_params, doseq=True)
        return urlunparse(parsed._replace(query=new_query))
    
    async def _generate_reports(self, payloads_count):
        """Generate all report formats (siempre con método GET)"""
        reporter = ReportGenerator(
            self.original_url, 
            payloads_count,
            method='GET',  # Fijo
            waf_type=self.waf_type
        )
        
        if self.found_vulnerabilities:
            print(f"\n{INFO}🔎 Summary of vulnerabilities found:{RESET}")
            for i, vuln in enumerate(self.found_vulnerabilities, 1):
                print(f"{WARN}{i}. {vuln['type']} via GET")
                print(f"   • Exploit URL: {vuln['complete_url']}")
                print(f"   • Payload: {vuln['payload']}")
                if vuln.get('context'):
                    print(f"   • Context: {vuln['context']}")
                if vuln.get('waf'):
                    print(f"   • WAF Bypass: {vuln['waf']}")
        
        report_results = reporter.generate_all_reports(self.found_vulnerabilities)
        print(f"\n{report_results}")
