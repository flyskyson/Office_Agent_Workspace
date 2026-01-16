# -*- coding: utf-8 -*-
"""
智能新闻助手 v2.0
Smart News Assistant

功能:
1. 从多个平台获取真实新闻（支持 MCP 服务器）
2. 基于用户兴趣关键词进行智能匹配
3. 自动保存推荐历史

作者: Office Agent Workspace
版本: 2.0.0
更新: 2026-01-16 - 集成 MCP 新闻客户端
"""

import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set, Tuple
import subprocess
import re

# Windows 编码修复
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

# 添加 Agent Library 到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "00_Agent_Library"))


class InterestMatcher:
    """兴趣匹配器"""

    def __init__(self, interests_path: Path = None):
        if interests_path is None:
            interests_path = Path(__file__).parent.parent / "06_Learning_Journal" / "workspace_memory" / "user_interests.json"

        self.interests_path = interests_path
        self.long_term: Set[str] = set()
        self.short_term: Set[str] = set()
        self.implicit: Set[str] = set()

        self._load_interests()

    def _load_interests(self):
        """加载兴趣关键词"""
        if self.interests_path.exists():
            try:
                data = json.loads(self.interests_path.read_text(encoding="utf-8"))
                self.long_term = set(data.get("long_term", []))
                self.short_term = set(data.get("short_term", []))
                self.implicit = set(data.get("implicit", []))
                print(f"✅ 已加载 {len(self.long_term)} 个长期兴趣，{len(self.short_term)} 个短期关注")
            except Exception as e:
                print(f"⚠️  加载兴趣失败: {e}")

    def calculate_match_score(self, title: str) -> Tuple[float, List[str]]:
        """计算匹配度分数

        Returns:
            (分数, 匹配的关键词列表)
        """
        title_lower = title.lower()
        matched_keywords = []
        score = 0.0

        # 短期关注权重最高 (3.0)
        for keyword in self.short_term:
            if keyword.lower() in title_lower:
                score += 3.0
                matched_keywords.append(f"[短]{keyword}")

        # 长期兴趣次之 (1.0)
        for keyword in self.long_term:
            if keyword.lower() in title_lower:
                score += 1.0
                matched_keywords.append(f"[长]{keyword}")

        # 隐式学习的关键词 (0.5)
        for keyword in self.implicit:
            if keyword.lower() in title_lower:
                score += 0.5
                matched_keywords.append(f"[隐]{keyword}")

        return min(score, 100.0), matched_keywords


class SmartNewsAssistant:
    """智能新闻助手 v2.0 - 集成 MCP 客户端"""

    def __init__(self, use_mcp: bool = True):
        """
        初始化助手

        Args:
            use_mcp: 是否使用 MCP 客户端（默认 True）
        """
        self.matcher = InterestMatcher()
        self.storage_path = Path(__file__).parent.parent / "06_Learning_Journal" / "workspace_memory"
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.history_file = self.storage_path / "news_recommendations.jsonl"
        self.use_mcp = use_mcp

        # 延迟导入 MCP 客户端
        if use_mcp:
            try:
                from mcp_news_client import MCPNewsClient
                self.mcp_client = MCPNewsClient()
                print("✅ MCP 客户端已加载")
            except ImportError:
                print("⚠️  MCP 客户端不可用，将使用备用方案")
                self.use_mcp = False
                self.mcp_client = None

    async def fetch_from_mcp(self, platforms: List[str] = None, limit: int = 20) -> List[Dict]:
        """
        使用 MCP 客户端获取新闻

        Args:
            platforms: 平台列表（如 ["zhihu", "weibo", "github"]）
            limit: 每个平台获取数量

        Returns:
            所有平台的新闻列表
        """
        if not self.use_mcp or not self.mcp_client:
            return []

        if platforms is None:
            # 技术平台默认
            platforms = ["zhihu", "github", "csdn", "36kr"]

        try:
            results = await self.mcp_client.get_news(platforms, limit)

            # 合并所有平台的新闻
            all_news = []
            for platform, data in results.get("platforms", {}).items():
                for item in data.get("news_list", []):
                    item["source_platform"] = platform
                    all_news.append(item)

            return all_news

        except Exception as e:
            print(f"⚠️  MCP 获取失败: {e}")
            return []

    async def fetch_from_scraper(self, platform: str = "weibo", limit: int = 20) -> List[Dict]:
        """
        使用 Playwright 爬虫获取新闻（备用方案）

        Args:
            platform: 新闻平台
            limit: 获取数量
        """
        scraper_path = Path(__file__).parent / "news_scraper.py"

        if not scraper_path.exists():
            print(f"⚠️  爬虫文件不存在: {scraper_path}")
            return []

        try:
            # 调用爬虫脚本
            result = subprocess.run(
                [sys.executable, str(scraper_path), "-p", platform, "-n", str(limit)],
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=60
            )

            if result.returncode == 0:
                # 解析输出（简化处理）
                news_items = []
                lines = result.stdout.split('\n')

                current_item = {}
                for line in lines:
                    # 解析格式: "1. 标题"
                    match = re.match(r'^\s*(\d+)\.\s+(.+)', line)
                    if match:
                        if current_item:
                            news_items.append(current_item)
                        current_item = {"title": match.group(2), "rank": int(match.group(1))}

                    # 解析热度
                    hot_match = re.search(r'🔥\s*热度:\s*([\d,]+)', line)
                    if hot_match and current_item:
                        current_item["hot"] = hot_match.group(1)

                    # 解析链接
                    url_match = re.search(r'🔗\s*(https?://\S+)', line)
                    if url_match and current_item:
                        current_item["url"] = url_match.group(1)

                if current_item:
                    news_items.append(current_item)

                return news_items
        except Exception as e:
            print(f"⚠️  爬虫获取失败: {e}")

        return []

    def match_news(self, news_list: List[Dict], threshold: float = 1.0) -> List[Dict]:
        """匹配用户感兴趣的新闻

        Args:
            news_list: 新闻列表
            threshold: 最低匹配分数阈值

        Returns:
            包含匹配度分数的新闻列表
        """
        matched = []

        for news in news_list:
            title = news.get('title', '')
            score, keywords = self.matcher.calculate_match_score(title)

            if score >= threshold:
                news_with_score = news.copy()
                news_with_score['match_score'] = round(score, 1)
                news_with_score['matched_keywords'] = keywords
                matched.append(news_with_score)

        # 按匹配度排序
        matched.sort(key=lambda x: x['match_score'], reverse=True)
        return matched

    def format_recommendations(self, news_list: List[Dict]) -> str:
        """格式化推荐输出"""
        lines = []
        lines.append("=" * 70)
        lines.append("📰 智能新闻推荐")
        lines.append("=" * 70)
        lines.append(f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"📊 找到 {len(news_list)} 条您可能感兴趣的新闻")
        lines.append("")

        if not news_list:
            lines.append("😔 暂无匹配的新闻")
            lines.append("")
            lines.append("💡 建议:")
            lines.append("   - 当前热搜可能与您的兴趣领域不匹配")
            lines.append("   - 可以尝试添加更多兴趣关键词")
            lines.append("   - 或者查看技术类平台（知乎、GitHub）")
            return "\n".join(lines)

        # 按匹配度分组
        high_match = [n for n in news_list if n['match_score'] >= 3.0]
        medium_match = [n for n in news_list if 1.0 <= n['match_score'] < 3.0]

        if high_match:
            lines.append("🔥 高度匹配推荐")
            lines.append("-" * 70)
            for i, news in enumerate(high_match[:5], 1):
                lines.append(f"{i}. {news.get('title', 'N/A')}")
                lines.append(f"   🎯 匹配度: {news['match_score']}%")
                if news.get('matched_keywords'):
                    lines.append(f"   🔑 关键词: {', '.join(news['matched_keywords'][:3])}")
                if news.get('hot'):
                    lines.append(f"   🔥 热度: {news['hot']}")
                if news.get('url'):
                    lines.append(f"   🔗 {news['url']}")
                lines.append("")

        if medium_match and len(medium_match) > len(high_match):
            lines.append("💡 可能感兴趣")
            lines.append("-" * 70)
            for i, news in enumerate(medium_match[:5], 1):
                lines.append(f"{i}. {news.get('title', 'N/A')}")
                lines.append(f"   🎯 匹配度: {news['match_score']}%")
                if news.get('url'):
                    lines.append(f"   🔗 {news['url']}")
                lines.append("")

        return "\n".join(lines)

    def save_recommendation(self, news_list: List[Dict]):
        """保存推荐历史"""
        try:
            record = {
                "timestamp": datetime.now().isoformat(),
                "count": len(news_list),
                "news": news_list[:10]  # 只保存前10条
            }

            with open(self.history_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(record, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"⚠️  保存历史失败: {e}")

    async def run(self, platforms: List[str] = None, limit: int = 20, mode: str = "auto"):
        """
        运行智能推荐

        Args:
            platforms: 平台列表（多平台模式）或单个平台名称（兼容旧版）
            limit: 获取数量
            mode: 运行模式
                - "auto": 自动选择（优先 MCP，降级到爬虫）
                - "mcp": 强制使用 MCP
                - "scraper": 强制使用爬虫
        """
        print("=" * 70)
        print("🤖 智能新闻助手 v2.0")
        print("=" * 70)

        # 兼容旧版单平台模式
        if isinstance(platforms, str):
            platforms = [platforms]

        if platforms is None:
            platforms = ["zhihu", "github", "csdn"]

        print(f"📍 平台: {', '.join(platforms)}")
        print(f"📊 数量: {limit}")
        print(f"🔧 模式: {mode} (MCP: {'启用' if self.use_mcp else '禁用'})")
        print("")

        # 1. 获取新闻
        news_list = []

        if mode == "scraper" or not self.use_mcp:
            # 爬虫模式
            for platform in platforms:
                print(f"📡 正在获取 {platform} 热点...")
                items = await self.fetch_from_scraper(platform, limit)
                news_list.extend(items)
        else:
            # MCP 模式
            print(f"📡 正在从 MCP 获取新闻...")
            news_list = await self.fetch_from_mcp(platforms, limit)

        if not news_list:
            print("❌ 获取新闻失败")
            return

        print(f"✅ 获取到 {len(news_list)} 条新闻")
        print("")

        # 2. 匹配兴趣
        print("🧠 正在分析您的兴趣...")
        matched_news = self.match_news(news_list)
        print("")

        # 3. 显示推荐
        print(self.format_recommendations(matched_news))

        # 4. 保存历史
        self.save_recommendation(matched_news)

        return matched_news


async def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(
        description="智能新闻助手 v2.0 - 集成 MCP 客户端",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 使用 MCP 获取多平台新闻（推荐）
  python smart_news_assistant.py -p zhihu github csdn

  # 使用爬虫模式
  python smart_news_assistant.py -p weibo -m scraper

  # 获取技术新闻
  python smart_news_assistant.py -p zhihu github 36kr -n 30
        """
    )

    parser.add_argument(
        "-p", "--platforms",
        nargs="+",
        default=["zhihu", "github", "csdn"],
        help="新闻平台列表（默认: zhihu github csdn）"
    )
    parser.add_argument(
        "-n", "--num",
        type=int,
        default=20,
        help="每个平台获取数量 (默认: 20)"
    )
    parser.add_argument(
        "-m", "--mode",
        choices=["auto", "mcp", "scraper"],
        default="auto",
        help="运行模式 (默认: auto)"
    )

    args = parser.parse_args()

    assistant = SmartNewsAssistant(use_mcp=(args.mode != "scraper"))
    await assistant.run(args.platforms, args.num, args.mode)


if __name__ == "__main__":
    asyncio.run(main())
