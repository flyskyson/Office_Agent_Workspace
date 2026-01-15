# -*- coding: utf-8 -*-
"""
AI 技术新闻看板
AI Tech News Dashboard

为 AI 技术爱好者定制的新闻聚合工具
"""
import asyncio
import sys
from pathlib import Path

# Windows 编码修复
if sys.platform == 'win32' and hasattr(sys.stdout, 'buffer'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')


def print_banner():
    """打印横幅"""
    print()
    print("█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + " " * 20 + "🤖 AI 技术新闻看板" + " " * 28 + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)
    print()


def print_menu():
    """打印菜单"""
    print("📰 新闻来源：")
    print()
    print("  【真实数据】")
    print("  1. 🕷️  微博热搜（筛选AI相关）")
    print("  2. 🔥 知乎热榜（AI技术讨论）")
    print("  3. 📊 百度热搜（科技热点）")
    print()
    print("  【AI 专属】")
    print("  4. 🤖 AI 新闻聚合器（模拟数据）")
    print("  5. 🚀 AI 工具追踪（GitHub/MCP）")
    print("  6. 🧠 智能监控（学习您的兴趣）")
    print()
    print("  【配置】")
    print("  7. ⚙️  管理兴趣关键词")
    print()
    print("  0. 退出")
    print()
    print("-" * 70)


async def fetch_weibo_ai():
    """获取微博AI相关热搜"""
    print("\n🕷️  正在获取微博热搜...")

    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "news_scraper",
        "00_Agent_Library/news_scraper.py"
    )
    news_scraper = importlib.util.module_from_spec(spec)

    try:
        spec.loader.exec_module(news_scraper)
        scraper = news_scraper.NewsScraper()
        results = await scraper.scrape_batch(["weibo"], limit=20)

        # 筛选AI相关
        ai_keywords = ["AI", "人工智能", "GPT", "ChatGPT", "Claude", "大模型",
                      "机器学习", "深度学习", "智能", "自动化", "科技"]

        ai_news = []
        for result in results:
            for item in result.get("news_list", []):
                title = item.get("title", "")
                if any(keyword in title for keyword in ai_keywords):
                    ai_news.append(item)

        if ai_news:
            print(f"\n✅ 找到 {len(ai_news)} 条 AI 相关热搜：\n")
            for i, news in enumerate(ai_news[:10], 1):
                print(f"{i}. {news['title']}")
                if news.get('hot'):
                    print(f"   🔥 热度: {news['hot']}")
                print()
        else:
            print("⚠️  当前热搜中没有 AI 相关内容")

    except Exception as e:
        print(f"❌ 获取失败: {e}")


async def fetch_zhihu_ai():
    """获取知乎AI技术讨论"""
    print("\n🔥 正在获取知乎热榜...")

    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "news_scraper",
        "00_Agent_Library/news_scraper.py"
    )
    news_scraper = importlib.util.module_from_spec(spec)

    try:
        spec.loader.exec_module(news_scraper)
        scraper = news_scraper.NewsScraper()
        results = await scraper.scrape_batch(["zhihu"], limit=15)

        for result in results:
            scraper.print_results([result])

    except Exception as e:
        print(f"⚠️  知乎API暂时不可用")
        print("💡 建议使用 AI 新闻聚合器或智能监控功能")


def fetch_ai_aggregator():
    """使用AI新闻聚合器"""
    print("\n🤖 正在启动 AI 新闻聚合器...\n")

    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "ai_news_aggregator",
        "00_Agent_Library/ai_news_aggregator.py"
    )
    ai_news_aggregator = importlib.util.module_from_spec(spec)

    try:
        spec.loader.exec_module(ai_news_aggregator)
        aggregator = ai_news_aggregator.AINewsAggregator()
        aggregator.run()

    except Exception as e:
        print(f"❌ 运行失败: {e}")


def fetch_ai_tools():
    """追踪AI工具更新"""
    print("\n🚀 正在追踪 AI 工具更新...\n")

    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "news_tracker",
        "01_Active_Projects/ai_news_tracker/src/news_tracker.py"
    )
    news_tracker = importlib.util.module_from_spec(spec)

    try:
        spec.loader.exec_module(news_tracker)
        tracker = news_tracker.AINewsTracker()

        # 模拟运行（非异步）
        import json
        from datetime import datetime

        print("=" * 70)
        print("🤖 AI 工具更新日报")
        print("=" * 70)
        print(f"📅 {datetime.now().strftime('%Y-%m-%d')}")
        print()

        # GitHub Trending
        print("## 🔥 GitHub 热门 AI 项目")
        trending = tracker.fetch_github_trending()
        for project in trending:
            print(f"\n- **[{project['name']}]({project['url']})**")
            print(f"  {project['description']}")
            print(f"  标签: {', '.join(project['tags'])}")

        # MCP 服务器
        print("\n## 📦 最新 MCP 服务器")
        servers = tracker.fetch_mcp_servers()
        for server in servers:
            print(f"\n- **{server['name']}** {server.get('status', '')}")
            print(f"  {server['description']}")
            print(f"  [查看]({server['url']})")

        # AI 工具
        print("\n## 🛠️ 新发布的 AI 工具")
        tools = tracker.fetch_ai_tools()
        for tool in tools[:3]:
            print(f"\n- **{tool['name']}** ({tool.get('released', 'N/A')})")
            print(f"  {tool['description']}")
            print(f"  分类: {tool.get('category', 'N/A')}")
            if 'url' in tool:
                print(f"  [链接]({tool['url']})")

        print("\n" + "=" * 70)

    except Exception as e:
        print(f"❌ 运行失败: {e}")


async def smart_monitor():
    """智能监控（学习兴趣）"""
    print("\n🧠 正在启动智能新闻监控...\n")

    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "smart_news_monitor",
        "00_Agent_Library/smart_news_monitor.py"
    )
    smart_news_monitor = importlib.util.module_from_spec(spec)

    try:
        spec.loader.exec_module(smart_news_monitor)
        monitor = smart_news_monitor.SmartNewsMonitor()

        # 显示状态
        print(monitor.get_summary())
        print()

        # 检查新闻
        await monitor.check_and_notify()

        print("\n💡 提示：您的兴趣关键词已保存，系统会持续学习")

    except Exception as e:
        print(f"❌ 运行失败: {e}")


def manage_interests():
    """管理兴趣关键词"""
    print("\n⚙️  兴趣关键词管理\n")

    import json
    from pathlib import Path

    interest_file = Path("06_Learning_Journal/workspace_memory/user_interests.json")

    if interest_file.exists():
        data = json.loads(interest_file.read_text(encoding="utf-8"))

        print("📊 当前兴趣配置：\n")
        print(f"  长期兴趣 ({len(data['long_term'])} 个):")
        print(f"    {', '.join(data['long_term'][:10])}")
        if len(data['long_term']) > 10:
            print(f"    ... 还有 {len(data['long_term']) - 10} 个")

        print(f"\n  短期关注 ({len(data['short_term'])} 个):")
        if data['short_term']:
            print(f"    {', '.join(data['short_term'])}")
        else:
            print("    （无）")

        print("\n💡 提示：这些关键词用于智能筛选新闻")
        print("   您可以通过对话中的关键词自动学习新兴趣")

    else:
        print("⚠️  兴趣配置文件不存在")
        print("   运行智能监控功能后会自动创建")


async def main():
    """主函数"""
    while True:
        print_banner()
        print_menu()

        choice = input("请选择 (0-7): ").strip()

        if choice == "0":
            print("\n👋 感谢使用！")
            break

        elif choice == "1":
            await fetch_weibo_ai()

        elif choice == "2":
            await fetch_zhihu_ai()

        elif choice == "3":
            print("\n📊 百度热搜功能开发中...")
            print("   建议使用 AI 新闻聚合器")

        elif choice == "4":
            fetch_ai_aggregator()

        elif choice == "5":
            fetch_ai_tools()

        elif choice == "6":
            await smart_monitor()

        elif choice == "7":
            manage_interests()

        else:
            print("\n❌ 无效选择，请输入 0-7")

        if choice != "0":
            input("\n按回车返回主菜单...")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 再见！")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
