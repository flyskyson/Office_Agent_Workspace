#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
广西政务服务平台 - 企业开办一件事 自动化登录脚本

使用方法：
1. 安装依赖: pip install playwright
2. 安装浏览器: playwright install chromium
3. 运行脚本: python 广西政务自动登录.py
"""

import asyncio
from playwright.async_api import async_playwright
import time

# 登录凭据
USERNAME = "15577555337"
PASSWORD = "Flyskylj1"

# 目标URL
LOGIN_URL = "https://zwfw.gxzf.gov.cn/yct/"
BUSINESS_SETUP_URL = "https://zwfw.gxzf.gov.cn/yct/"


async def login_and_navigate():
    """登录并导航到企业开办一件事"""
    print("=" * 60)
    print("广西政务服务平台 - 自动化登录")
    print("=" * 60)
    print()

    async with async_playwright() as p:
        # 启动浏览器（使用 Chromium）
        browser = await p.chromium.launch(
            headless=False,  # 显示浏览器窗口
            slow_mo=500      # 操作间隔（毫秒），便于观察
        )

        # 创建浏览器上下文
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )

        # 创建新页面
        page = await context.new_page()

        try:
            # 步骤1: 打开首页
            print("[1/5] 正在打开广西政务服务平台...")
            await page.goto(LOGIN_URL, wait_until='networkidle', timeout=30000)
            print("      首页加载完成")
            await asyncio.sleep(1)

            # 步骤2: 点击"企业开办一件事"
            print("[2/5] 正在查找'企业开办一件事'入口...")

            # 尝试多种方式找到并点击"企业开办一件事"
            clicked = False

            # 方法1: 通过文本查找
            try:
                await page.wait_for_selector('text="企业开办"', timeout=5000)
                await page.click('text="企业开办"', timeout=5000)
                clicked = True
                print("      点击成功")
            except:
                print("      方法1失败，尝试方法2...")

            # 方法2: 通过链接导航
            if not clicked:
                try:
                    # 直接导航到登录页面
                    login_page_url = "https://zwfw.gxzf.gov.cn/gxzwfw/phaseii/login/tologin.do?gotourl=//zwfw.gxzf.gov.cn"
                    await page.goto(login_page_url, wait_until='networkidle', timeout=30000)
                    clicked = True
                    print("      直接导航到登录页面")
                except:
                    print("      方法2失败，尝试方法3...")

            await asyncio.sleep(2)

            # 步骤3: 填写登录信息
            print("[3/5] 正在填写登录信息...")

            # 等待登录表单加载
            await page.wait_for_selector('textbox[placeholder*="身份证"], textbox[placeholder*="手机"]', timeout=10000)

            # 填写用户名
            await page.fill('textbox[placeholder*="身份证"], textbox[placeholder*="手机"]', USERNAME)
            print(f"      用户名: {USERNAME}")

            # 填写密码
            await page.fill('input[type="password"]', PASSWORD)
            print("      密码: ********")

            await asyncio.sleep(1)

            # 步骤4: 等待用户完成滑块验证
            print("[4/5] 等待滑块验证...")
            print("      请在浏览器中手动拖动滑块完成验证")
            print("      完成后脚本将自动点击登录按钮...")

            # 等待登录按钮可点击（用户完成滑块验证后）
            await page.wait_for_selector('button:has-text("登录")', timeout=120000)  # 最多等待2分钟

            # 额外等待，让用户有时间完成滑块
            await asyncio.sleep(2)

            # 步骤5: 点击登录
            print("[5/5] 正在点击登录按钮...")
            await page.click('button:has-text("登录")')
            print("      登录请求已发送")

            # 等待页面跳转
            await asyncio.sleep(3)

            # 检查是否登录成功
            current_url = page.url
            print()
            print("=" * 60)
            print("当前页面:", current_url)

            if "login" not in current_url.lower():
                print("登录成功！")
                print()
                print("接下来可以:")
                print("1. 查找并点击'企业开办一件事'入口")
                print("2. 或直接访问业务办理页面")
                print()
                print("浏览器将保持打开状态，你可以继续操作...")
                print()
                print("按 Ctrl+C 退出脚本")
            else:
                print("登录可能失败，请检查:")
                print("- 滑块验证是否完成")
                print("- 用户名和密码是否正确")
                print("- 是否需要短信验证码")

            # 保持浏览器打开，等待用户操作
            print()
            input("按 Enter 键关闭浏览器...")

        except Exception as e:
            print(f"发生错误: {e}")
            import traceback
            traceback.print_exc()

        finally:
            await browser.close()


def main():
    """主函数"""
    try:
        asyncio.run(login_and_navigate())
    except KeyboardInterrupt:
        print("\n\n用户中断，正在退出...")
    except Exception as e:
        print(f"\n程序异常退出: {e}")


if __name__ == "__main__":
    main()
