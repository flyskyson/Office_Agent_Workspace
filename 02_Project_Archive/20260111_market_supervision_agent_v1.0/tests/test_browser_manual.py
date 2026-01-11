"""
简单的浏览器控制器测试
不需要网络连接
"""

import sys
import logging
from pathlib import Path

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from browser_controller import BrowserController

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_browser_basic():
    """测试浏览器基本功能"""
    print("\n" + "="*60)
    print("测试 1: 浏览器启动和关闭")
    print("="*60)

    try:
        browser = BrowserController(headless=False)
        browser.start()
        print("✅ 浏览器启动成功")

        # 等待一下让用户看到浏览器
        import time
        time.sleep(2)

        browser.close()
        print("✅ 浏览器关闭成功")

        return True
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_context_manager():
    """测试上下文管理器"""
    print("\n" + "="*60)
    print("测试 2: 上下文管理器")
    print("="*60)

    try:
        with BrowserController(headless=False) as browser:
            print("✅ 浏览器已通过上下文管理器启动")
            import time
            time.sleep(2)

        print("✅ 浏览器已自动关闭")
        return True
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_local_file():
    """测试加载本地 HTML 文件"""
    print("\n" + "="*60)
    print("测试 3: 加载本地文件")
    print("="*60)

    # 创建一个简单的 HTML 文件
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>测试页面</title>
    <meta charset="UTF-8">
</head>
<body>
    <h1>浏览器控制器测试页面</h1>
    <p>这是一个测试页面，用于验证浏览器控制器功能。</p>

    <form>
        <label>用户名: <input type="text" id="username" placeholder="请输入用户名"></label><br><br>
        <label>密码: <input type="password" id="password" placeholder="请输入密码"></label><br><br>
        <button type="submit">登录</button>
    </form>
</body>
</html>
    """

    test_file = Path(__file__).parent.parent / "test_page.html"
    test_file.write_text(html_content, encoding='utf-8')

    try:
        with BrowserController(headless=False) as browser:
            # 使用 file:// 协议加载本地文件
            file_url = f"file:///{test_file.as_posix()}"
            print(f"正在加载: {file_url}")

            browser.navigate(file_url)
            print("✅ 页面加载成功")

            # 获取页面标题
            title = browser.page.title()
            print(f"页面标题: {title}")

            # 测试填写表单
            print("\n正在测试表单填写...")
            browser.fill_form("#username", "test_user")
            browser.fill_form("#password", "test_password")
            print("✅ 表单填写成功")

            # 截图
            screenshot_path = Path(__file__).parent.parent / "test_screenshot.png"
            browser.screenshot(str(screenshot_path))
            print(f"✅ 截图已保存: {screenshot_path}")

            # 等待用户查看
            import time
            print("\n浏览器将在 5 秒后关闭...")
            time.sleep(5)

        return True
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # 清理测试文件
        if test_file.exists():
            test_file.unlink()

def main():
    """运行所有测试"""
    print("\n" + "="*60)
    print("[TEST] 市场监管智能体 - 浏览器控制器测试套件")
    print("="*60)

    results = []

    # 测试 1: 基本功能
    results.append(("基本功能", test_browser_basic()))

    # 测试 2: 上下文管理器
    results.append(("上下文管理器", test_context_manager()))

    # 测试 3: 本地文件
    results.append(("本地文件加载", test_local_file()))

    # 结果汇总
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)

    for test_name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{test_name}: {status}")

    total = len(results)
    passed = sum(1 for _, p in results if p)

    print("\n" + "="*60)
    print(f"总计: {passed}/{total} 测试通过")
    print("="*60)

    if passed == total:
        print("\n[OK] 所有测试通过！浏览器控制器工作正常。")
    else:
        print(f"\n[WARN] {total - passed} 个测试失败，请检查错误信息。")

if __name__ == "__main__":
    main()
