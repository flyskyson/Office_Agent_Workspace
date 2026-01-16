#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版表单填写器

能够智能处理公告页面，找到进入实际表单的入口

作者: Claude Code
日期: 2026-01-14
"""

import sys
import time
import json
from pathlib import Path

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
    "business_scope": "日用百货销售；预包装食品销售"
}


class EnhancedFormFiller:
    """增强版表单填写器"""

    def __init__(self, session: PersistentSessionManager):
        self.session = session
        self.page = session.page

    def detect_page_state(self) -> dict:
        """检测页面状态"""
        url = self.page.url
        title = self.page.title()

        logger.info(f"当前页面: {url}")
        logger.info(f"页面标题: {title}")

        # 使用JavaScript深度分析页面
        js_analyze = """
        () => {
            const result = {
                url: window.location.href,
                title: document.title,
                page_type: 'unknown',
                elements: {
                    links: [],
                    buttons: [],
                    iframes: []
                },
                text_content: ''
            };

            // 获取页面主要文本内容
            const bodyText = document.body.textContent || '';
            result.text_content = bodyText.substring(0, 500);

            // 检测iframe（很多政务系统使用iframe）
            const iframes = document.querySelectorAll('iframe');
            iframes.forEach((iframe, idx) => {
                result.elements.iframes.push({
                    index: idx,
                    id: iframe.id || '',
                    name: iframe.name || '',
                    src: iframe.src || '',
                    title: iframe.title || ''
                });
            });

            // 检测所有链接
            const links = document.querySelectorAll('a[href]');
            links.forEach((link, idx) => {
                if (idx < 50) {  // 只取前50个
                    result.elements.links.push({
                        index: idx,
                        text: link.textContent?.trim().substring(0, 50) || '',
                        href: link.href || ''
                    });
                }
            });

            // 检测所有按钮
            const buttons = document.querySelectorAll('button, [role="button"], [onclick]');
            buttons.forEach((btn, idx) => {
                if (idx < 30) {  // 只取前30个
                    result.elements.buttons.push({
                        index: idx,
                        text: btn.textContent?.trim().substring(0, 50) || '',
                        onclick: btn.getAttribute('onclick') || '',
                        className: btn.className || ''
                    });
                }
            });

            // 判断页面类型
            if (bodyText.includes('关于停用启用') || bodyText.includes('食品许可模块')) {
                result.page_type = 'announcement';
            } else if (bodyText.includes('个体工商户') || bodyText.includes('开业') ||
                       bodyText.includes('名称预先核准') || bodyText.includes('设立登记')) {
                result.page_type = 'business_setup';
            } else if (url.includes('companySetup') || title.includes('企业开办')) {
                result.page_type = 'enterprise_setup';
            } else if (bodyText.includes('登录') || url.includes('login')) {
                result.page_type = 'login';
            }

            return result;
        }
        """

        try:
            state = self.page.evaluate(js_analyze)
            logger.info(f"页面类型: {state.get('page_type', 'unknown')}")
            logger.info(f"iframe数量: {len(state.get('elements', {}).get('iframes', []))}")
            logger.info(f"链接数量: {len(state.get('elements', {}).get('links', []))}")
            logger.info(f"按钮数量: {len(state.get('elements', {}).get('buttons', []))}")
            return state
        except Exception as e:
            logger.error(f"页面状态检测失败: {e}")
            return {}

    def find_and_click_entry(self, page_state: dict) -> bool:
        """查找并点击进入表单的入口"""
        logger.info("查找表单入口...")

        # 方法1: 检查是否有iframe（很多政务系统用iframe嵌套表单）
        iframes = page_state.get('elements', {}).get('iframes', [])
        if iframes:
            logger.info(f"发现 {len(iframes)} 个iframe")

            for iframe in iframes:
                src = iframe.get('src', '')
                logger.info(f"  - iframe: {src[:100]}")

                # 如果iframe包含表单相关内容
                if any(kw in src.lower() for kw in ['form', 'apply', 'setup', 'register']):
                    logger.success(f"找到表单iframe: {src}")
                    # 直接导航到iframe的src
                    self.page.goto(src)
                    time.sleep(3)
                    return True

        # 方法2: 查找相关链接
        links = page_state.get('elements', {}).get('links', [])
        keywords = ['个体工商户', '开业', '设立', '登记', '名称', '申请', '办理']

        for link in links:
            text = link.get('text', '')
            href = link.get('href', '')

            for keyword in keywords:
                if keyword in text:
                    logger.success(f"找到链接: {text}")
                    logger.info(f"  URL: {href}")

                    if href and not href.startswith('javascript:'):
                        self.page.goto(href)
                        time.sleep(3)
                        return True

        # 方法3: 查找按钮
        buttons = page_state.get('elements', {}).get('buttons', [])
        for btn in buttons:
            text = btn.get('text', '')
            onclick = btn.get('onclick', '')

            for keyword in keywords:
                if keyword in text or keyword in onclick:
                    logger.success(f"找到按钮: {text}")
                    if onclick:
                        # 执行onclick
                        self.page.evaluate(f"{onclick}")
                        time.sleep(3)
                        return True

        # 方法4: 检查页面文本，查找可能的提示信息
        text_content = page_state.get('text_content', '')
        logger.info("页面文本内容:")
        logger.info(text_content[:300])

        # 如果是公告页面，尝试查找"我知道了"或"进入"按钮
        if '关于停用启用' in text_content:
            logger.info("检测到公告页面，查找关闭按钮...")

            js_find_close = """
            () => {
                // 查找各种可能的关闭/进入按钮
                const selectors = [
                    'button:contains("关闭")',
                    'button:contains("我知道了")',
                    'button:contains("进入")',
                    'a:contains("关闭")',
                    'a:contains("我知道了")',
                    'div[onclick*="close"]',
                    'div[onclick*="enter"]'
                ];

                for (let selector of selectors) {
                    const elements = document.querySelectorAll(selector.replace(':contains', ''));
                    for (let el of elements) {
                        if (el.textContent && (el.textContent.includes('关闭') ||
                            el.textContent.includes('我知道了') || el.textContent.includes('进入'))) {
                            return {
                                found: true,
                                tag: el.tagName,
                                text: el.textContent,
                                onclick: el.getAttribute('onclick') || ''
                            };
                        }
                    }
                }

                return {found: false};
            }
            """

            try:
                result = self.page.evaluate(js_find_close)
                if result.get('found'):
                    logger.info(f"找到关闭按钮: {result.get('text')}")
                    # 点击关闭
                    if result.get('onclick'):
                        self.page.evaluate(result['onclick'])
                    time.sleep(2)
                    return True
            except:
                pass

        logger.warning("未找到表单入口")
        return False

    def deep_detect_form_fields(self) -> dict:
        """深度检测表单字段（包括iframe内的）"""
        logger.info("深度检测表单字段...")

        js_detect = """
        () => {
            const result = {
                url: window.location.href,
                title: document.title,
                forms: [],
                fields: {
                    inputs: [],
                    selects: [],
                    textareas: [],
                    radios: [],
                    checkboxes: []
                }
            };

            // 检测所有可见的输入字段
            const allInputs = document.querySelectorAll('input:not([type="hidden"]):not([style*="display: none"])');
            allInputs.forEach((input, idx) => {
                const visible = input.offsetParent !== null;
                if (visible && idx < 100) {
                    const label = self._get_label(input);
                    result.fields.inputs.push({
                        index: idx,
                        type: input.type || 'text',
                        name: input.name || '',
                        id: input.id || '',
                        placeholder: input.placeholder || '',
                        className: input.className || '',
                        label: label,
                        value: input.value || '',
                        required: input.required
                    });
                }
            });

            // 检测下拉框
            const selects = document.querySelectorAll('select:not([style*="display: none"])');
            selects.forEach((select, idx) => {
                if (idx < 50) {
                    const options = Array.from(select.options).map(opt => ({
                        value: opt.value,
                        text: opt.text?.trim() || ''
                    }));
                    const label = self._get_label(select);
                    result.fields.selects.push({
                        index: idx,
                        name: select.name || '',
                        id: select.id || '',
                        className: select.className || '',
                        label: label,
                        options: options
                    });
                }
            });

            // 检测文本框
            const textareas = document.querySelectorAll('textarea:not([style*="display: none"])');
            textareas.forEach((textarea, idx) => {
                if (idx < 20) {
                    const label = self._get_label(textarea);
                    result.fields.textareas.push({
                        index: idx,
                        name: textarea.name || '',
                        id: textarea.id || '',
                        placeholder: textarea.placeholder || '',
                        label: label
                    });
                }
            });

            return result;

            function _get_label(element) {
                if (element.id) {
                    const label = document.querySelector(`label[for="${element.id}"]`);
                    if (label) return label.textContent?.trim() || '';
                }

                const parentLabel = element.closest('label');
                if (parentLabel) {
                    return parentLabel.textContent?.trim() || '';
                }

                let prev = element.previousElementSibling;
                let attempts = 0;
                while (prev && attempts < 5) {
                    if (prev.tagName === 'LABEL' || prev.tagName === 'SPAN' ||
                        prev.tagName === 'DIV' || prev.tagName === 'TD') {
                        const text = prev.textContent?.trim() || '';
                        if (text && text.length < 100 && !text.includes('：')) {
                            return text;
                        }
                    }
                    prev = prev.previousElementSibling;
                    attempts++;
                }

                return '';
            }
        }
        """

        try:
            fields = self.page.evaluate(js_detect)

            logger.info(f"检测到:")
            logger.info(f"  - 输入框: {len(fields.get('fields', {}).get('inputs', []))} 个")
            logger.info(f"  - 下拉框: {len(fields.get('fields', {}).get('selects', []))} 个")
            logger.info(f"  - 文本框: {len(fields.get('fields', {}).get('textareas', []))} 个")

            return fields
        except Exception as e:
            logger.error(f"字段检测失败: {e}")
            return {}

    def smart_fill_fields(self, fields: dict, data: dict) -> dict:
        """智能填写字段"""
        logger.info("开始智能填写...")
        results = {}

        # 字段映射
        mappings = {
            'business_name': ['名称', '字号', '店铺', '商户'],
            'operator_name': ['经营者', '申请人', '姓名'],
            'id_card': ['身份证', '证件', 'ID'],
            'phone': ['电话', '手机', '联系'],
            'business_address': ['地址', '场所', '住所'],
            'business_scope': ['范围', '主营']
        }

        # 填写输入框
        for input_field in fields.get('fields', {}).get('inputs', []):
            label = input_field.get('label', '').lower()
            placeholder = input_field.get('placeholder', '').lower()

            matched = False
            for data_key, keywords in mappings.items():
                if data_key in data:
                    for keyword in keywords:
                        if keyword in label or keyword in placeholder:
                            value = data[data_key]
                            self._fill_input(input_field, value)
                            results[data_key] = True
                            logger.success(f"✓ 填写: {keyword} = {value}")
                            matched = True
                            break
                if matched:
                    break

        # 填写文本框
        for textarea in fields.get('fields', {}).get('textareas', []):
            label = textarea.get('label', '').lower()
            if '范围' in label:
                value = data.get('business_scope', '')
                if value:
                    self._fill_textarea(textarea, value)
                    results['business_scope'] = True
                    logger.success(f"✓ 填写经营范围: {value}")

        return results

    def _fill_input(self, field: dict, value: str):
        """填写输入框"""
        if field.get('id'):
            selector = f"#{field['id']}"
        elif field.get('name'):
            selector = f"[name=\"{field['name']}\"]"
        else:
            selector = f"input[type=\"{field.get('type', 'text')}\"]"

        self.page.evaluate(f"""
            () => {{
                const input = document.querySelector('{selector}');
                if (input) {{
                    input.focus();
                    input.value = '{value}';
                    input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    input.blur();
                }}
            }}
        """)
        time.sleep(0.3)

    def _fill_textarea(self, field: dict, value: str):
        """填写文本框"""
        if field.get('id'):
            selector = f"#{field['id']}"
        elif field.get('name'):
            selector = f"[name=\"{field['name']}\"]"
        else:
            selector = "textarea"

        self.page.evaluate(f"""
            () => {{
                const textarea = document.querySelector('{selector}');
                if (textarea) {{
                    textarea.focus();
                    textarea.value = '{value}';
                    textarea.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    textarea.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
            }}
        """)
        time.sleep(0.3)


def main():
    """主函数"""
    logger.info("=" * 80)
    logger.info("增强版表单填写器")
    logger.info("=" * 80)

    session = PersistentSessionManager(
        user_data_dir=Path("data/browser_profile"),
        headless=False,
        slow_mo=500
    )

    try:
        # 启动
        logger.info("\n[步骤1] 启动浏览器...")
        success = session.start(auto_login=False)
        if not success:
            logger.error("启动失败")
            return False

        # 导航
        logger.info("\n[步骤2] 导航到政务服务网...")
        session.navigate_to("https://zwfw.gxzf.gov.cn/yct/")
        time.sleep(3)

        # 检查登录
        logger.info("\n[步骤3] 检查登录状态...")
        if not session._check_login_status():
            logger.error("未登录")
            return False
        logger.success("已登录")

        # 创建填写器
        filler = EnhancedFormFiller(session)

        # 检测页面状态
        logger.info("\n[步骤4] 检测页面状态...")
        page_state = filler.detect_page_state()

        # 保存状态
        state_file = Path("data/page_state.json")
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(page_state, f, ensure_ascii=False, indent=2)
        logger.info(f"页面状态已保存: {state_file}")

        # 查找并点击入口
        logger.info("\n[步骤5] 查找表单入口...")
        max_attempts = 3
        for attempt in range(max_attempts):
            logger.info(f"尝试 {attempt + 1}/{max_attempts}...")

            if filler.find_and_click_entry(page_state):
                logger.success("成功进入表单页面")
                time.sleep(2)

                # 重新检测页面
                page_state = filler.detect_page_state()

                # 深度检测字段
                logger.info("\n[步骤6] 深度检测表单字段...")
                fields = filler.deep_detect_form_fields()

                # 保存字段信息
                fields_file = Path("data/form_fields_detail.json")
                with open(fields_file, 'w', encoding='utf-8') as f:
                    json.dump(fields, f, ensure_ascii=False, indent=2)
                logger.info(f"字段信息已保存: {fields_file}")

                # 如果找到输入框，尝试填写
                input_count = len(fields.get('fields', {}).get('inputs', []))
                if input_count > 1:  # 排除搜索框
                    logger.info(f"\n[步骤7] 填写表单...")
                    results = filler.smart_fill_fields(fields, TEST_DATA)

                    success_count = sum(1 for v in results.values() if v)
                    logger.info(f"\n填写结果: {success_count} 个字段")

                    # 截图
                    screenshot = session.take_screenshot("form_filled.png")
                    logger.info(f"截图: {screenshot}")

                break
            else:
                logger.warning(f"尝试 {attempt + 1} 失败")
                if attempt < max_attempts - 1:
                    time.sleep(2)

        logger.info("\n浏览器保持打开30秒...")
        time.sleep(30)

        return True

    except Exception as e:
        logger.error(f"\n执行失败: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        session.close()


if __name__ == "__main__":
    logger.remove()
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
        level="INFO"
    )
    logger.add(
        "logs/enhanced_filler_{time:YYYYMMDD_HHmmss}.log",
        rotation="10 MB",
        level="DEBUG",
        encoding="utf-8"
    )

    result = main()

    if result:
        logger.success("\n" + "=" * 80)
        logger.success("增强版表单填写完成！")
        logger.success("=" * 80)
    else:
        logger.error("\n执行失败")

    sys.exit(0 if result else 1)
