from colorama import Fore, Style, init

# Initialize colorama for consistent colors across platforms
init()

# ======================
# COLOR CONSTANTS
# ======================
INFO = Fore.CYAN + Style.BRIGHT
WARN = Fore.YELLOW + Style.BRIGHT
ERROR = Fore.RED + Style.BRIGHT
SUCCESS = Fore.GREEN + Style.BRIGHT
RESET = Style.RESET_ALL

# Color shortcuts
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
RED = Fore.RED
CYAN = Fore.CYAN
MAGENTA = Fore.MAGENTA
WHITE = Fore.WHITE
BLUE = Fore.BLUE

# ======================
# HTTP CONFIGURATION
# ======================
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    # Add more modern user agents
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
]

# ======================
# PAYLOAD CONFIGURATION
# ======================
PAYLOAD_DIR = "config/payloads"
WAF_PAYLOAD_DIR = "config/payloads"
DEFAULT_PAYLOADS = {
    'default': f'{PAYLOAD_DIR}/default.txt',
    'akamai': f'{PAYLOAD_DIR}/akamai.txt',
    'cloudfront': f'{PAYLOAD_DIR}/cloudfront.txt',
    'cloudflare': f'{PAYLOAD_DIR}/cloudflare.txt',
    'imperva': f'{PAYLOAD_DIR}/imperva.txt',
    'incapsula': f'{PAYLOAD_DIR}/incapsula.txt',
    'wordfence': f'{PAYLOAD_DIR}/wordfence.txt',
    'sucuri': f'{PAYLOAD_DIR}/sucuri.txt',
    'barracuda': f'{PAYLOAD_DIR}/barracuda.txt'
}

# ======================
# SCANNER CONFIGURATION
# ======================
REQUEST_TIMEOUT = 30000  # 30 seconds in milliseconds
NAVIGATION_TIMEOUT = 60000  # 60 seconds in milliseconds
MAX_PAYLOADS = 1000  # Maximum number of payloads to load
SCAN_TIMEOUT = 30  # Seconds before scan timeout
MAX_REDIRECTS = 5  # Maximum redirects to follow
CONCURRENT_REQUESTS = 10  # Number of concurrent requests

# ======================
# WAF DETECTION CONFIG
# ======================
WAF_SIGNATURES = {
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

WAF_TEST_PAYLOADS = [
    "' OR 1=1--",                    # SQLi test
    "<script>alert(1)</script>",     # Basic XSS
    "../../../etc/passwd",           # Path traversal
    "|cat /etc/passwd",              # Command injection
    "{{7*7}}",                       # SSTI test
    "${jndi:ldap://test}"            # Log4j test
]

# ======================
# REPORTING CONFIG
# ======================
REPORT_DIR = "reports"
REPORT_TEMPLATES = "templates" # = {
#    'HTML': 'templates/report.html',
#    'PDF': 'templates/report.pdf',
#    'JSON': 'templates/report.json'
#}

# ======================
# CONTEXT TYPES FOR SMART PAYLOADS
# ======================
CONTEXT_TYPES = [
    'html',
    'attribute',
    'script',
    'javascript',
    'style',
    'comment',
    'url'
]

# ======================
# ENCODING VARIATIONS
# ======================
ENCODING_TYPES = [
    'url',
    'html',
    'hex',
    'unicode',
    'base64',
    'utf7'
]
