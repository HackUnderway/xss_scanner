from urllib.parse import urlparse, parse_qs
from config.constants import INFO, WARN, ERROR, SUCCESS, RESET, Fore, Style

def is_valid_url(url):
    """Check if the URL is valid and uses HTTP/HTTPS"""
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            print(f"{ERROR}🚨 URL must include scheme (http:// or https://) and domain{RESET}")
            return False
        if result.scheme not in ('http', 'https'):
            print(f"{ERROR}🚨 Only http:// and https:// URLs are supported{RESET}")
            return False
        return True
    except Exception as e:
        print(f"{ERROR}🚨 Invalid URL format: {e}{RESET}")
        return False

def has_injection_point(url):
    """Check if URL has a query parameter suitable for injection"""
    try:
        parsed = urlparse(url)
        if not parsed.query:
            print(f"\n{WARN}⚠️ Error: URL must contain query parameters (e.g., '?param='){RESET}")
            print(f"{INFO}Correct example: {Fore.CYAN}https://portswigger-labs.net/xss/xss.php?x={RESET}")
            print(f"{ERROR}Incorrect example: {Fore.RED}https://portswigger-labs.net{RESET}")
            print(f"{ERROR}Incorrect example: {Fore.RED}https://portswigger-labs.net/xss/xss.php?x=test{RESET}")
            return False
        
        params = parse_qs(parsed.query, keep_blank_values=True)
        for param, values in params.items():
            if not values or values[0] == '':
                return True
        
        print(f"\n{WARN}⚠️ Error: All parameters have fixed values{RESET}")
        print(f"{INFO}Suggestion: Add an empty parameter (e.g., '?param='){RESET}")
        return False
        
    except Exception as e:
        print(f"{ERROR}🚨 Error validating URL: {e}{RESET}")
        return False
