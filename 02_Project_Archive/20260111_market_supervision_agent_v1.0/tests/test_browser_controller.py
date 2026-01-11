"""
浏览器控制器测试
"""

import pytest
import sys
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from browser_controller import BrowserController


def test_browser_start_close():
    """测试浏览器启动和关闭"""
    browser = BrowserController(headless=True)
    browser.start()

    assert browser.browser is not None
    assert browser.page is not None

    browser.close()


def test_browser_navigation():
    """测试浏览器导航"""
    browser = BrowserController(headless=True)
    browser.start()

    browser.navigate("https://example.com")
    title = browser.page.title()

    assert "Example" in title

    browser.close()


def test_context_manager():
    """测试上下文管理器"""
    with BrowserController(headless=True) as browser:
        browser.navigate("https://example.com")
        title = browser.page.title()
        assert title is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
