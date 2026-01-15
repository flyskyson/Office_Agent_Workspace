# -*- coding: utf-8 -*-
"""
工作区统一新闻入口
整合多种新闻获取方式
"""
import asyncio
import sys
from pathlib import Path

# Windows 编码修复
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')


def print_menu():
    """打印菜单"""
    print("="*60)
    print("📰 工作区新闻中心")
    print("="*60)
    print()
    print("请选择获取新闻的方式：")
    print()
    print("  1. 🕷️  Playwright 爬虫（微博真实数据）")
    print("  2. 📦 模拟数据（多平台演示）")
    print("  3. 🌐 MCP 服务器（需要启动）")
    print()
    print("配置指南：")
    print("  4. 📖 查看部署教程（DailyHotApi + Vercel）")
    print("  5. 🔧 查看 TrendRadar 设置")
    print()
    print("  0. 退出")
    print()
    print("="*60)


async def option_1_scraper():
    """Playwright 爬虫"""
    print("\n🕷️  使用 Playwright 爬取微博热搜...")
    print()

    # 导入爬虫模块
    import importlib.util
    spec = importlib.util.spec_from_file_location("news_scraper", "00_Agent_Library/news_scraper.py")
    news_scraper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(news_scraper)

    scraper = news_scraper.NewsScraper()

    try:
        from playwright.async_api import async_playwright
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            # 爬取微博
            result = await scraper.scrape_weibo(page, limit=10)
            if result:
                print(scraper.format_output(result))

            await browser.close()
    except ImportError:
        print("❌ Playwright 未安装")
        print("   请运行: pip install playwright && playwright install chromium")
    except Exception as e:
        print(f"❌ 爬取失败: {e}")


async def option_2_mock():
    """模拟数据"""
    print("\n📦 使用模拟数据...")
    print()

    import importlib.util
    spec = importlib.util.spec_from_file_location("news_reader", "00_Agent_Library/news_reader.py")
    news_reader = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(news_reader)

    reader = news_reader.UnifiedNewsReader()

    # 获取多个平台
    platforms = ["zhihu", "weibo", "bilibili"]
    for platform in platforms:
        result = await reader.fetch_from_vvhan(platform, limit=5)
        if result:
            print(reader.format_output(result))


async def option_3_mcp():
    """MCP 服务器"""
    print("\n🌐 MCP 服务器模式")
    print()
    print("可用的 MCP 服务器：")
    print("  1. mcp-hot-news")
    print("     启动: mcp-hot-news")
    print()
    print("  2. @wopal/mcp-server-hotnews")
    print("     启动: npx @wopal/mcp-server-hotnews")
    print()
    print("💡 提示：MCP 服务器需要单独启动，然后通过 MCP 客户端调用")


def option_4_guide():
    """部署教程"""
    print("\n📖 DailyHotApi 部署教程")
    print()

    guide_file = Path("docs/guides/DEPLOY_DAILYHOTAPI.md")
    if guide_file.exists():
        print(f"📄 详细教程: {guide_file}")
        print()
        print("快速步骤：")
        print("  1. 访问 https://github.com/imsyy/DailyHotApi-Vercel")
        print("  2. Fork 项目到你的 GitHub")
        print("  3. 在 Vercel 导入并部署")
        print("  4. 获得 *.vercel.app 域名")
        print("  5. 在代码中使用 API")
    else:
        print("📄 部署教程文件不存在")
        print("   请访问: https://github.com/imsyy/DailyHotApi-Vercel")


def option_5_trendradar():
    """TrendRadar 设置"""
    print("\n🔧 TrendRadar 设置指南")
    print()
    print("项目地址: https://github.com/sansan0/TrendRadar")
    print()
    print("功能特点：")
    print("  ✅ 监控 35+ 平台热榜")
    print("  ✅ 基于 GitHub Actions（免费）")
    print("  ✅ 自动推送和 AI 分析")
    print("  ✅ 无需自己维护服务器")
    print()
    print("设置步骤：")
    print("  1. Fork 项目到你的 GitHub")
    print("  2. 启用 GitHub Actions")
    print("  3. 配置 Secrets（如需要）")
    print("  4. 运行 Workflow")


async def main():
    """主函数"""
    while True:
        print_menu()

        choice = input("请选择 (0-5): ").strip()

        if choice == "0":
            print("\n👋 再见！")
            break

        elif choice == "1":
            await option_1_scraper()

        elif choice == "2":
            await option_2_mock()

        elif choice == "3":
            await option_3_mcp()

        elif choice == "4":
            option_4_guide()

        elif choice == "5":
            option_5_trendradar()

        else:
            print("\n❌ 无效选择，请重新输入")

        input("\n按回车继续...")


if __name__ == "__main__":
    asyncio.run(main())
