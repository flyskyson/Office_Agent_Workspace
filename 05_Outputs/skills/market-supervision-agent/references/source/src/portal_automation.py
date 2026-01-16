#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
政务服务网表单自动化 - 广西数字政务一体化平台

https://zwfw.gxzf.gov.cn/yct/

功能：
- 自动登录
- 拟定名称
- 填写经营户信息
- 填写经营范围
- 数据保存到数据库

作者: Claude Code
日期: 2026-01-14
"""

import time
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from loguru import logger

try:
    from playwright.sync_api import sync_playwright, Browser, Page, BrowserContext, TimeoutError as PlaywrightTimeoutError
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False
    logger.warning("Playwright未安装，请运行: pip install playwright && playwright install chromium")

# 导入滑块验证码解决器
try:
    from src.captcha_solver import SliderCaptchaSolver, HybridCaptchaSolver
    HAS_CAPTCHA_SOLVER = True
    logger.info("滑块验证码解决器已加载")
except ImportError:
    HAS_CAPTCHA_SOLVER = False
    logger.warning("滑块验证码解决器未找到，将使用手动处理")


@dataclass
class PortalConfig:
    """政务服务网配置"""
    base_url: str = "https://zwfw.gxzf.gov.cn/yct/"
    login_url: str = "https://zwfw.gxzf.gov.cn/yct/login"

    # 登录凭证
    username: Optional[str] = None
    password: Optional[str] = None

    # 浏览器配置
    headless: bool = False              # 是否无头模式（建议设为False，方便观察）
    slow_mo: int = 500                  # 操作延迟（毫秒）
    timeout: int = 30000                # 默认超时时间

    # Cookie保存路径（保持登录状态）
    cookies_path: str = "data/portal_cookies.json"

    # 截图保存路径
    screenshot_dir: str = "data/screenshots"


class PortalAutomation:
    """政务服务网自动化类"""

    # 选择器配置（根据实际页面调整）
    SELECTORS = {
        'login': {
            'username_input': 'input[type="text"][placeholder*="用户名"], input[name="username"], #username',
            'password_input': 'input[type="password"][placeholder*="密码"], input[name="password"], #password',
            'captcha_input': 'input[placeholder*="验证码"], input[name="captcha"]',
            'captcha_image': 'img[src*="captcha"], img.captcha',
            'login_button': 'button:has-text("登录"), input[type="submit"], .login-btn',
            'login_success_indicator': '.user-info, .avatar, [class*="user"]'
        },
        'registration': {
            'menu_link': 'a:has-text("个体工商户"), a:has-text("设立登记")',
            'name_input': 'input[placeholder*="名称"], input[name="businessName"]',
            'name_check_button': 'button:has-text("查重"), button:has-text("检查")',
            'operator_name_input': 'input[name="operatorName"]',
            'id_card_input': 'input[name="idCard"]',
            'phone_input': 'input[name="phone"]',
            'address_input': 'input[name="address"], textarea[name="address"]',
            'scope_input': 'textarea[name="businessScope"], input[name="businessScope"]',
            'scope_select_button': 'button:has-text("选择"), button:has-text("添加")',
            'save_button': 'button:has-text("保存"), button:has-text("暂存")',
            'submit_button': 'button:has-text("提交"), button:has-text("申请")'
        }
    }

    def __init__(self, config: Optional[PortalConfig] = None):
        """初始化自动化实例

        Args:
            config: 配置对象
        """
        if not HAS_PLAYWRIGHT:
            raise RuntimeError("Playwright未安装，请运行: pip install playwright && playwright install chromium")

        self.config = config or PortalConfig()

        # 创建必要目录
        Path(self.config.cookies_path).parent.mkdir(parents=True, exist_ok=True)
        Path(self.config.screenshot_dir).mkdir(parents=True, exist_ok=True)

        # 浏览器对象
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

        # 验证码解决器
        self.captcha_solver = None

        logger.info("政务服务网自动化初始化完成")

    def start(self):
        """启动浏览器"""
        logger.info("启动浏览器...")

        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=self.config.headless,
            slow_mo=self.config.slow_mo
        )

        self.context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )

        # 尝试加载已保存的cookies
        self._load_cookies()

        self.page = self.context.new_page()
        self.page.set_default_timeout(self.config.timeout)

        # 初始化验证码解决器
        if HAS_CAPTCHA_SOLVER:
            self.captcha_solver = SliderCaptchaSolver(self.page)
            logger.info("验证码解决器已初始化")

        logger.info("浏览器启动成功")

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

        logger.info("浏览器已关闭")

    def _load_cookies(self):
        """加载保存的cookies"""
        cookies_file = Path(self.config.cookies_path)
        if cookies_file.exists():
            try:
                with open(cookies_file, 'r', encoding='utf-8') as f:
                    cookies = json.load(f)
                self.context.add_cookies(cookies)
                logger.info("已加载保存的cookies")
            except Exception as e:
                logger.warning(f"加载cookies失败: {e}")

    def _save_cookies(self):
        """保存cookies"""
        try:
            cookies = self.context.cookies()
            with open(self.config.cookies_path, 'w', encoding='utf-8') as f:
                json.dump(cookies, f, ensure_ascii=False, indent=2)
            logger.info("cookies已保存")
        except Exception as e:
            logger.warning(f"保存cookies失败: {e}")

    def _screenshot(self, name: str):
        """截图"""
        if self.page:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.png"
            filepath = Path(self.config.screenshot_dir) / filename
            self.page.screenshot(path=str(filepath), full_page=True)
            logger.debug(f"截图已保存: {filepath}")
            return str(filepath)

    def _wait_and_click(self, selector: str, timeout: int = 5000) -> bool:
        """等待元素并点击

        Args:
            selector: 选择器
            timeout: 超时时间

        Returns:
            是否成功
        """
        try:
            self.page.wait_for_selector(selector, timeout=timeout)
            self.page.click(selector)
            return True
        except Exception as e:
            logger.warning(f"点击失败: {selector}, {e}")
            return False

    def _wait_and_fill(self, selector: str, value: str, timeout: int = 5000) -> bool:
        """等待元素并填写

        Args:
            selector: 选择器
            value: 填写值
            timeout: 超时时间

        Returns:
            是否成功
        """
        try:
            self.page.wait_for_selector(selector, timeout=timeout)
            self.page.fill(selector, value)
            time.sleep(0.5)  # 等待填写完成
            return True
        except Exception as e:
            logger.warning(f"填写失败: {selector}, {e}")
            return False

    def login(self, username: Optional[str] = None, password: Optional[str] = None) -> bool:
        """登录政务服务网

        Args:
            username: 用户名（可选，默认使用配置中的）
            password: 密码（可选，默认使用配置中的）

        Returns:
            是否登录成功
        """
        username = username or self.config.username
        password = password or self.config.password

        if not username or not password:
            logger.error("用户名或密码未配置")
            return False

        try:
            logger.info(f"开始登录: {username}")

            # 导航到登录页
            self.page.goto(self.config.login_url, wait_until="domcontentloaded")
            self._screenshot("login_page")

            # 检查是否已登录
            if self._check_already_logged_in():
                logger.info("已经登录，跳过登录步骤")
                return True

            # 填写用户名
            selectors = self.SELECTORS['login']
            if not self._wait_and_fill(selectors['username_input'], username):
                logger.error("找不到用户名输入框")
                self._screenshot("login_error_no_username")
                return False

            # 填写密码
            if not self._wait_and_fill(selectors['password_input'], password):
                logger.error("找不到密码输入框")
                self._screenshot("login_error_no_password")
                return False

            self._screenshot("login_filled")

            # 处理滑块验证码（优先自动处理）
            slider_handled = False
            if self.captcha_solver:
                logger.info("尝试自动解决滑块验证码...")
                slider_handled = self.captcha_solver.detect_and_solve_slider(timeout=5000)

            # 如果自动处理失败，尝试手动处理
            if not slider_handled:
                if self.page.locator(selectors['captcha_input']).count() > 0:
                    logger.warning("检测到验证码，需要手动输入")
                    self._screenshot("login_captcha")
                    input("请手动输入验证码并按回车继续...")

            # 点击登录按钮
            if not self._wait_and_click(selectors['login_button'], timeout=10000):
                logger.error("找不到登录按钮")
                self._screenshot("login_error_no_button")
                return False

            # 等待登录完成
            time.sleep(3)

            # 检查登录是否成功
            if self._check_login_success():
                logger.info("登录成功")
                self._save_cookies()
                self._screenshot("login_success")
                return True
            else:
                logger.error("登录失败")
                self._screenshot("login_failed")
                return False

        except Exception as e:
            logger.error(f"登录异常: {e}")
            self._screenshot("login_error")
            return False

    def _check_already_logged_in(self) -> bool:
        """检查是否已登录"""
        selectors = self.SELECTORS['login']['login_success_indicator'].split(', ')
        for selector in selectors:
            try:
                if self.page.locator(selector).count() > 0:
                    return True
            except:
                continue
        return False

    def _check_login_success(self) -> bool:
        """检查登录是否成功"""
        return self._check_already_logged_in()

    def navigate_to_registration(self) -> bool:
        """导航到设立登记页面

        Returns:
            是否成功
        """
        try:
            logger.info("导航到设立登记页面")

            # 导航到首页
            self.page.goto(self.config.base_url, wait_until="domcontentloaded")
            time.sleep(2)

            # 查找并点击菜单
            selectors = self.SELECTORS['registration']
            menu_selectors = selectors['menu_link'].split(', ')

            for selector in menu_selectors:
                try:
                    if self.page.locator(selector).count() > 0:
                        self.page.click(selector)
                        time.sleep(2)
                        self._screenshot("registration_page")
                        logger.info("已导航到设立登记页面")
                        return True
                except:
                    continue

            logger.warning("未找到设立登记菜单，可能已在页面或需要手动导航")
            self._screenshot("navigation_error")
            return False

        except Exception as e:
            logger.error(f"导航失败: {e}")
            return False

    def fill_business_name(self, business_name: str, check_duplicate: bool = True) -> bool:
        """拟定名称

        Args:
            business_name: 拟定的个体工商户名称
            check_duplicate: 是否查重

        Returns:
            是否成功
        """
        try:
            logger.info(f"拟定名称: {business_name}")

            selectors = self.SELECTORS['registration']

            # 填写名称
            if not self._wait_and_fill(selectors['name_input'], business_name):
                logger.error("找不到名称输入框")
                return False

            time.sleep(1)

            # 查重（如果需要）
            if check_duplicate and self.page.locator(selectors['name_check_button']).count() > 0:
                logger.info("执行名称查重")
                self._wait_and_click(selectors['name_check_button'])
                time.sleep(3)  # 等待查重结果

                # 这里可以添加查重结果的处理逻辑
                # 例如检查是否有提示名称可用

            self._screenshot("name_filled")
            logger.info("名称拟定完成")
            return True

        except Exception as e:
            logger.error(f"拟定名称失败: {e}")
            return False

    def fill_operator_info(self, operator_data: Dict[str, Any]) -> bool:
        """填写经营户信息

        Args:
            operator_data: 经营户数据字典

        Returns:
            是否成功
        """
        try:
            logger.info("填写经营户信息")

            selectors = self.SELECTORS['registration']

            # 字段映射
            field_mapping = {
                'operator_name': selectors['operator_name_input'],
                'id_card': selectors['id_card_input'],
                'phone': selectors['phone_input'],
                'address': selectors['address_input']
            }

            filled_count = 0
            for field, selector in field_mapping.items():
                value = operator_data.get(field)
                if value:
                    # 尝试多个选择器
                    for sel in selector.split(', '):
                        if self._wait_and_fill(sel, str(value), timeout=3000):
                            filled_count += 1
                            logger.debug(f"填写: {field} = {value}")
                            break
                    time.sleep(0.5)

            self._screenshot("operator_info_filled")
            logger.info(f"经营户信息填写完成: {filled_count} 个字段")
            return filled_count > 0

        except Exception as e:
            logger.error(f"填写经营户信息失败: {e}")
            return False

    def fill_business_scope(self, business_scope: str) -> bool:
        """填写经营范围

        Args:
            business_scope: 经营范围文本

        Returns:
            是否成功
        """
        try:
            logger.info(f"填写经营范围: {business_scope}")

            selectors = self.SELECTORS['registration']

            # 检查是否有选择按钮
            if self.page.locator(selectors['scope_select_button']).count() > 0:
                # 使用选择器
                logger.info("使用经营范围选择器")
                self._wait_and_click(selectors['scope_select_button'])
                time.sleep(2)

                # 这里可能需要更复杂的逻辑来处理弹出的选择界面
                # 例如点击树形结构的选项、搜索等

                # 暂时截图，提示用户手动操作
                self._screenshot("scope_selector_opened")
                logger.warning("经营范围选择器已打开，可能需要手动操作")
                input("请手动选择经营范围后按回车继续...")

            else:
                # 直接填写
                if not self._wait_and_fill(selectors['scope_input'], business_scope):
                    logger.error("找不到经营范围输入框")
                    return False

            self._screenshot("scope_filled")
            logger.info("经营范围填写完成")
            return True

        except Exception as e:
            logger.error(f"填写经营范围失败: {e}")
            return False

    def save_form(self) -> bool:
        """保存表单

        Returns:
            是否成功
        """
        try:
            logger.info("保存表单")

            selectors = self.SELECTORS['registration']
            save_selectors = selectors['save_button'].split(', ')

            for selector in save_selectors:
                if self.page.locator(selector).count() > 0:
                    self._wait_and_click(selector)
                    time.sleep(2)
                    self._screenshot("form_saved")
                    logger.info("表单保存成功")
                    return True

            logger.warning("未找到保存按钮")
            return False

        except Exception as e:
            logger.error(f"保存表单失败: {e}")
            return False

    def extract_form_data(self) -> Dict[str, Any]:
        """提取表单中已填写的数据

        Returns:
            提取的数据字典
        """
        try:
            logger.info("提取表单数据")

            selectors = self.SELECTORS['registration']

            data = {}

            # 提取各字段值
            fields_to_extract = {
                'business_name': selectors['name_input'],
                'operator_name': selectors['operator_name_input'],
                'id_card': selectors['id_card_input'],
                'phone': selectors['phone_input'],
                'address': selectors['address_input'],
                'business_scope': selectors['scope_input']
            }

            for field, selector in fields_to_extract.items():
                for sel in selector.split(', '):
                    try:
                        elements = self.page.locator(sel)
                        if elements.count() > 0:
                            # 尝试获取input值
                            tag_name = elements.evaluate('el => el.tagName.toLowerCase()')
                            if tag_name == 'input' or tag_name == 'textarea':
                                value = elements.input_value()
                            else:
                                value = elements.text_content()

                            if value:
                                data[field] = value.strip()
                                logger.debug(f"提取: {field} = {value}")
                                break
                    except:
                        continue

            logger.info(f"提取到 {len(data)} 个字段")
            self._screenshot("data_extracted")
            return data

        except Exception as e:
            logger.error(f"提取数据失败: {e}")
            return {}

    def process_registration(
        self,
        business_name: str,
        operator_data: Dict[str, Any],
        business_scope: str,
        auto_submit: bool = False
    ) -> Dict[str, Any]:
        """完整处理设立登记流程

        Args:
            business_name: 个体工商户名称
            operator_data: 经营户数据
            business_scope: 经营范围
            auto_submit: 是否自动提交（建议False，先保存）

        Returns:
            处理结果
        """
        result = {
            'success': False,
            'business_name': business_name,
            'extracted_data': {},
            'screenshots': [],
            'errors': []
        }

        try:
            # 1. 登录
            if not self.login():
                result['errors'].append('登录失败')
                return result

            # 2. 导航到设立登记页面
            if not self.navigate_to_registration():
                result['errors'].append('导航失败')
                return result

            # 3. 拟定名称
            if not self.fill_business_name(business_name):
                result['errors'].append('拟定名称失败')
                return result

            # 4. 填写经营户信息
            if not self.fill_operator_info(operator_data):
                result['warnings'].append('部分经营户信息填写失败')

            # 5. 填写经营范围
            if not self.fill_business_scope(business_scope):
                result['warnings'].append('经营范围填写可能不完整')

            # 6. 保存表单
            if not self.save_form():
                result['warnings'].append('保存表单可能失败')

            # 7. 提取填写的数据
            extracted = self.extract_form_data()
            result['extracted_data'] = extracted

            # 8. 自动提交（可选）
            if auto_submit:
                logger.warning("自动提交功能已禁用，请手动检查后提交")
                input("请检查表单内容，确认无误后手动提交，完成后按回车...")

            # 9. 截图保存
            final_screenshot = self._screenshot("final")
            result['screenshots'].append(final_screenshot)

            result['success'] = True
            logger.info("设立登记流程处理完成")

        except Exception as e:
            error_msg = f"处理异常: {str(e)}"
            result['errors'].append(error_msg)
            logger.error(error_msg)

        return result

    def __enter__(self):
        """上下文管理器入口"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()


# ============ 便捷函数 ============

def quick_process(
    business_name: str,
    operator_data: Dict[str, Any],
    business_scope: str,
    username: str,
    password: str
) -> Dict[str, Any]:
    """快速处理设立登记

    Args:
        business_name: 个体工商户名称
        operator_data: 经营户数据
        business_scope: 经营范围
        username: 政务服务网用户名
        password: 政务服务网密码

    Returns:
        处理结果
    """
    config = PortalConfig(username=username, password=password, headless=False)

    with PortalAutomation(config) as portal:
        result = portal.process_registration(
            business_name=business_name,
            operator_data=operator_data,
            business_scope=business_scope,
            auto_submit=False
        )

    return result
