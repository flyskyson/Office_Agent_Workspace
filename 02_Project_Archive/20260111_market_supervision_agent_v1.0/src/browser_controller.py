"""
浏览器控制器模块
复用 Playwright 能力，提供浏览器自动化功能
"""

from playwright.sync_api import sync_playwright, Browser, Page, BrowserContext
from typing import Optional, Dict, Any
import logging
from pathlib import Path


class BrowserController:
    """浏览器控制器类"""

    def __init__(self, headless: bool = False, slow_mo: int = 100):
        """
        初始化浏览器控制器

        Args:
            headless: 是否无头模式
            slow_mo: 操作延迟（毫秒）
        """
        self.logger = logging.getLogger('BrowserController')
        self.headless = headless
        self.slow_mo = slow_mo

        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

    def start(self):
        """启动浏览器"""
        self.logger.info("启动浏览器...")

        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            slow_mo=self.slow_mo
        )

        self.context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )

        self.page = self.context.new_page()
        self.logger.info("浏览器启动成功")

    def close(self):
        """关闭浏览器"""
        if self.page:
            self.page.close()
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

        self.logger.info("浏览器已关闭")

    def navigate(self, url: str, wait_until: str = "load"):
        """
        导航到指定URL

        Args:
            url: 目标URL
            wait_until: 等待条件 (load, domcontentloaded, networkidle)
        """
        self.logger.info(f"导航到: {url}")
        self.page.goto(url, wait_until=wait_until, timeout=60000)

    def fill_form(self, selector: str, value: str):
        """
        填写表单字段

        Args:
            selector: 元素选择器
            value: 填入的值
        """
        self.logger.debug(f"填写表单: {selector} = {value}")
        self.page.fill(selector, value)

    def click(self, selector: str):
        """
        点击元素

        Args:
            selector: 元素选择器
        """
        self.logger.debug(f"点击元素: {selector}")
        self.page.click(selector)

    def select_option(self, selector: str, value: str):
        """
        选择下拉菜单选项

        Args:
            selector: 下拉菜单选择器
            value: 选项值
        """
        self.logger.debug(f"选择选项: {selector} = {value}")
        self.page.select_option(selector, value)

    def wait_for_selector(self, selector: str, timeout: int = 30000):
        """
        等待元素出现

        Args:
            selector: 元素选择器
            timeout: 超时时间（毫秒）
        """
        self.logger.debug(f"等待元素: {selector}")
        self.page.wait_for_selector(selector, timeout=timeout)

    def screenshot(self, path: str, full_page: bool = True):
        """
        截图

        Args:
            path: 保存路径
            full_page: 是否全页截图
        """
        self.logger.info(f"截图保存到: {path}")
        self.page.screenshot(path=path, full_page=full_page)

    def get_text(self, selector: str) -> str:
        """
        获取元素文本

        Args:
            selector: 元素选择器

        Returns:
            str: 元素文本内容
        """
        return self.page.text_content(selector) or ""

    def execute_script(self, script: str) -> Any:
        """
        执行 JavaScript

        Args:
            script: JavaScript 代码

        Returns:
            执行结果
        """
        return self.page.evaluate(script)

    def save_cookies(self, path: str):
        """
        保存 Cookies

        Args:
            path: 保存路径
        """
        import json
        cookies = self.context.cookies()

        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(cookies, f, ensure_ascii=False, indent=2)

        self.logger.info(f"Cookies 已保存到: {path}")

    def load_cookies(self, path: str):
        """
        加载 Cookies

        Args:
            path: Cookies 文件路径
        """
        import json

        if not Path(path).exists():
            self.logger.warning(f"Cookies 文件不存在: {path}")
            return

        with open(path, 'r', encoding='utf-8') as f:
            cookies = json.load(f)

        self.context.add_cookies(cookies)
        self.logger.info(f"Cookies 已加载: {path}")

    def __enter__(self):
        """上下文管理器入口"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()


if __name__ == "__main__":
    # 测试代码
    logging.basicConfig(level=logging.INFO)

    with BrowserController(headless=False) as browser:
        browser.navigate("https://example.com")
        browser.screenshot("test_screenshot.png")
        print("浏览器测试完成")
