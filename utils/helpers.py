import os
from datetime import datetime
from config.constants import INFO, RESET

def get_report_filename(base_name="xss_scan"):
    """Generate a consistent filename with timestamp for reports."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    if not os.path.exists('reports'):
        os.makedirs('reports')
    return f"reports/{base_name}_{timestamp}"

def print_progress(current, total, message=""):
    """Display a progress bar in the console."""
    progress = current / total
    bar_length = 40
    filled = int(bar_length * progress)
    bar = '█' * filled + '-' * (bar_length - filled)
    print(f"\r{INFO}⏳ {message} [{bar}] {current}/{total} ({progress:.1%}){RESET}", end="", flush=True)

def clear_line():
    """Clear the current line in the terminal."""
    print("\r" + " " * 100 + "\r", end="")
