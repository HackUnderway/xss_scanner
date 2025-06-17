import requests
import re
from bs4 import BeautifulSoup
from config.constants import INFO, WARN, ERROR, RESET

class WAFDetector:
    def __init__(self):
        self.waf_signatures = {
            'Cloudflare': ['cloudflare', 'cf-ray', '__cfduid', 'cf-bmj'],
            'Akamai': ['akamai', 'x-akamai', 'akamai-transform'],
            'Imperva': ['imperva', 'incapsula', 'x-cdn', 'incap_ses'],
            'AWS WAF': ['aws', 'x-aws-id', 'awselb', 'x-amz-id'],
            'Wordfence': ['wordfence', 'waf', 'wf_', 'wordfence_verifiedhuman'],
            'Sucuri': ['sucuri', 'x-sucuri-id', 'sucuri_cloudproxy'],
            'Barracuda': ['barracuda', 'barra_counter_session', 'barracuda_'],
            'Fortinet': ['fortigate', 'fortiwaf'],
            'F5 BIG-IP': ['bigipserver', 'f5', 'x-wa-info']
        }
        self.blocked_responses = [403, 406, 419, 429]
    
    def detect(self, url):
        """Detect WAF by examining headers and response behavior."""
        try:
            # First request - normal
            response = requests.get(
                url, 
                headers={'User-Agent': 'Mozilla/5.0'},
                allow_redirects=False,
                timeout=10
            )
            
            # Check headers for WAF signatures
            headers = str(response.headers).lower()
            content = response.text.lower()
            
            for waf, signatures in self.waf_signatures.items():
                if any(sig.lower() in headers or sig.lower() in content for sig in signatures):
                    return waf
            
            # Check for blocking behavior
            test_payloads = [
                "' OR 1=1--",
                "<script>alert(1)</script>",
                "../../../etc/passwd",
                "|cat /etc/passwd",
                "{{7*7}}",
                "${jndi:ldap://test}"
            ]
            
            for payload in test_payloads:
                test_url = f"{url}?test={payload}" if '?' in url else f"{url}?x={payload}"
                try:
                    test_response = requests.get(
                        test_url,
                        headers={'User-Agent': 'Mozilla/5.0'},
                        timeout=8
                    )
                    
                    if test_response.status_code in self.blocked_responses:
                        return "Generic WAF (Behavior Detection)"
                    
                    if any(block_msg in test_response.text.lower() 
                           for block_msg in ['blocked', 'forbidden', 'security', 'waf']):
                        return "Generic WAF (Block Message Detection)"
                
                except requests.exceptions.RequestException:
                    continue
            
            # No WAF detected
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"{ERROR}🚨 WAF detection failed: {e}{RESET}")
            return None
        except Exception as e:
            print(f"{ERROR}🚨 Unexpected error during WAF detection: {e}{RESET}")
            return None
