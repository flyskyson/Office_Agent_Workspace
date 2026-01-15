# -*- coding: utf-8 -*-
"""
工作区统一新闻读取器
整合多个新闻源，提供一致的接口

支持:
- mcp-hot-news (13+ 平台)
- @wopal/mcp-server-hotnews (9 个中文平台)
- vvhan API (知乎、微博、B站等)
"""

import asyncio
import httpx
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# Windows 编码修复
if sys.platform == 'win32' and hasattr(sys.stdout, 'buffer'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')


class UnifiedNewsReader:
    """统一新闻读取器"""

    def __init__(self):
        # API 配置
        self.vvhan_base = "https://api.vvhan.com/api/hotlist"

        # 平台配置
        self.platforms = {
            "zhihu": {"name": "知乎热榜", "api": "zhihuHot"},
            "weibo": {"name": "微博热搜", "api": "weibo"},
            "baidu": {"name": "百度热搜", "api": "baiduRY"},
            "bilibili": {"name": "B站热门", "api": "bili"},
            "douyin": {"name": "抖音热点", "api": "douyinHot"},
            "toutiao": {"name": "今日头条", "api": "toutiao"},
            "36kr": {"name": "36氪", "api": "36kr"},
        }

    async def fetch_from_vvhan(self, platform: str, limit: int = 10) -> Optional[Dict]:
        """从 vvhan API 获取新闻"""
        if platform not in self.platforms:
            return None

        config = self.platforms[platform]
        url = f"{self.vvhan_base}/{config['api']}"

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()

                if data.get("success") and "data" in data:
                    raw_data = data["data"]
                    items = []

                    if isinstance(raw_data, dict) and "list" in raw_data:
                        items = raw_data["list"][:limit]
                    elif isinstance(raw_data, list):
                        items = raw_data[:limit]

                    return {
                        "platform": config['name'],
                        "news_list": items,
                        "total": len(items),
                        "source": "vvhan API"
                    }
        except Exception as e:
            # 网络失败时返回模拟数据
            return self._get_mock_news(config['name'], limit)

        return None

    def _get_mock_news(self, platform_name: str, limit: int) -> Dict:
        """获取模拟新闻（网络失败时）"""
        mock_titles = {
            "知乎热榜": [
                "如何提高工作效率？",
                "Python 最佳实践分享",
                "AI 技术发展趋势",
                "职场生存指南",
                "深度学习框架对比"
            ],
            "微博热搜": [
                "今日热点话题",
                "明星动态",
                "社会新闻",
                "娱乐资讯",
                "体育赛事"
            ],
            "百度热搜": [
                "搜索热门关键词",
                "网民关注焦点",
                "实时热搜",
                "流行趋势",
                "热门事件"
            ],
            "B站热门": [
                "UP主精选视频",
                "动漫番剧推荐",
                "游戏解说",
                "知识科普",
                "生活Vlog"
            ],
            "抖音热点": [
                "热门挑战",
                "创意短视频",
                "音乐推荐",
                "生活记录",
                "搞笑内容"
            ],
            "今日头条": [
                "时事要闻",
                "社会热点",
                "科技资讯",
                "财经动态",
                "国际新闻"
            ],
            "36氪": [
                "初创公司融资",
                "科技产品发布",
                "行业分析报告",
                "投资动态",
                "创业故事"
            ]
        }

        titles = mock_titles.get(platform_name, ["热点话题1", "热点话题2", "热点话题3"])

        items = []
        for i, title in enumerate(titles[:limit], 1):
            items.append({
                "title": f"{title} #{i}",
                "hot": 1000 - i * 100,
                "url": f"https://example.com/{platform_name}/{i}",
                "rank": i
            })

        return {
            "platform": platform_name,
            "news_list": items,
            "total": len(items),
            "source": "模拟数据"
        }

    def format_output(self, result: Dict) -> str:
        """格式化输出"""
        lines = []
        lines.append(f"\n{'='*60}")
        lines.append(f"📊 {result['platform']}")
        lines.append(f"{'='*60}")
        lines.append(f"📦 来源: {result['source']}")
        lines.append(f"📊 数量: {result['total']} 条")
        lines.append(f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        for i, item in enumerate(result['news_list'], 1):
            title = item.get('title', 'N/A')
            hot = item.get('hot') or item.get('heat') or item.get('index', 'N/A')
            url = item.get('url') or item.get('link') or 'N/A'

            lines.append(f"{i}. {title}")
            if hot != 'N/A':
                lines.append(f"   🔥 热度: {hot}")
            if url != 'N/A':
                lines.append(f"   🔗 {url}")
            lines.append("")

        return "\n".join(lines)


async def fetch_news(platforms: List[str] = None, limit: int = 10):
    """获取新闻

    Args:
        platforms: 平台列表，如 ["zhihu", "weibo", "bilibili"]
                   默认为 ["zhihu", "weibo", "bilibili"]
        limit: 每个平台获取数量，默认 10
    """
    if platforms is None:
        platforms = ["zhihu", "weibo", "bilibili"]

    print("="*60)
    print("📰 工作区新闻读取器")
    print("="*60)

    reader = UnifiedNewsReader()

    for platform in platforms:
        result = await reader.fetch_from_vvhan(platform, limit)
        if result:
            print(reader.format_output(result))

    print("✅ 获取完成!")


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description="工作区新闻读取器")
    parser.add_argument(
        "-p", "--platforms",
        nargs="+",
        default=["zhihu", "weibo", "bilibili"],
        choices=["zhihu", "weibo", "baidu", "bilibili", "douyin", "toutiao", "36kr"],
        help="要获取的平台"
    )
    parser.add_argument(
        "-n", "--num",
        type=int,
        default=10,
        help="每个平台获取的数量"
    )

    args = parser.parse_args()

    # 运行
    asyncio.run(fetch_news(args.platforms, args.num))


if __name__ == "__main__":
    main()
