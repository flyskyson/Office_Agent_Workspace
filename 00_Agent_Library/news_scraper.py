# -*- coding: utf-8 -*-
"""
使用 Playwright 直接爬取热榜数据
绕过 API，直接获取网页数据

支持平台：
- 微博热搜（已验证）
- 知乎热榜
- 百度热搜
"""
import asyncio
import sys
from datetime import datetime
from playwright.async_api import async_playwright
from typing import Dict, List, Optional

# Windows 编码修复
if sys.platform == 'win32' and hasattr(sys.stdout, 'buffer'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')


class NewsScraper:
    """使用 Playwright 爬取热榜"""

    def __init__(self):
        self.supported_platforms = {
            "weibo": {"name": "微博热搜", "func": "scrape_weibo"},
            "zhihu": {"name": "知乎热榜", "func": "scrape_zhihu"},
            "baidu": {"name": "百度热搜", "func": "scrape_baidu"},
        }

    async def scrape_zhihu(self, page, limit=10):
        """爬取知乎热榜"""
        try:
            # 使用移动端页面，无需登录
            await page.goto("https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=10", timeout=15000)

            # 等待响应
            await page.wait_for_load_state("networkidle", timeout=10000)

            # 获取 JSON 数据
            data = await page.evaluate("() => JSON.parse(document.body.innerText)")

            items = []
            if data and "data" in data:
                for i, item in enumerate(data["data"][:limit], 1):
                    target = item.get("target", {})
                    title = target.get("title", "")
                    url = target.get("url", "")
                    hot = target.get("hot_number", "")

                    # 格式化热度
                    if hot:
                        hot_num = int(hot)
                        if hot_num > 10000:
                            hot = f"{hot_num / 10000:.1f}万"

                    items.append({
                        "title": title.strip(),
                        "url": url,
                        "hot": str(hot) if hot else "",
                        "rank": i
                    })

            return {
                "platform": "知乎热榜",
                "news_list": items,
                "total": len(items),
                "source": "API 爬取"
            }

        except Exception as e:
            print(f"   ⚠️ 知乎爬取失败: {e}")
            return None

    async def scrape_weibo(self, page, limit=10):
        """爬取微博热搜"""
        try:
            await page.goto("https://s.weibo.com/top/summary", timeout=15000)
            await page.wait_for_selector("#pl_top_realtimehot table", timeout=10000)

            items = []
            rows = await page.query_selector_all("#pl_top_realtimehot table tbody tr")

            for i, row in enumerate(rows[:limit], 1):
                # 标题
                title_el = await row.query_selector("td:nth-child(2) > a")
                if title_el:
                    title = await title_el.inner_text()
                    link = await page.evaluate("(el) => el.href", title_el)

                    # 热度
                    hot_el = await row.query_selector("td:nth-child(2) > span")
                    hot = ""
                    if hot_el:
                        hot = await hot_el.inner_text()

                    items.append({
                        "title": title.strip(),
                        "url": link,
                        "hot": hot.strip() if hot else "",
                        "rank": i
                    })

            return {
                "platform": "微博热搜",
                "news_list": items,
                "total": len(items),
                "source": "网页爬取"
            }

        except Exception as e:
            print(f"   ⚠️ 微博爬取失败: {e}")
            return None

    async def scrape_baidu(self, page, limit=10):
        """爬取百度热搜"""
        try:
            await page.goto("https://top.baidu.com/board?tab=realtime", timeout=15000)
            await page.wait_for_selector(".c-single-text-ellipsis", timeout=10000)

            items = []
            elements = await page.query_selector_all(".category-wrap_iQLoo.vertical_3uCeJ_0")

            for i, el in enumerate(elements[:limit], 1):
                # 标题
                title_el = await el.query_selector(".c-single-text-ellipsis")
                if title_el:
                    title = await title_el.inner_text()

                    # 链接和热度
                    link_el = await el.query_selector("a")
                    link = ""
                    if link_el:
                        link = await page.evaluate("(el) => el.href", link_el)

                    hot_el = await el.query_selector(".hot-index_1Bl1a")
                    hot = ""
                    if hot_el:
                        hot = await hot_el.inner_text()

                    items.append({
                        "title": title.strip(),
                        "url": link,
                        "hot": hot.strip() if hot else "",
                        "rank": i
                    })

            return {
                "platform": "百度热搜",
                "news_list": items,
                "total": len(items),
                "source": "网页爬取"
            }

        except Exception as e:
            print(f"   ⚠️ 百度爬取失败: {e}")
            return None

    def format_output(self, result):
        """格式化输出"""
        if not result:
            return ""

        lines = []
        lines.append(f"\n{'='*60}")
        lines.append(f"📊 {result['platform']}")
        lines.append(f"{'='*60}")
        lines.append(f"📦 来源: {result['source']}")
        lines.append(f"📊 数量: {result['total']} 条")
        lines.append(f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        for item in result['news_list']:
            title = item.get('title', 'N/A')
            hot = item.get('hot', '')
            url = item.get('url', '')

            lines.append(f"{item['rank']}. {title}")
            if hot:
                lines.append(f"   🔥 热度: {hot}")
            if url:
                lines.append(f"   🔗 {url}")
            lines.append("")

        return "\n".join(lines)


    async def scrape_batch(self, platforms: List[str], limit: int = 10) -> List[Dict]:
        """批量爬取多个平台

        Args:
            platforms: 平台列表，如 ["weibo", "zhihu", "baidu"]
            limit: 每个平台获取数量

        Returns:
            所有平台的结果列表
        """
        results = []

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            for platform in platforms:
                if platform not in self.supported_platforms:
                    print(f"⚠️ 不支持的平台: {platform}")
                    continue

                platform_info = self.supported_platforms[platform]
                func_name = platform_info["func"]

                print(f"📰 正在爬取 {platform_info['name']}...")

                # 动态调用对应的方法
                scrape_func = getattr(self, func_name)
                result = await scrape_func(page, limit=limit)

                if result:
                    results.append(result)
                    print(f"   ✅ 成功获取 {result['total']} 条")
                else:
                    print(f"   ❌ 爬取失败")

            await browser.close()

        return results

    def print_results(self, results: List[Dict]):
        """打印所有结果"""
        for result in results:
            print(self.format_output(result))


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description="热榜爬取器 (Playwright)")
    parser.add_argument(
        "-p", "--platforms",
        nargs="+",
        default=["weibo"],
        choices=["weibo", "zhihu", "baidu"],
        help="要爬取的平台"
    )
    parser.add_argument(
        "-n", "--num",
        type=int,
        default=10,
        help="每个平台获取的数量"
    )

    args = parser.parse_args()

    # 运行
    async def run():
        print("="*60)
        print("🔍 热榜爬取器 (Playwright)")
        print("="*60)
        print()

        scraper = NewsScraper()
        results = await scraper.scrape_batch(args.platforms, args.num)
        scraper.print_results(results)

        print("\n✅ 完成!")

    asyncio.run(run())


if __name__ == "__main__":
    main()
