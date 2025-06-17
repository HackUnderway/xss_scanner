#!/usr/bin/env python3
import argparse
import asyncio
import os
from urllib.parse import urlparse
from config.banner import show_banner
from config.constants import (
    INFO, WARN, ERROR, SUCCESS, RESET, 
    Fore, Style, WAF_PAYLOAD_DIR
)
from core.scanner import XSSScanner
from core.waf_detector import WAFDetector
from utils.validator import is_valid_url, has_injection_point

class CustomHelpFormatter(argparse.RawTextHelpFormatter):
    def _format_usage(self, usage, actions, groups, prefix):
        return super()._format_usage(usage, actions, groups, prefix)

def get_argument_parser():
    """Configure and return the argument parser with colored help"""
    parser = argparse.ArgumentParser(
        usage="main.py [-h] url [-p PAYLOADS] [-v] [-w WAF]",
        description=f"{SUCCESS}🔎 Advanced XSS Scanner Tool v2.0{Style.RESET_ALL}",
        epilog=f"""{Fore.YELLOW}Example usage:\n{Style.RESET_ALL}
{Fore.GREEN}{Style.BRIGHT}✅ URL MUST CONTAIN INJECTION PARAMETERS:{Style.RESET_ALL}

{Fore.WHITE}Basic GET scan: 
    python main.py "https://portswigger-labs.net/xss/xss.php?x=" 

{Fore.WHITE}Specify WAF type: 
    python main.py "https://portswigger-labs.net/xss/xss.php?x=" -w cloudflare

{Fore.WHITE}Visible browser mode: 
    python main.py "https://portswigger-labs.net/xss/xss.php?x=" -v

{Fore.WHITE}Custom payload file: 
    python main.py "https://portswigger-labs.net/xss/xss.php?x=" -p config/payloads/cloudfront.txt

{Fore.RED}{Style.BRIGHT}❌ Incorrect examples:{Style.RESET_ALL}
    python main.py "https://portswigger-labs.net"
    python main.py "https://portswigger-labs.net/xss/xss.php?x=test"{Style.RESET_ALL}

{Fore.CYAN}Features:{Style.RESET_ALL}
  • GET method support
  • Automatic WAF detection
  • Context-aware payloads
  • WAF-specific bypass techniques
  • Smart payload generation
  • Comprehensive reporting""",
        formatter_class=CustomHelpFormatter,
        add_help=False
    )

    # Help option
    parser.add_argument(
        "-h", "--help",
        action="help",
        default=argparse.SUPPRESS,
        help=f"{Fore.WHITE}Show this help message and exit{Style.RESET_ALL}"
    )

    # Positional argument (url)
    parser.add_argument(
        "target_url",
        help=f"{Fore.WHITE}Target URL with injection point (must contain ?param=){Style.RESET_ALL}"
    )

    # Optional arguments
    parser.add_argument(
        "-p", "--payloads",
        default=None,
        help=f"{Fore.WHITE}Custom payload file to use{Style.RESET_ALL}"
    )

    parser.add_argument(
        "-v", "--visible",
        action="store_false",
        dest="headless",
        help=f"{Fore.WHITE}Run browser in visible mode{Style.RESET_ALL}"
    )

    parser.add_argument(
        "-w", "--waf",
        choices=['akamai', 'cloudflare', 'cloudfront', 'imperva', 'incapsula', 'wordfence', 'auto'],
        help=f"{Fore.WHITE}Specify WAF type or 'auto' for detection{Style.RESET_ALL}"
    )

    parser.add_argument(
        "--no-smart",
        action="store_false",
        dest="smart_payloads",
        default=True,
        help=f"{Fore.WHITE}Disable smart payload generation{Style.RESET_ALL}"
    )

    return parser

async def main():
    show_banner()
    parser = get_argument_parser()
    args = parser.parse_args()

    # Validación temprana de la URL
    if not is_valid_url(args.target_url):
        return

    if not has_injection_point(args.target_url):
        return

    # WAF detection
    waf_type = args.waf
    if waf_type == 'auto' or (args.waf is None and args.payloads is None):
        print(f"{INFO}ℹ️ Detecting WAF...{RESET}")
        detector = WAFDetector()
        waf_type = detector.detect(args.target_url)
        if waf_type:
            print(f"{INFO}ℹ️ Detected WAF: {waf_type}{RESET}")
        else:
            print(f"{INFO}ℹ️ No WAF detected{RESET}")
    
    # Determine payload file
    payload_file = args.payloads
    if waf_type and waf_type != 'auto' and not args.payloads:
        payload_file = os.path.join(WAF_PAYLOAD_DIR, f"{waf_type.lower()}.txt")

    # Initialize scanner
    scanner = XSSScanner(
        target_url=args.target_url,
        payload_file=payload_file,
        waf_type=waf_type,
        headless=args.headless,
        smart_payloads=args.smart_payloads
    )
    
    # Run scan
    await scanner.scan()

if __name__ == "__main__":
    asyncio.run(main())
