<h1 align="center">XSS Scanner Tool 🕵🏽‍♂️</h1>

<p align="center">
  Herramienta avanzada de escaneo XSS (Cross-Site Scripting) para auditorías de seguridad web, con capacidades de evasión de WAF y generación de reportes completos.
</p>

<p align="center">
<img src="assets/xss_scanner.png" title="NmapScan" alt="Xss_Scanner" width="600"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue.svg" alt="Python version">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="LICENCE">
  <img src="https://img.shields.io/badge/Reportes-PDF%20%7C%20JSON%20%7C%20HTML-green.svg" alt="Formatos de reporte">
  <img src="https://img.shields.io/badge/ACTIVE-RECON-orange?logo=security&logoColor=white">
</p>

---

## 🔍 Características principales

- **Detección multifacética**:
  - XSS reflejado y basado en DOM
  - Context-aware payloads (identifica el contexto de inyección)
  - Técnicas avanzadas de evasión de WAFs (Cloudflare, Cloudfront, etc.)

- **Motor inteligente**:
  - Generación dinámica de payloads
  - Detección automática de WAFs
  - Modo headless con Puppeteer/Playwright

- **Reporting profesional**:
  - Reportes en HTML, PDF y JSON
  - Explicación detallada de vulnerabilidades
  - URLs de explotación listas para pruebas.

## 🚀 Casos de uso típicos

1. **Auditorías de seguridad**
```bash
python main.py "https://example.com/search?q=" -w cloudflare
```
2. **Pruebas de penetración**
```bash
python main.py "https://testphp.vulnweb.com/artists.php?artist=" -v
```
3. **Investigación de WAFs:**
```bash
python main.py "https://testphp.vulnweb.com/artists.php?artist=" -v
```

## 📌 Requisitos técnicos

- Python 3.11+

- Navegador Chromium/Chrome instalado

- Dependencias: playwright, argparse, pyfiglet

## ⚠️ Consideraciones éticas

#### Esta herramienta debe usarse únicamente en:

- Sitios propios con permiso explícito

- Entornos de pruebas controlados

- Programas de bug bounty con autorización

- El uso no autorizado en sistemas ajenos es ilegal.

---
## ⚙️ Instalación

Clona el repositorio:

```bash
git clone https://github.com/HackUnderway/xss_scanner.git
```
```bash
cd xss_scanner
```
```bash
pip install -r requirements.txt
```

#### Instalar navegadores (Chromium)
```bash
playwright install chromium
```
#### Verificar instalación
```bash
python -c "from playwright.sync_api import sync_playwright; sync_playwright().start()"
```
#### Ayuda/Guía
```bash
python main.py -h
```
```bash
▐▄• ▄ .▄▄ · .▄▄ · 
 █▌█▌▪▐█ ▀. ▐█ ▀. 
 ·██· ▄▀▀▀█▄▄▀▀▀█▄
▪▐█·█▌▐█▄▪▐█▐█▄▪▐█
•▀▀ ▀▀ ▀▀▀▀  ▀▀▀▀
XSS Scanner Tool v2.0
by @HackUnderway

Features:
• DOM-based XSS detection                                                                                                 
• Reflected XSS detection                                                                                                 
• WAF bypass techniques                                                                                                   
• Smart payload generation                                                                                                
• Comprehensive reporting                                                                                                 

usage: main.py [-h] url [-p PAYLOADS] [-v] [-w WAF]

🔎 Advanced XSS Scanner Tool v2.0

positional arguments:
  target_url            Target URL with injection point (must contain ?param=)

options:
  -h, --help            Show this help message and exit
  -p, --payloads PAYLOADS
                        Custom payload file to use
  -v, --visible         Run browser in visible mode
  -w, --waf {akamai,cloudflare,cloudfront,imperva,incapsula,wordfence,auto}
                        Specify WAF type or 'auto' for detection
  --no-smart            Disable smart payload generation

Example usage:

✅ URL MUST CONTAIN INJECTION PARAMETERS:

Basic GET scan: 
    python main.py "https://portswigger-labs.net/xss/xss.php?x="                                                          

Specify WAF type:                                                                                                         
    python main.py "https://portswigger-labs.net/xss/xss.php?x=" -w cloudflare                                            

Visible browser mode:                                                                                                     
    python main.py "https://portswigger-labs.net/xss/xss.php?x=" -v                                                       

Custom payload file:                                                                                                      
    python main.py "https://portswigger-labs.net/xss/xss.php?x=" -p config/payloads/cloudfront.txt                        

❌ Incorrect examples:                                                                                                    
    python main.py "https://portswigger-labs.net"
    python main.py "https://portswigger-labs.net/xss/xss.php?x=test"

Features:
  • GET method support
  • Automatic WAF detection
  • Context-aware payloads
  • WAF-specific bypass techniques
  • Smart payload generation
  • Comprehensive reporting

```
## 🚀 Uso
##### Escaneo básico con método GET:
python main.py "https://portswigger-labs.net/xss/xss.php?x="

##### Especificar el tipo de WAF (Firewall de Aplicaciones Web):
python main.py "https://portswigger-labs.net/xss/xss.php?x=" -w cloudflare

##### Modo visible del navegador:
python main.py "https://portswigger-labs.net/xss/xss.php?x=" -v

##### Archivo personalizado de payloads:
python main.py "https://portswigger-labs.net/xss/xss.php?x=" -p config/payloads/cloudfront.txt

<p align="center">
  <img src="assets/xss_scanner.png" alt="Xss_Scanner" width="600"/>
  <img src="assets/prueba_xss.png" alt="Prueba_XSS" width="600"/>
  <img src="assets/reporte_html.png" alt="Reporte_Html" width="600"/>
  <img src="assets/reporte_json.png" alt="Reporte_Json" width="600"/>
  <img src="assets/reporte_pdf.png" alt="Reporte_Pdf" width="600"/>
</p>

### Créditos de payloads usados:

https://github.com/gprime31/WAF-bypass-xss-payloads

https://portswigger.net/web-security/cross-site-scripting/cheat-sheet

### Recursos para ver formatos JSON:

https://jsonscope.com/

https://jsoncrack.com/editor

https://2x2xplz.github.io/json_visualizer/default.htm

> **El proyecto está abierto a colaboradores.**

# DISTRIBUCIONES SOPORTADAS
|Distribución | Versión verificada | 	¿Soportado? | 	Estado |
|--------------|--------------------|------|-------|
|Kali Linux| 2026.1=2| si| funcionando   |
|Parrot Security OS| 6.3| si | funcionando   |
|Windows| 11 | si | funcionando   |
|BackBox| 9 | si | funcionando   |
|Arch Linux| 2024.12.01 | si | funcionando   |

# SOPORTE
Preguntas, errores o sugerencias: info@hackunderway.com

# LICENSE
- [x] XSS Scanner tiene licencia.
- [x] Consulta el archivo [LICENSE](https://github.com/HackUnderway/xss_scanner#MIT-1-ov-file) para más información.

# 👨‍💻 Author

* [Victor Bancayan](https://www.offsec.com/bug-bounty-program/) - (**CEO at [Hack Underway](https://hackunderway.com/)**) 

---

<h2 align="center">🕵️‍♂️ OSINT Platform</h2>
<p align="center">
  <a href="https://hackunderway.io/" target="_blank">
    <img src="https://img.shields.io/badge/Try%20Enterprise%20Mode-hackunderway.io-0088CC?style=for-the-badge&logo=internet&logoColor=white" alt="OSINT Platform">
  </a>
</p>
<p align="center">
  <b>Automate OSINT processes</b><br>
  New <b>Enterprise Mode</b> – Maltego-inspired interface with visual graphs and professional workflows.<br>
  <a href="https://hackunderway.io/new-update-to-our-osint-platform-hack-underway/" target="_blank">📢 See what's new</a>
</p>

## 🔗 Links
[![Patreon](https://img.shields.io/badge/patreon-000000?style=for-the-badge&logo=Patreon&logoColor=white)](https://www.patreon.com/c/HackUnderway)
[![Web site](https://img.shields.io/badge/Website-FF7139?style=for-the-badge&logo=firefox&logoColor=white)](https://hackunderway.com)
[![Facebook](https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white)](https://www.facebook.com/HackUnderway)
[![YouTube](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@JeyZetaOficial)
[![Twitter/X](https://img.shields.io/badge/Twitter/X-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/JeyZetaOficial)
[![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://instagram.com/hackunderway)
[![TryHackMe](https://img.shields.io/badge/TryHackMe-212C42?style=for-the-badge&logo=tryhackme&logoColor=white)](https://tryhackme.com/p/JeyZeta)

## ☕️ Support the project

If you like this tool, consider buying me a coffee:

[![Buy Me a Coffee](https://img.shields.io/badge/-Buy%20me%20a%20coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://www.buymeacoffee.com/hackunderway)

## 🌞 Subscriptions

###### Subscribe to: [Jey Zeta](https://www.facebook.com/JeyZetaOficial/subscribe/)

[![Kali Linux](https://img.shields.io/badge/Kali_Linux-557C94?style=for-the-badge&logo=kalilinux&logoColor=white)](https://www.kali.org/)

from <img src="https://i.imgur.com/ngJCbSI.png" title="Perú"> made in <img src="https://i.imgur.com/NNfy2o6.png" title="Python"> with <img src="https://i.imgur.com/S86RzPA.png" title="Love"> by: <font color="red">Victor Bancayan</font>

© 2026
