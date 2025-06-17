import pytest
from unittest.mock import AsyncMock, patch
from core.scanner import XSSScanner
from utils.validator import is_valid_url

class TestXSSScanner:
    @pytest.mark.asyncio
    async def test_valid_url_detection(self):
        """Test that URL validation works correctly"""
        assert is_valid_url("http://example.com") is True
        assert is_valid_url("https://example.com/path?q=test") is True
        assert is_valid_url("ftp://example.com") is False
        assert is_valid_url("not-a-url") is False

    @pytest.mark.asyncio
    async def test_scan_with_mocks(self):
        """Test scanner with mocked dependencies"""
        with patch('core.browser.BrowserManager') as mock_browser, \
             patch('core.payloads.PayloadManager.load_payloads') as mock_load:
            
            # Configure mocks
            mock_load.return_value = ['test-payload']
            mock_browser.return_value.setup = AsyncMock()
            mock_browser.return_value.close = AsyncMock()
            
            # Create and run scanner
            scanner = XSSScanner("http://test.com/?q=")
            await scanner.scan()
            
            # Verify mocks were called
            mock_load.assert_called_once()
            mock_browser.return_value.setup.assert_called_once()
