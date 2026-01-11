"""
企业年报表单处理模块
"""

import logging
from typing import Dict, Any
from ..browser_controller import BrowserController


class AnnualReportForm:
    """企业年报表单处理类"""

    def __init__(self, browser: BrowserController, config: Dict[str, Any]):
        """
        初始化年报表单处理器

        Args:
            browser: 浏览器控制器实例
            config: 配置信息（包含URL和选择器）
        """
        self.browser = browser
        self.config = config
        self.logger = logging.getLogger('AnnualReportForm')

    def login(self, username: str, password: str) -> bool:
        """
        登录系统

        Args:
            username: 用户名/统一社会信用代码
            password: 密码

        Returns:
            bool: 登录是否成功
        """
        try:
            # 导航到登录页面
            login_url = self.config.get('urls', {}).get('login')
            self.browser.navigate(login_url)

            # 获取选择器
            selectors = self.config.get('selectors', {}).get('login', {})

            # 填写登录表单
            self.browser.fill_form(selectors.get('username'), username)
            self.browser.fill_form(selectors.get('password'), password)

            # 点击登录按钮
            self.browser.click(selectors.get('submit'))

            # 等待登录成功（检查是否跳转到主页）
            self.browser.wait_for_selector(
                selectors.get('success_indicator'),
                timeout=10000
            )

            self.logger.info("登录成功")
            return True

        except Exception as e:
            self.logger.error(f"登录失败: {str(e)}")
            return False

    def navigate_to_annual_report(self, year: int) -> bool:
        """
        导航到年报填写页面

        Args:
            year: 年报年度

        Returns:
            bool: 导航是否成功
        """
        try:
            # 获取年报页面URL
            annual_report_url = self.config.get('urls', {}).get('annual_report')
            if '{year}' in annual_report_url:
                annual_report_url = annual_report_url.format(year=year)

            self.browser.navigate(annual_report_url)

            self.logger.info(f"已导航到 {year} 年度年报页面")
            return True

        except Exception as e:
            self.logger.error(f"导航失败: {str(e)}")
            return False

    def fill_basic_info(self, company_data: Dict[str, Any]) -> bool:
        """
        填写企业基本信息

        Args:
            company_data: 企业数据

        Returns:
            bool: 填写是否成功
        """
        try:
            selectors = self.config.get('selectors', {}).get('basic_info', {})

            # 企业名称
            if 'company_name' in company_data:
                self.browser.fill_form(
                    selectors.get('company_name'),
                    company_data['company_name']
                )

            # 统一社会信用代码
            if 'credit_code' in company_data:
                self.browser.fill_form(
                    selectors.get('credit_code'),
                    company_data['credit_code']
                )

            # 注册资本
            if 'registered_capital' in company_data:
                self.browser.fill_form(
                    selectors.get('registered_capital'),
                    str(company_data['registered_capital'])
                )

            # 企业类型
            if 'company_type' in company_data:
                self.browser.select_option(
                    selectors.get('company_type'),
                    company_data['company_type']
                )

            # 经营地址
            if 'business_address' in company_data:
                self.browser.fill_form(
                    selectors.get('business_address'),
                    company_data['business_address']
                )

            self.logger.info("企业基本信息填写完成")
            return True

        except Exception as e:
            self.logger.error(f"填写基本信息失败: {str(e)}")
            return False

    def fill_financial_info(self, financial_data: Dict[str, Any]) -> bool:
        """
        填写财务信息

        Args:
            financial_data: 财务数据

        Returns:
            bool: 填写是否成功
        """
        try:
            selectors = self.config.get('selectors', {}).get('financial_info', {})

            # 资产总额
            if 'total_assets' in financial_data:
                self.browser.fill_form(
                    selectors.get('total_assets'),
                    str(financial_data['total_assets'])
                )

            # 负债总额
            if 'total_liabilities' in financial_data:
                self.browser.fill_form(
                    selectors.get('total_liabilities'),
                    str(financial_data['total_liabilities'])
                )

            # 营业总收入
            if 'total_revenue' in financial_data:
                self.browser.fill_form(
                    selectors.get('total_revenue'),
                    str(financial_data['total_revenue'])
                )

            # 净利润
            if 'net_profit' in financial_data:
                self.browser.fill_form(
                    selectors.get('net_profit'),
                    str(financial_data['net_profit'])
                )

            self.logger.info("财务信息填写完成")
            return True

        except Exception as e:
            self.logger.error(f"填写财务信息失败: {str(e)}")
            return False

    def submit(self) -> bool:
        """
        提交年报

        Returns:
            bool: 提交是否成功
        """
        try:
            selectors = self.config.get('selectors', {}).get('submit', {})

            # 点击提交按钮
            self.browser.click(selectors.get('button'))

            # 确认提交（如果有确认对话框）
            if selectors.get('confirm'):
                self.browser.click(selectors.get('confirm'))

            # 等待提交成功提示
            self.browser.wait_for_selector(
                selectors.get('success_message'),
                timeout=15000
            )

            self.logger.info("年报提交成功")
            return True

        except Exception as e:
            self.logger.error(f"提交年报失败: {str(e)}")
            return False

    def process(self, company_data: Dict[str, Any]) -> bool:
        """
        完整处理年报流程

        Args:
            company_data: 企业数据（包含基本信息、财务信息等）

        Returns:
            bool: 处理是否成功
        """
        try:
            # 1. 登录
            if not self.login(
                company_data.get('credit_code'),
                company_data.get('password')
            ):
                return False

            # 2. 导航到年报页面
            if not self.navigate_to_annual_report(company_data.get('year', 2024)):
                return False

            # 3. 填写基本信息
            if not self.fill_basic_info(company_data):
                return False

            # 4. 填写财务信息
            if 'financial_data' in company_data:
                if not self.fill_financial_info(company_data['financial_data']):
                    return False

            # 5. 提交
            if not self.submit():
                return False

            self.logger.info("年报处理完成")
            return True

        except Exception as e:
            self.logger.error(f"年报处理失败: {str(e)}")
            return False
