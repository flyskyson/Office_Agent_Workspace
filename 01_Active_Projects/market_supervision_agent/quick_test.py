"""
市场监管智能体 - 快速功能验证
"""

import sys
from pathlib import Path

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from browser_controller import BrowserController
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)

print("\n" + "="*60)
print("Market Supervision Agent - Quick Test")
print("="*60)

try:
    print("\n[1/3] Testing browser start...")
    with BrowserController(headless=False) as browser:
        print("[OK] Browser started successfully!")

        # 创建测试 HTML
        html = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Test Page</title></head>
<body>
    <h1>Browser Controller Test</h1>
    <input id="test-input" type="text" placeholder="Enter text">
    <button id="test-button">Click Me</button>
</body></html>"""

        test_file = Path(__file__).parent.parent / "test.html"
        test_file.write_text(html, encoding='utf-8')

        print("\n[2/3] Loading test page...")
        browser.navigate(f"file:///{test_file.as_posix()}")
        print(f"[OK] Page title: {browser.page.title()}")

        print("\n[3/3] Testing form interaction...")
        browser.fill_form("#test-input", "Hello World")
        print("[OK] Form filled successfully!")

        # 截图
        screenshot = Path(__file__).parent.parent / "quick_test.png"
        browser.screenshot(str(screenshot))
        print(f"[OK] Screenshot saved: {screenshot}")

        print("\n" + "="*60)
        print("[SUCCESS] All tests passed!")
        print("="*60)

        import time
        print("\nBrowser will close in 3 seconds...")
        time.sleep(3)

        # 清理
        if test_file.exists():
            test_file.unlink()

except Exception as e:
    print(f"\n[ERROR] Test failed: {e}")
    import traceback
    traceback.print_exc()

print("\n[DONE] Test completed.\n")
