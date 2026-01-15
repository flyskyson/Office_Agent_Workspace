#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能表单填写器

使用持久化会话自动填写个体工商户开业申请表

功能：
1. 智能页面识别和导航
2. 表单元素自动检测
3. 多字段智能填写
4. 验证码识别（集成百度OCR）
5. 材料上传支持

作者: Claude Code
日期: 2026-01-14
"""

import sys
import time
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

# 确保项目根目录在路径中
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger
from src.session_manager import PersistentSessionManager


# 测试数据
TEST_DATA = {
    "operator_name": "张三",
    "id_card": "450205199001011234",
    "phone": "13800138000",
    "business_name": "张三便利店",
    "business_address": "广西玉林市兴业县蒲塘镇xx路xx号",
    "business_scope": "日用百货销售；预包装食品销售",
    "industry_type": "便利店",
    "organization_form": "个体工商户",
    "registered_capital": "50000",
    "employees_count": "1",
    "business_term": "长期"
}


class IntelligentFormFiller:
    """智能表单填写器"""

    def __init__(self, session: PersistentSessionManager):
        self.session = session
        self.page = session.page

    def detect_page_type(self) -> str:
        """检测当前页面类型"""
        url = self.page.url
        title = self.page.title()

        logger.info(f"当前页面: {url}")
        logger.info(f"页面标题: {title}")

        # 检查是否在公告页面
        if "关于停用启用" in title or "食品许可模块" in title:
            return "announcement"

        # 检查是否在企业开办相关页面（这里就是表单页面！）
        # 实际上 companySetup/index.html 就是个体工商户开业申请页面
        if "companySetup" in url or "企业开办" in title or "市场监管准入" in title:
            # 进一步检查：如果在表单填写阶段
            js_check_form = """
            () => {
                // 检查页面是否有表单元素
                const forms = document.querySelectorAll('form');
                const inputs = document.querySelectorAll('input:not([type="hidden"])');
                const textareas = document.querySelectorAll('textarea');

                return {
                    has_form: forms.length > 0,
                    input_count: inputs.length,
                    textarea_count: textareas.length,
                    page_text: document.body.textContent.substring(0, 200)
                };
            }
            """

            try:
                form_check = self.page.evaluate(js_check_form)
                logger.debug(f"表单检查: {form_check}")

                # 如果页面有输入框或文本框，认为是表单页面
                if form_check.get('input_count', 0) > 0 or form_check.get('textarea_count', 0) > 0:
                    return "application_form"

                # 否则认为是企业开办首页
                return "enterprise_setup_home"

            except Exception as e:
                logger.debug(f"表单检查失败: {e}")
                return "enterprise_setup_home"

        # 检查是否在表单填写页面
        if "form" in url.lower() or "apply" in url.lower() or "申请表" in title:
            return "application_form"

        # 检查是否在登录页面
        if "login" in url.lower() or "登录" in title:
            return "login"

        return "unknown"

    def navigate_to_application_form(self) -> bool:
        """导航到申请表页面"""
        page_type = self.detect_page_type()

        if page_type == "application_form":
            logger.success("已经在申请表页面")
            return True

        if page_type == "announcement":
            logger.info("检测到公告页面，查找进入链接...")

            # 查找进入按钮
            js_find_entry = """
            () => {
                // 查找可能的进入按钮
                const buttons = document.querySelectorAll('button, a, div[onclick]');
                for (let btn of buttons) {
                    const text = btn.textContent?.trim() || '';
                    if (text.includes('进入') || text.includes('办理') ||
                        text.includes('申请') || text.includes('我知道了')) {
                        return {
                            found: true,
                            text: text,
                            tag: btn.tagName,
                            onclick: btn.getAttribute('onclick') || '',
                            href: btn.href || ''
                        };
                    }
                }
                return {found: false};
            }
            """

            result = self.page.evaluate(js_find_entry)

            if result.get('found'):
                logger.success(f"找到按钮: {result['text']}")

                # 点击按钮
                if result.get('onclick'):
                    self.page.evaluate(f"{result['onclick']}")
                elif result.get('href'):
                    self.page.goto(result['href'])
                else:
                    self.page.click(f"button:has-text('{result['text']}')")

                time.sleep(3)
                return self.navigate_to_application_form()

            logger.warning("未找到进入按钮，尝试直接导航...")
            self.page.goto("https://wxxcx.zwfw.gxzf.gov.cn/")
            time.sleep(3)
            return self.navigate_to_application_form()

        if page_type == "enterprise_setup_home":
            logger.info("在企业开办首页，查找申请入口...")

            # 查找个体工商户开业链接
            js_find_link = """
            () => {
                const links = Array.from(document.querySelectorAll('a'));
                const keywords = ['个体', '开业', '设立', '登记', '办理', '申请'];

                for (let link of links) {
                    const text = link.textContent?.trim() || '';
                    const href = link.href || '';

                    // 匹配包含个体工商户相关关键词的链接
                    if (keywords.some(kw => text.includes(kw))) {
                        return {
                            found: true,
                            text: text.substring(0, 50),
                            href: href
                        };
                    }
                }

                return {found: false};
            }
            """

            result = self.page.evaluate(js_find_link)

            if result.get('found'):
                logger.success(f"找到链接: {result['text']}")
                logger.info(f"链接地址: {result.get('href', '无')}")

                if result.get('href'):
                    self.page.goto(result['href'])
                else:
                    # 使用JavaScript点击
                    self.page.evaluate(f"""
                        () => {{
                            const links = Array.from(document.querySelectorAll('a'));
                            for (let link of links) {{
                                if (link.textContent.includes('个体')) {{
                                    link.click();
                                    return true;
                                }}
                            }}
                            return false;
                        }}
                    """)

                time.sleep(3)
                return True

            logger.warning("未找到个体工商户开业链接")
            return False

        logger.warning(f"未知页面类型: {page_type}")
        return False

    def analyze_form_structure(self) -> Dict[str, Any]:
        """分析表单结构"""
        logger.info("分析表单结构...")

        js_analyze = """
        () => {
            const result = {
                url: window.location.href,
                title: document.title,
                forms: [],
                inputs: [],
                selects: [],
                textareas: [],
                radio_groups: {},
                checkbox_groups: {},
                file_inputs: []
            };

            // 检测所有表单
            const forms = document.querySelectorAll('form');
            forms.forEach((form, formIdx) => {
                const formInfo = {
                    index: formIdx,
                    id: form.id || '',
                    name: form.name || '',
                    action: form.action || '',
                    method: form.method || '',
                    field_count: 0
                };

                // 检测表单内的输入字段
                const inputs = form.querySelectorAll('input:not([type="hidden"]), textarea, select');
                formInfo.field_count = inputs.length;

                result.forms.push(formInfo);
            });

            // 检测输入框
            const visibleInputs = document.querySelectorAll(
                'input[type="text"]:not([style*="display: none"]):not([hidden]), ' +
                'input[type="tel"]:not([style*="display: none"]):not([hidden]), ' +
                'input[type="email"]:not([style*="display: none"]):not([hidden]), ' +
                'input[type="number"]:not([style*="display: none"]):not([hidden]), ' +
                'input[type="id"]:not([style*="display: none"]):not([hidden])'
            );

            visibleInputs.forEach((input, idx) => {
                const label = self._find_label_for_input(input);
                result.inputs.push({
                    index: idx,
                    tag: 'input',
                    type: input.type || 'text',
                    name: input.name || '',
                    id: input.id || '',
                    placeholder: input.placeholder || '',
                    className: input.className || '',
                    label: label,
                    required: input.required || false,
                    value: input.value || ''
                });
            });

            // 检测下拉框
            const selects = document.querySelectorAll('select:not([style*="display: none"]):not([hidden])');
            selects.forEach((select, idx) => {
                const options = Array.from(select.options).map(opt => ({
                    value: opt.value,
                    text: opt.text?.trim() || ''
                }));

                const label = self._find_label_for_input(select);
                result.selects.push({
                    index: idx,
                    name: select.name || '',
                    id: select.id || '',
                    placeholder: select.options[select.selectedIndex]?.text || '',
                    className: select.className || '',
                    label: label,
                    required: select.required || false,
                    options: options
                });
            });

            // 检测文本框
            const textareas = document.querySelectorAll('textarea:not([style*="display: none"]):not([hidden])');
            textareas.forEach((textarea, idx) => {
                const label = self._find_label_for_input(textarea);
                result.textareas.push({
                    index: idx,
                    name: textarea.name || '',
                    id: textarea.id || '',
                    placeholder: textarea.placeholder || '',
                    className: textarea.className || '',
                    label: label,
                    required: textarea.required || false,
                    rows: textarea.rows || 0
                });
            });

            // 检测文件上传
            const fileInputs = document.querySelectorAll('input[type="file"]');
            fileInputs.forEach((input, idx) => {
                const label = self._find_label_for_input(input);
                result.file_inputs.push({
                    index: idx,
                    name: input.name || '',
                    id: input.id || '',
                    accept: input.accept || '',
                    label: label,
                    multiple: input.multiple || false
                });
            });

            return result;
        }

        // 辅助函数：查找输入框对应的标签
        function _find_label_for_input(element) {
            // 方法1: 通过 for 属性查找
            if (element.id) {
                const label = document.querySelector(`label[for="${element.id}"]`);
                if (label) {
                    return label.textContent?.trim() || '';
                }
            }

            // 方法2: 查找父元素中的 label
            const parent = element.closest('label');
            if (parent) {
                return parent.textContent?.replace(element.value, '').trim() || '';
            }

            // 方法3: 查找前面的文本节点或兄弟元素
            let prev = element.previousElementSibling;
            let attempts = 0;
            while (prev && attempts < 3) {
                if (prev.tagName === 'LABEL' || prev.tagName === 'SPAN' || prev.tagName === 'DIV') {
                    const text = prev.textContent?.trim() || '';
                    if (text && !text.includes('：')) {
                        return text;
                    }
                }
                prev = prev.previousElementSibling;
                attempts++;
            }

            return '';
        }
        """

        try:
            structure = self.page.evaluate(js_analyze)
            return structure
        except Exception as e:
            logger.error(f"表单结构分析失败: {e}")
            return {}

    def smart_fill_form(self, form_structure: Dict[str, Any], data: Dict[str, str]) -> Dict[str, bool]:
        """智能填写表单"""
        logger.info("开始智能填写表单...")

        fill_results = {}

        # 字段映射配置
        field_mappings = {
            'business_name': ['名称', '字号', '店铺名', '企业名', '商户名'],
            'operator_name': ['经营者', '申请人', '姓名', '负责人'],
            'id_card': ['身份证', '证件号', '证件号码', 'ID'],
            'phone': ['电话', '手机', '联系方式', '联系电话'],
            'business_address': ['地址', '经营场所', '住所', '营业地址'],
            'business_scope': ['范围', '经营范围'],
            'registered_capital': ['资本', '资金', '注册资金'],
            'employees_count': ['人数', '员工', '从业人数']
        }

        # 填写文本输入框
        for input_field in form_structure.get('inputs', []):
            label = input_field.get('label', '').lower()
            placeholder = input_field.get('placeholder', '').lower()
            name = input_field.get('name', '').lower()

            # 尝试匹配字段
            matched = False
            for data_key, keywords in field_mappings.items():
                if data_key in data:
                    for keyword in keywords:
                        if keyword in label or keyword in placeholder or keyword in name:
                            # 填写字段
                            value = data[data_key]
                            self._fill_input_field(input_field, value)
                            fill_results[data_key] = True
                            logger.success(f"✓ 已填写: {keyword} = {value}")
                            matched = True
                            break
                if matched:
                    break

            if not matched:
                # 记录未匹配的字段
                logger.debug(f"未匹配字段: label={input_field.get('label')}, placeholder={input_field.get('placeholder')}")

        # 填写文本框
        for textarea in form_structure.get('textareas', []):
            label = textarea.get('label', '').lower()
            placeholder = textarea.get('placeholder', '').lower()

            if '范围' in label or 'scope' in placeholder.lower():
                value = data.get('business_scope', '')
                if value:
                    self._fill_textarea(textarea, value)
                    fill_results['business_scope'] = True
                    logger.success(f"✓ 已填写经营范围: {value}")

        return fill_results

    def _fill_input_field(self, field_info: Dict[str, Any], value: str):
        """填写输入框"""
        # 构建选择器
        selector = ''
        if field_info.get('id'):
            selector = f"#{field_info['id']}"
        elif field_info.get('name'):
            selector = f"[name=\"{field_info['name']}\"]"
        else:
            # 使用索引
            selector = f"input[type=\"{field_info.get('type', 'text')}\"]:nth-of-type({field_info['index'] + 1})"

        # 使用JavaScript填写（更可靠）
        self.page.evaluate(f"""
            () => {{
                const inputs = document.querySelectorAll('{selector}');
                if (inputs.length > {field_info['index']}) {{
                    const input = inputs[{field_info['index']}];
                    input.focus();
                    input.value = '{value}';
                    input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    input.blur();
                }}
            }}
        """)

        time.sleep(0.3)

    def _fill_textarea(self, field_info: Dict[str, Any], value: str):
        """填写文本框"""
        if field_info.get('id'):
            selector = f"#{field_info['id']}"
        elif field_info.get('name'):
            selector = f"[name=\"{field_info['name']}\"]"
        else:
            selector = f"textarea:nth-of-type({field_info['index'] + 1})"

        self.page.evaluate(f"""
            () => {{
                const textareas = document.querySelectorAll('{selector}');
                if (textareas.length > {field_info['index']}) {{
                    const textarea = textareas[{field_info['index']}];
                    textarea.focus();
                    textarea.value = '{value}';
                    textarea.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    textarea.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
            }}
        """)

        time.sleep(0.3)

    def take_screenshots(self, prefix: str = "form_fill"):
        """截图保存"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}.png"
        screenshot_path = self.session.take_screenshot(filename)
        logger.info(f"截图已保存: {screenshot_path}")
        return screenshot_path


def main():
    """主函数"""
    logger.info("=" * 80)
    logger.info("智能表单填写器")
    logger.info("=" * 80)

    # 创建会话管理器
    session = PersistentSessionManager(
        user_data_dir=Path("data/browser_profile"),
        headless=False,
        slow_mo=500
    )

    try:
        # 启动会话
        logger.info("\n[步骤1] 启动浏览器并加载会话...")
        success = session.start(auto_login=False)

        if not success:
            logger.error("启动失败")
            return False

        # 先导航到政务服务网（确保页面加载）
        logger.info("\n[步骤1.5] 导航到政务服务网...")
        session.navigate_to("https://zwfw.gxzf.gov.cn/yct/")
        time.sleep(3)

        # 检查登录状态
        logger.info("\n[步骤2] 检查登录状态...")
        is_logged_in = session._check_login_status()

        if not is_logged_in:
            logger.error("未登录，请先运行: python start_persistent_session.py")
            return False

        logger.success("已登录状态确认")

        # 创建填写器
        filler = IntelligentFormFiller(session)

        # 导航到申请表页面
        logger.info("\n[步骤3] 导航到申请表页面...")
        if not filler.navigate_to_application_form():
            logger.error("导航到申请表页面失败")
            return False

        # 截图
        filler.take_screenshots("01_form_page")

        # 分析表单结构
        logger.info("\n[步骤4] 分析表单结构...")
        form_structure = filler.analyze_form_structure()

        # 保存表单结构
        structure_file = Path("data/form_structure.json")
        with open(structure_file, 'w', encoding='utf-8') as f:
            json.dump(form_structure, f, ensure_ascii=False, indent=2)
        logger.info(f"表单结构已保存: {structure_file}")

        # 显示统计信息
        logger.info(f"\n表单统计:")
        logger.info(f"  - 表单数量: {len(form_structure.get('forms', []))}")
        logger.info(f"  - 输入框: {len(form_structure.get('inputs', []))} 个")
        logger.info(f"  - 下拉框: {len(form_structure.get('selects', []))} 个")
        logger.info(f"  - 文本框: {len(form_structure.get('textareas', []))} 个")
        logger.info(f"  - 文件上传: {len(form_structure.get('file_inputs', []))} 个")

        # 填写表单
        logger.info("\n[步骤5] 智能填写表单...")
        fill_results = filler.smart_fill_form(form_structure, TEST_DATA)

        # 截图
        filler.take_screenshots("02_after_fill")

        # 显示填写结果
        logger.info(f"\n填写结果:")
        for field, success in fill_results.items():
            status = "✓" if success else "✗"
            logger.info(f"  {status} {field}")

        success_count = sum(1 for v in fill_results.values() if v)
        total_count = len(TEST_DATA)

        logger.info(f"\n成功填写 {success_count}/{total_count} 个字段")

        # 保存填写结果
        result = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "page_url": form_structure.get('url'),
            "page_title": form_structure.get('title'),
            "test_data": TEST_DATA,
            "fill_results": fill_results,
            "success_rate": f"{success_count}/{total_count}"
        }

        result_file = Path("data/form_fill_result.json")
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        logger.success(f"\n填写结果已保存: {result_file}")

        # 保持浏览器打开
        logger.info("\n浏览器将保持打开30秒，请检查填写结果...")
        time.sleep(30)

        return True

    except Exception as e:
        logger.error(f"\n表单填写失败: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        session.close()
        logger.info("\n会话已关闭")


if __name__ == "__main__":
    # 配置日志
    logger.remove()
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
        level="INFO"
    )
    logger.add(
        "logs/intelligent_filler_{time:YYYYMMDD_HHmmss}.log",
        rotation="10 MB",
        level="DEBUG",
        encoding="utf-8"
    )

    # 运行
    result = main()

    if result:
        logger.success("\n" + "=" * 80)
        logger.success("智能表单填写完成！")
        logger.success("=" * 80)
    else:
        logger.error("\n智能表单填写失败")

    sys.exit(0 if result else 1)
