#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
政务服务网自动化 - 持久化会话版本

使用持久化会话，一次登录，长期有效

功能：
- 自动检测登录状态
- 导航到企业开办页面
- 自动填写表单
- 数据提取

作者: Claude Code
日期: 2026-01-14
"""

import time
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from loguru import logger

try:
    from playwright.sync_api import sync_playwright, Browser, Page, BrowserContext
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

from src.session_manager import PersistentSessionManager


class PersistentPortalAutomation:
    """持久化会话的政务服务网自动化"""

    # 页面URL
    URLS = {
        "home": "https://zwfw.gxzf.gov.cn/yct/",
        "login": "https://zwfw.gxzf.gov.cn/gxzwfw/phaseii/login/tologin.do"
    }

    def __init__(
        self,
        user_data_dir: str = "data/browser_profile",
        headless: bool = False
    ):
        """
        初始化自动化实例

        Args:
            user_data_dir: 用户数据目录
            headless: 是否无头模式
        """
        self.session = PersistentSessionManager(
            user_data_dir=Path(user_data_dir),
            headless=headless
        )

        self.page = None

    def start(self, auto_login: bool = True) -> bool:
        """
        启动会话

        Args:
            auto_login: 是否自动打开登录页

        Returns:
            是否成功
        """
        logger.info("启动政务服务网自动化...")

        success = self.session.start(auto_login=auto_login)

        if success:
            self.page = self.session.page
            logger.success("政务服务网自动化启动成功")

        return success

    def navigate_to_enterprise_setup(self) -> bool:
        """
        导航到企业开办一件事页面

        Returns:
            是否成功
        """
        try:
            logger.info("导航到企业开办一件事...")

            # 先到首页
            self.session.navigate_to(self.URLS["home"])
            time.sleep(2)

            # 查找企业开办链接
            js_code = """
            () => {
                const links = document.querySelectorAll('a');
                for (let link of links) {
                    const text = link.textContent?.trim() || '';
                    if (text.includes('企业开办') && text.includes('一件事')) {
                        return {
                            text: text,
                            href: link.href || '',
                            found: true
                        };
                    }
                }
                return {found: false};
            }
            """

            result = self.page.evaluate(js_code)

            if result.get('found'):
                logger.info(f"找到链接: {result['text']}")

                if result.get('href'):
                    # 直接导航
                    self.session.navigate_to(result['href'])
                else:
                    # 使用JavaScript点击
                    self.page.evaluate("""
                        () => {
                            const links = document.querySelectorAll('a');
                            for (let link of links) {
                                if (link.textContent.includes('企业开办')) {
                                    link.click();
                                    return true;
                                }
                            }
                            return false;
                        }
                    """)

                time.sleep(3)
                self.session.take_screenshot("enterprise_setup_page.png")

                logger.success("已导航到企业开办页面")
                logger.info(f"当前页面: {self.page.url}")
                return True
            else:
                logger.warning("未找到企业开办链接")
                self.session.take_screenshot("no_enterprise_link.png")
                return False

        except Exception as e:
            logger.error(f"导航失败: {e}")
            return False

    def detect_page_elements(self) -> Dict[str, Any]:
        """
        检测页面元素

        Returns:
            页面元素信息
        """
        try:
            js_code = """
            () => {
                const result = {
                    url: window.location.href,
                    title: document.title,
                    inputs: [],
                    buttons: [],
                    links: []
                };

                // 检测输入框
                const inputs = document.querySelectorAll('input[type="text"], input[type="password"], textarea');
                inputs.forEach((input, idx) => {
                    result.inputs.push({
                        index: idx,
                        type: input.type || 'text',
                        name: input.name || '',
                        id: input.id || '',
                        placeholder: input.placeholder || '',
                        className: input.className || ''
                    });
                });

                // 检测按钮
                const buttons = document.querySelectorAll('button, input[type="submit"], input[type="button"]');
                buttons.forEach((button, idx) => {
                    const text = button.textContent?.substring(0, 30) || button.value || '';
                    result.buttons.push({
                        index: idx,
                        text: text.trim(),
                        type: button.type || '',
                        className: button.className || ''
                    });
                });

                // 检测链接
                const links = document.querySelectorAll('a');
                links.forEach((link, idx) => {
                    const text = link.textContent?.trim() || '';
                    if (text && text.length < 50 && idx < 20) {
                        result.links.push({
                            text: text,
                            href: link.href || ''
                        });
                    }
                });

                return result;
            }
            """

            elements = self.page.evaluate(js_code)

            logger.info(f"页面URL: {elements['url']}")
            logger.info(f"页面标题: {elements['title']}")
            logger.info(f"输入框数量: {len(elements['inputs'])}")
            logger.info(f"按钮数量: {len(elements['buttons'])}")
            logger.info(f"链接数量: {len(elements['links'])}")

            # 保存到文件
            output_path = Path("data/page_elements.json")
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(elements, f, ensure_ascii=False, indent=2)

            logger.info(f"页面元素已保存: {output_path}")

            return elements

        except Exception as e:
            logger.error(f"检测页面元素失败: {e}")
            return {}

    def close(self):
        """关闭会话"""
        self.session.close()

    def __enter__(self):
        """上下文管理器入口"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()


# ==================== 测试和使用示例 ====================

def test_persistent_automation():
    """测试持久化自动化"""
    logger.info("=" * 60)
    logger.info("测试政务服务网持久化自动化")
    logger.info("=" * 60)

    with PersistentPortalAutomation() as portal:
        # 导航到企业开办
        portal.navigate_to_enterprise_setup()

        # 检测页面元素
        elements = portal.detect_page_elements()

        # 保持浏览器打开
        logger.info("\n浏览器将保持打开30秒...")
        time.sleep(30)


if __name__ == "__main__":
    import sys
    from loguru import logger as _

    # 配置日志
    logger.remove()
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
        level="INFO"
    )

    test_persistent_automation()
