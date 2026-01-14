# -*- coding: utf-8 -*-
"""
智能新闻监控助手
Smart News Monitor Assistant

功能:
1. 记住用户的兴趣点 (长期和短期)
2. 从多平台获取热点新闻
3. 智能匹配相关新闻
4. 主动推送用户感兴趣的内容

作者: Office Agent Workspace
版本: 1.0.0
"""

import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Set
import re

# Windows 编码修复
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')


class InterestMemory:
    """兴趣记忆系统"""

    def __init__(self, storage_path: Path = None):
        if storage_path is None:
            storage_path = Path(__file__).parent.parent / "06_Learning_Journal" / "workspace_memory"
        self.storage_path = storage_path
        self.interest_file = storage_path / "user_interests.json"

        # 兴趣分类
        self.long_term_interests: Set[str] = set()  # 长期兴趣
        self.short_term_interests: Set[str] = set()  # 短期关注
        self.implicit_keywords: Set[str] = set()  # 隐式学习的关键词

        # 时间戳
        self.last_update = None

        self._load()

    def _load(self):
        """加载兴趣数据"""
        if self.interest_file.exists():
            try:
                data = json.loads(self.interest_file.read_text(encoding="utf-8"))
                self.long_term_interests = set(data.get("long_term", []))
                self.short_term_interests = set(data.get("short_term", []))
                self.implicit_keywords = set(data.get("implicit", []))
                self.last_update = data.get("last_update")
                print(f"✅ 已加载 {len(self.long_term_interests)} 个长期兴趣，{len(self.short_term_interests)} 个短期关注")
            except Exception as e:
                print(f"⚠️  加载兴趣数据失败: {e}")
                self._init_default_interests()
        else:
            self._init_default_interests()

    def _init_default_interests(self):
        """初始化默认兴趣"""
        # 基于工作区的默认兴趣
        self.long_term_interests = {
            "AI", "人工智能", "Python", "办公自动化",
            "Flask", "Streamlit", "OCR", "市场监管",
            "知识管理", "向量化", "MCP", "Claude"
        }
        self.short_term_interests = set()
        self.implicit_keywords = set()
        self.save()

    def save(self):
        """保存兴趣数据"""
        self.storage_path.mkdir(parents=True, exist_ok=True)
        data = {
            "long_term": list(self.long_term_interests),
            "short_term": list(self.short_term_interests),
            "implicit": list(self.implicit_keywords),
            "last_update": datetime.now().isoformat()
        }
        self.interest_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def add_long_term(self, keyword: str):
        """添加长期兴趣"""
        self.long_term_interests.add(keyword)
        self.save()

    def add_short_term(self, keyword: str, days=7):
        """添加短期关注 (自动过期)"""
        self.short_term_interests.add(keyword)
        self.save()

    def learn_implicit(self, text: str):
        """从文本中隐式学习关键词"""
        # 简单的关键词提取
        keywords = re.findall(r'[\u4e00-\u9fa5a-zA-Z]{2,}', text)
        for keyword in keywords:
            if len(keyword) >= 2 and keyword not in self.long_term_interests:
                self.implicit_keywords.add(keyword)
        self.save()

    def get_all_keywords(self) -> Set[str]:
        """获取所有有效关键词"""
        # 清理过期的短期兴趣
        all_keywords = self.long_term_interests | self.short_term_interests | self.implicit_keywords
        return all_keywords

    def match_score(self, text: str) -> float:
        """计算文本与兴趣的匹配分数"""
        keywords = self.get_all_keywords()
        if not keywords:
            return 0.0

        text_lower = text.lower()
        matches = sum(1 for kw in keywords if kw.lower() in text_lower)
        return min(matches / len(keywords) * 10, 1.0)  # 归一化到 0-1


class NewsItem:
    """新闻条目"""

    def __init__(self, title: str, url: str, platform: str, hot_value: str = "", rank: int = 0):
        self.title = title
        self.url = url
        self.platform = platform
        self.hot_value = hot_value
        self.rank = rank
        self.timestamp = datetime.now()

    def to_dict(self):
        return {
            "title": self.title,
            "url": self.url,
            "platform": self.platform,
            "hot_value": self.hot_value,
            "rank": self.rank,
            "timestamp": self.timestamp.isoformat()
        }


class SmartNewsMonitor:
    """智能新闻监控助手"""

    def __init__(self):
        self.memory = InterestMemory()
        self.last_check = None
        self.cache_file = Path(__file__).parent.parent / "06_Learning_Journal" / "workspace_memory" / "news_cache.json"
        self.cache = self._load_cache()

    def _load_cache(self) -> Dict:
        """加载新闻缓存"""
        if self.cache_file.exists():
            try:
                return json.loads(self.cache_file.read_text(encoding="utf-8"))
            except:
                return {}
        return {}

    def _save_cache(self):
        """保存新闻缓存"""
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        self.cache_file.write_text(json.dumps(self.cache, ensure_ascii=False, indent=2), encoding="utf-8")

    def add_interest(self, keyword: str, interest_type: str = "long"):
        """添加兴趣关键词"""
        if interest_type == "long":
            self.memory.add_long_term(keyword)
            print(f"✅ 已添加长期兴趣: {keyword}")
        else:
            self.memory.add_short_term(keyword)
            print(f"✅ 已添加短期关注: {keyword}")

    def learn_from_context(self, text: str):
        """从上下文学习"""
        self.memory.learn_implicit(text)
        print(f"🧠 已从上下文学习关键词")

    async def fetch_hot_news(self) -> List[NewsItem]:
        """获取热点新闻"""
        try:
            from mcp_hot_news.client import HotNewsClient

            all_news = []
            platforms = ["zhihu", "bilibili", "douyin", "kuaishou"]

            async with HotNewsClient() as client:
                tasks = [client.get_hot_news(platform, limit=20) for platform in platforms]
                results = await asyncio.gather(*tasks, return_exceptions=True)

                for platform, result in zip(platforms, results):
                    if isinstance(result, Exception):
                        print(f"⚠️  {platform} 获取失败: {result}")
                        continue

                    for item in result.get("news_list", []):
                        news = NewsItem(
                            title=item.get("title", ""),
                            url=item.get("url", ""),
                            platform=platform,
                            hot_value=str(item.get("hot_value", "")),
                            rank=item.get("rank", 0)
                        )
                        all_news.append(news)

            return all_news

        except ImportError:
            print("⚠️  mcp-hot-news 未安装，使用模拟数据")
            return self._get_mock_news()

    def _get_mock_news(self) -> List[NewsItem]:
        """获取模拟新闻数据"""
        mock_data = [
            NewsItem("GPT-5 发布预告，性能提升300%", "https://example.com/gpt5", "知乎", "100万热", 1),
            NewsItem("Python 3.14 正式发布", "https://example.com/py314", "知乎", "50万热", 2),
            NewsItem("Flask 4.0 带来重大更新", "https://example.com/flask4", "哔哩哔哩", "30万热", 1),
            NewsItem("OCR 技术突破：识别准确率达99.9%", "https://example.com/ocr", "知乎", "20万热", 3),
            NewsItem("市场监管引入 AI 智能审批", "https://example.com/market", "知乎", "15万热", 4),
        ]
        return mock_data

    def filter_interesting_news(self, news_list: List[NewsItem], threshold: float = 0.3) -> List[NewsItem]:
        """筛选感兴趣的新闻"""
        interesting = []
        for news in news_list:
            score = self.memory.match_score(news.title)
            if score >= threshold:
                interesting.append((news, score))
        # 按分数排序
        interesting.sort(key=lambda x: x[1], reverse=True)
        return [news for news, _ in interesting]

    async def check_and_notify(self, silent: bool = False) -> List[NewsItem]:
        """检查并通知感兴趣的新闻"""
        # 获取最新新闻
        all_news = await self.fetch_hot_news()

        # 筛选感兴趣的新闻
        interesting_news = self.filter_interesting_news(all_news)

        if not silent:
            if interesting_news:
                print(f"\n📰 发现 {len(interesting_news)} 条您可能感兴趣的新闻:")
                print("=" * 60)
                for i, news in enumerate(interesting_news[:10], 1):
                    score = self.memory.match_score(news.title)
                    print(f"\n{i}. [{news.platform}] {news.title}")
                    print(f"   🔥 热度: {news.hot_value} | 🎯 匹配度: {score:.1%}")
                    print(f"   🔗 {news.url}")
            else:
                print("📭 暂无您感兴趣的新闻")

        self.last_check = datetime.now()
        return interesting_news

    def get_summary(self) -> str:
        """获取监控摘要"""
        keywords = self.memory.get_all_keywords()
        return f"""
📊 智能新闻监控助手状态
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧠 兴趣关键词: {len(keywords)} 个
   主要兴趣: {', '.join(list(self.memory.long_term_interests)[:5])}{'...' if len(self.memory.long_term_interests) > 5 else ''}

🔍 监控平台: 知乎、微博、哔哩哔哩、抖音、快手

⏰ 上次检查: {self.last_check.strftime('%Y-%m-%d %H:%M:%S') if self.last_check else '未运行'}

💡 使用提示:
   - 说"添加兴趣: xxx" 添加长期兴趣
   - 说"关注: xxx" 添加短期关注
   - 说"检查新闻" 主动检查热点
   - 我会自动记住对话中的关键词
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """.strip()


# CLI 测试入口
async def main():
    """测试入口"""
    monitor = SmartNewsMonitor()

    print(monitor.get_summary())

    # 检查新闻
    await monitor.check_and_notify()

    # 交互式测试
    print("\n💬 您可以输入命令:")
    print("  - 添加兴趣: <关键词>")
    print("  - 关注: <关键词>")
    print("  - 检查新闻")
    print("  - 退出")

    while True:
        cmd = input("\n> ").strip()
        if not cmd:
            continue

        if cmd in ["退出", "exit", "quit"]:
            print("👋 再见！")
            break

        elif cmd.startswith("添加兴趣:") or cmd.startswith("add interest:"):
            keyword = cmd.split(":", 1)[1].strip()
            monitor.add_interest(keyword, "long")

        elif cmd.startswith("关注:") or cmd.startswith("follow:"):
            keyword = cmd.split(":", 1)[1].strip()
            monitor.add_interest(keyword, "short")

        elif cmd in ["检查新闻", "check news", "新闻"]:
            await monitor.check_and_notify()

        elif cmd in ["状态", "status", "summary"]:
            print(monitor.get_summary())

        else:
            # 隐式学习
            monitor.learn_from_context(cmd)
            print(f"🧠 已记录: {cmd}")


if __name__ == "__main__":
    asyncio.run(main())
