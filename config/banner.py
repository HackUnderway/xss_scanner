from colorama import Fore, Style, init

init(autoreset=True)

def show_banner():
    """Display the tool banner with enhanced colors"""
    banner = f"""
{Fore.GREEN}
▐▄• ▄ .▄▄ · .▄▄ · 
 █▌█▌▪▐█ ▀. ▐█ ▀. 
 ·██· ▄▀▀▀█▄▄▀▀▀█▄
▪▐█·█▌▐█▄▪▐█▐█▄▪▐█
•▀▀ ▀▀ ▀▀▀▀  ▀▀▀▀
{Fore.WHITE}{Style.BRIGHT}XSS Scanner Tool {Fore.YELLOW}v2.0{Style.RESET_ALL}
{Fore.CYAN}by @HackUnderway{Style.RESET_ALL}

{Fore.MAGENTA}{Style.BRIGHT}Features:
{Fore.WHITE}• DOM-based XSS detection
{Fore.WHITE}• Reflected XSS detection
{Fore.WHITE}• WAF bypass techniques
{Fore.WHITE}• Smart payload generation
{Fore.WHITE}• Comprehensive reporting{Style.RESET_ALL}
"""
    print(banner)
