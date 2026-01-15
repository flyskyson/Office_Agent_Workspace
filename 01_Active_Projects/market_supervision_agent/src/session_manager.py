#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
持久化会话管理器

使用Playwright的持久化上下文功能，一次登录，长期有效

使用方法：
1. 第一次运行时，会在浏览器中打开登录页面
2. 手动登录后，会话自动保存
3. 后续运行自动使用保存的会话，无需重复登录

作者: Claude Code
日期: 2026-01-14
"""

import json
import time
from pathlib import Path
from typing import Optional
from loguru import logger

try:
    from playwright.sync_api import sync_playwright, BrowserContext, Page, Browser
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False
    logger.error("Playwright未安装")


class PersistentSessionManager:
    """持久化会话管理器"""

    def __init__(
        self,
        user_data_dir: Optional[Path] = None,
        headless: bool = False,
        slow_mo: int = 500
    ):
        """
        初始化会话管理器

        Args:
            user_data_dir: 用户数据目录（保存会话）
            headless: 是否无头模式
            slow_mo: 操作延迟（毫秒）
        """
        if not HAS_PLAYWRIGHT:
            raise RuntimeError("Playwright未安装")

        if user_data_dir is None:
            user_data_dir = Path("data/browser_profile")

        self.user_data_dir = Path(user_data_dir)
        self.headless = headless
        self.slow_mo = slow_mo

        # 浏览器对象
        self.playwright = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

        logger.info(f"持久化会话管理器初始化")
        logger.info(f"用户数据目录: {self.user_data_dir}")

    def start(self, auto_login: bool = False, login_url: str = "https://zwfw.gxzf.gov.cn/yct/") -> bool:
        """
        启动浏览器并加载会话

        Args:
            auto_login: 是否自动打开登录页
            login_url: 登录页面URL

        Returns:
            是否成功
        """
        try:
            logger.info("启动浏览器...")

            self.playwright = sync_playwright().start()

            # 使用持久化上下文
            self.context = self.playwright.chromium.launch_persistent_context(
                user_data_dir=str(self.user_data_dir),
                headless=self.headless,
                slow_mo=self.slow_mo,
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )

            # 获取或创建页面
            if len(self.context.pages) > 0:
                self.page = self.context.pages[0]
            else:
                self.page = self.context.new_page()

            self.page.set_default_timeout(30000)

            logger.success("浏览器启动成功")

            # 检查是否需要登录
            if auto_login:
                return self._check_and_login(login_url)
            else:
                return self._check_login_status()

        except Exception as e:
            logger.error(f"启动浏览器失败: {e}")
            return False

    def _check_and_login(self, login_url: str) -> bool:
        """
        检查登录状态，如果未登录则打开登录页

        Args:
            login_url: 登录页面URL

        Returns:
            是否已登录
        """
        try:
            logger.info(f"导航到: {login_url}")
            self.page.goto(login_url, wait_until="networkidle")
            time.sleep(2)

            # 检查是否需要登录
            page_text = self.page.text_content("body") or ""

            if "你好！请先登录" in page_text or "立即登录" in page_text:
                logger.warning("检测到未登录状态")
                logger.info("请在浏览器中手动登录")
                logger.info("登录成功后，程序将自动继续...")

                # 等待用户登录
                self._wait_for_login()

                return True
            else:
                logger.success("检测到已登录状态")
                return True

        except Exception as e:
            logger.error(f"检查登录状态失败: {e}")
            return False

    def _check_login_status(self) -> bool:
        """
        检查当前登录状态

        Returns:
            是否已登录
        """
        try:
            if not self.page:
                logger.warning("页面未初始化")
                return False

            # 获取当前页面URL
            current_url = self.page.url
            logger.info(f"当前页面: {current_url}")

            # 检查页面内容
            page_text = self.page.text_content("body") or ""

            if "你好！请先登录" in page_text or "立即登录" in page_text:
                logger.warning("当前未登录")
                return False
            else:
                logger.success("当前已登录")
                return True

        except Exception as e:
            logger.error(f"检查登录状态失败: {e}")
            return False

    def _wait_for_login(self, timeout: int = 300):
        """
        等待用户登录

        Args:
            timeout: 超时时间（秒）
        """
        logger.info(f"等待用户登录（最多{timeout}秒）...")

        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                # 检查登录状态
                page_text = self.page.text_content("body") or ""

                if "你好！请先登录" not in page_text and "立即登录" not in page_text:
                    logger.success("检测到登录成功！")
                    time.sleep(2)
                    return

                time.sleep(2)

            except Exception as e:
                logger.warning(f"检查登录状态时出错: {e}")
                time.sleep(2)

        logger.error(f"等待登录超时（{timeout}秒）")

    def navigate_to(self, url: str, wait_until: str = "networkidle") -> bool:
        """
        导航到指定URL

        Args:
            url: 目标URL
            wait_until: 等待条件

        Returns:
            是否成功
        """
        try:
            logger.info(f"导航到: {url}")
            self.page.goto(url, wait_until=wait_until)
            time.sleep(1)
            return True
        except Exception as e:
            logger.error(f"导航失败: {e}")
            return False

    def click_element(self, selector: str, timeout: int = 5000) -> bool:
        """
        点击元素

        Args:
            selector: CSS选择器
            timeout: 超时时间

        Returns:
            是否成功
        """
        try:
            logger.info(f"点击元素: {selector}")
            self.page.wait_for_selector(selector, timeout=timeout)
            self.page.click(selector)
            time.sleep(1)
            return True
        except Exception as e:
            logger.error(f"点击失败: {selector}, {e}")
            return False

    def fill_text(self, selector: str, text: str, timeout: int = 5000) -> bool:
        """
        填写文本

        Args:
            selector: CSS选择器
            text: 文本内容
            timeout: 超时时间

        Returns:
            是否成功
        """
        try:
            logger.info(f"填写: {selector} = {text}")
            self.page.wait_for_selector(selector, timeout=timeout)
            self.page.fill(selector, text)
            time.sleep(0.5)
            return True
        except Exception as e:
            logger.error(f"填写失败: {selector}, {e}")
            return False

    def take_screenshot(self, filename: str = None, full_page: bool = True) -> str:
        """
        截图

        Args:
            filename: 文件名（可选）
            full_page: 是否截取整页

        Returns:
            截图文件路径
        """
        try:
            if filename is None:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"

            screenshot_dir = Path("data/screenshots")
            screenshot_dir.mkdir(parents=True, exist_ok=True)

            filepath = screenshot_dir / filename
            self.page.screenshot(path=str(filepath), full_page=full_page)

            logger.info(f"截图已保存: {filepath}")
            return str(filepath)

        except Exception as e:
            logger.error(f"截图失败: {e}")
            return ""

    def execute_script(self, script: str):
        """
        执行JavaScript

        Args:
            script: JavaScript代码

        Returns:
            执行结果
        """
        try:
            return self.page.evaluate(script)
        except Exception as e:
            logger.error(f"执行脚本失败: {e}")
            return None

    def get_cookies(self) -> list:
        """
        获取所有Cookie

        Returns:
            Cookie列表
        """
        try:
            cookies = self.context.cookies()
            logger.info(f"获取到 {len(cookies)} 个Cookie")
            return cookies
        except Exception as e:
            logger.error(f"获取Cookie失败: {e}")
            return []

    def save_cookies(self, filepath: str = "data/portal_cookies.json"):
        """
        保存Cookie到文件

        Args:
            filepath: 文件路径

        Returns:
            是否成功
        """
        try:
            cookies = self.get_cookies()

            filepath = Path(filepath)
            filepath.parent.mkdir(parents=True, exist_ok=True)

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(cookies, f, ensure_ascii=False, indent=2)

            logger.success(f"Cookie已保存: {filepath}")
            return True

        except Exception as e:
            logger.error(f"保存Cookie失败: {e}")
            return False

    def close(self):
        """关闭浏览器"""
        if self.context:
            self.context.close()
            logger.info("浏览器已关闭")

        if self.playwright:
            self.playwright.stop()
            logger.info("Playwright已停止")

    def __enter__(self):
        """上下文管理器入口"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()


# ==================== 便捷函数 ====================

def create_session(
    user_data_dir: str = "data/browser_profile",
    headless: bool = False,
    auto_login: bool = False
) -> PersistentSessionManager:
    """
    创建会话

    Args:
        user_data_dir: 用户数据目录
        headless: 是否无头模式
        auto_login: 是否自动登录

    Returns:
        会话管理器实例
    """
    manager = PersistentSessionManager(
        user_data_dir=Path(user_data_dir),
        headless=headless
    )

    manager.start(auto_login=auto_login)

    return manager


if __name__ == "__main__":
    # 测试代码
    logger.info("=" * 60)
    logger.info("持久化会话管理器测试")
    logger.info("=" * 60)

    with PersistentSessionManager() as session:
        # 导航到政务服务网
        session.navigate_to("https://zwfw.gxzf.gov.cn/yct/")

        # 截图
        session.take_screenshot("session_test.png")

        # 保持浏览器打开30秒
        logger.info("浏览器将保持打开30秒...")
        time.sleep(30)
