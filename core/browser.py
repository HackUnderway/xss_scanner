from playwright.async_api import async_playwright
from config.constants import USER_AGENTS, REQUEST_TIMEOUT, NAVIGATION_TIMEOUT
import random
import asyncio

class BrowserManager:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
    
    async def setup(self, headless=True):
        """Initialize browser context with random user agent."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=headless,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--disable-gpu'
            ]
        )
        
        user_agent = random.choice(USER_AGENTS)
        self.context = await self.browser.new_context(
            user_agent=user_agent,
            ignore_https_errors=True,
            java_script_enabled=True,
            viewport={'width': 1920, 'height': 1080}
        )
        
        # Set timeouts
        self.context.set_default_timeout(REQUEST_TIMEOUT)
        self.context.set_default_navigation_timeout(NAVIGATION_TIMEOUT)
        
        self.page = await self.context.new_page()
        return self.page
    
    async def close(self):
        """Clean up browser resources."""
        try:
            if hasattr(self, 'page') and self.page:
                await self.page.close()
            if hasattr(self, 'context') and self.context:
                await self.context.close()
            if hasattr(self, 'browser') and self.browser:
                await self.browser.close()
            if hasattr(self, 'playwright') and self.playwright:
                await self.playwright.stop()
        except Exception as e:
            print(f"Error closing browser: {e}")
    
    async def navigate(self, url):
        """Navigate to URL and return page content."""
        try:
            await self.page.goto(url, wait_until="networkidle")
            await self.page.wait_for_load_state("domcontentloaded")
            return await self.page.content()
        except Exception as e:
            print(f"Navigation error: {e}")
            return None
