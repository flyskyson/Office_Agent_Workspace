#!/usr/bin/env python3
"""
零基础学员测试脚本
专门为没有编程经验的学员设计
"""

import os
import sys
import time
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def print_header(text):
    """打印漂亮的标题"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def check_environment():
    """检查环境配置"""
    print_header("步骤1: 检查环境配置")

    # 检查配置文件
    config_files = [
        ("config/selectors.yaml", "选择器配置文件"),
        ("config/urls.yaml", "URL配置文件"),
        (".env", "环境变量文件"),
        ("data/sample_customers.json", "示例数据文件")
    ]

    all_ok = True
    for file_path, description in config_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"✅ {description}: {file_path}")
        else:
            print(f"❌ {description}: {file_path} (未找到)")
            all_ok = False

    return all_ok

def test_browser_simple():
    """简单测试浏览器功能"""
    print_header("步骤2: 测试浏览器功能")

    try:
        # 尝试导入Playwright
        from playwright.sync_api import sync_playwright

        print("正在启动浏览器...")

        with sync_playwright() as p:
            # 启动浏览器
            browser = p.chromium.launch(headless=False)  # headless=False 显示浏览器窗口
            print("✅ 浏览器启动成功")

            # 创建页面
            page = browser.new_page()
            print("✅ 页面创建成功")

            # 导航到测试页面
            test_url = "https://www.baidu.com"
            print(f"正在导航到: {test_url}")
            page.goto(test_url)

            # 截图保存
            screenshot_path = project_root / "logs" / "screenshots" / "test_browser.png"
            screenshot_path.parent.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(screenshot_path))
            print(f"✅ 截图已保存: {screenshot_path}")

            # 获取页面标题
            title = page.title()
            print(f"✅ 页面标题: {title}")

            # 关闭浏览器
            browser.close()
            print("✅ 浏览器已关闭")

            return True

    except Exception as e:
        print(f"❌ 浏览器测试失败: {str(e)}")
        print("\n💡 可能的原因:")
        print("1. Playwright未安装: 运行 'playwright install chromium'")
        print("2. 浏览器未安装: 确保已安装Chrome或Edge")
        print("3. 网络连接问题: 检查网络连接")
        return False

def test_configuration():
    """测试配置文件"""
    print_header("步骤3: 测试配置文件")

    try:
        import yaml

        # 测试选择器配置文件
        selectors_path = project_root / "config" / "selectors.yaml"
        if selectors_path.exists():
            with open(selectors_path, 'r', encoding='utf-8') as f:
                selectors = yaml.safe_load(f)

            print("✅ 选择器配置文件解析成功")

            # 检查关键配置
            required_sections = ['login']
            for section in required_sections:
                if section in selectors:
                    print(f"  ✅ 找到配置节: {section}")
                else:
                    print(f"  ⚠️  缺少配置节: {section}")

        # 测试URL配置文件
        urls_path = project_root / "config" / "urls.yaml"
        if urls_path.exists():
            with open(urls_path, 'r', encoding='utf-8') as f:
                urls = yaml.safe_load(f)
            print("✅ URL配置文件解析成功")

        return True

    except Exception as e:
        print(f"❌ 配置文件测试失败: {str(e)}")
        return False

def test_sample_data():
    """测试示例数据"""
    print_header("步骤4: 测试示例数据")

    try:
        import json

        data_path = project_root / "data" / "sample_customers.json"
        if data_path.exists():
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            print("✅ 示例数据文件解析成功")

            # 显示数据统计
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, list):
                        print(f"  📊 {key}: {len(value)} 条记录")
                    else:
                        print(f"  📊 {key}: 已配置")
            elif isinstance(data, list):
                print(f"  📊 总记录数: {len(data)}")

            return True
        else:
            print("⚠️  示例数据文件未找到")
            return False

    except Exception as e:
        print(f"❌ 示例数据测试失败: {str(e)}")
        return False

def generate_next_steps():
    """生成下一步建议"""
    print_header("🎯 下一步学习建议")

    print("根据你的业务需求，建议按以下顺序学习:")
    print("\n1. 🔧 基础配置 (1-2天)")
    print("   • 学习使用浏览器开发者工具 (F12)")
    print("   • 配置登录页面的选择器")
    print("   • 运行 quick_test.py 测试登录")

    print("\n2. 📝 业务表单配置 (2-3天)")
    print("   • 选择一种业务类型开始:")
    print("     a) 个体工商户设立登记")
    print("     b) 个体工商户变更登记")
    print("     c) 个体工商户年报")
    print("   • 配置对应的表单选择器")

    print("\n3. 🧪 功能测试 (1-2天)")
    print("   • 测试单个企业处理")
    print("   • 测试批量处理")
    print("   • 验证结果准确性")

    print("\n4. 📊 数据管理 (2-3天)")
    print("   • 设计本地数据库结构")
    print("   • 实现数据导入导出")
    print("   • 建立查询统计功能")

    print("\n5. 🖥️ 用户界面 (可选, 3-5天)")
    print("   • 开发简单Web界面")
    print("   • 添加文件上传功能")
    print("   • 实现进度监控")

def main():
    """主函数"""
    print_header("市场监管智能体 - 零基础测试")
    print("专为没有编程经验的学员设计")
    print("版本: 1.0 | 日期: 2026-01-11")

    # 检查环境
    env_ok = check_environment()
    if not env_ok:
        print("\n⚠️  环境配置不完整，请先完成基础配置")
        print("参考 CONFIG_CHECKLIST.md 文件")

    # 测试浏览器
    browser_ok = test_browser_simple()

    # 测试配置
    config_ok = test_configuration()

    # 测试数据
    data_ok = test_sample_data()

    # 总结
    print_header("测试结果总结")

    if all([env_ok, browser_ok, config_ok, data_ok]):
        print("🎉 所有测试通过！可以开始配置业务自动化了。")
    else:
        print("⚠️  部分测试未通过，请根据上面的提示解决问题。")

    # 生成下一步建议
    generate_next_steps()

    print_header("📚 学习资源")
    print("1. 配置检查清单: CONFIG_CHECKLIST.md")
    print("2. 选择器指南: SELECTOR_GUIDE.md")
    print("3. 项目文档: README.md")
    print("4. 恢复指南: RESTORE_GUIDE.md")

    print("\n💡 提示: 遇到问题时，可以:")
    print("• 查看日志文件: logs/ 目录")
    print("• 检查截图: logs/screenshots/ 目录")
    print("• 参考错误信息调整配置")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 测试已取消")
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()