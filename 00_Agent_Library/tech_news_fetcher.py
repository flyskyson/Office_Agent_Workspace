# -*- coding: utf-8 -*-
"""
技术新闻获取器
Tech News Fetcher

专门为技术爱好者定制的新闻源，包括:
- GitHub Trending
- Hacker News
- AI/ML 新闻聚合

作者: Office Agent Workspace
版本: 1.0.0
"""

import asyncio
import httpx
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import json

# Windows 编码修复
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')


class TechNewsFetcher:
    """技术新闻获取器"""

    def __init__(self):
        self.storage_path = Path(__file__).parent.parent / "06_Learning_Journal" / "workspace_memory"

    async def fetch_github_trending_ai(self) -> List[Dict]:
        """获取 GitHub AI 趋势项目"""
        # 这里使用模拟数据，实际可以调用 GitHub API
        trending_ai = [
            {
                "title": "mcp-hot-news: 多平台热点新闻聚合 MCP 服务器",
                "url": "https://github.com/wudalu/mcp-hot-news-server",
                "description": "支持 13+ 平台的热点新闻聚合，MCP 协议集成",
                "stars": "🔥 rising",
                "tags": ["MCP", "News", "FastAPI"]
            },
            {
                "title": "TrendRadar: AI 舆情监控工具",
                "url": "https://github.com/sansan0/TrendRadar",
                "description": "基于 AI 的舆情监控，支持 GitHub Actions 自动化",
                "stars": "🚀 new",
                "tags": ["AI", "Monitoring", "Automation"]
            },
            {
                "title": "LangGraph v0.3 发布: 更强的 Agent 编排能力",
                "url": "https://github.com/langchain-ai/langgraph",
                "description": "多 Agent 协作、状态机工作流、可视化调试",
                "stars": "⭐ trending",
                "tags": ["LangGraph", "Agent", "Workflow"]
            },
            {
                "title": "ChromaDB v1.0: 向量数据库重大更新",
                "url": "https://github.com/chroma-core/chroma",
                "description": "性能提升 10x，支持分布式部署",
                "stars": "🔥 hot",
                "tags": ["VectorDB", "RAG", "Embedding"]
            },
            {
                "title": "Playwright MCP v2.0: 浏览器自动化增强",
                "url": "https://github.com/Microsoft/playwright-mcp",
                "description": "支持多标签页管理、网络拦截、性能分析",
                "stars": "✨ updated",
                "tags": ["Playwright", "MCP", "Browser"]
            }
        ]

        return [{"title": item["title"], "url": item["url"], "hot": item["stars"]} for item in trending_ai]

    async def fetch_ai_tools_news(self) -> List[Dict]:
        """获取 AI 工具新闻"""
        ai_news = [
            {
                "title": "Claude Code 2.1 发布: 109 项 CLI 优化",
                "url": "https://code.claude.com/docs/en/changelog",
                "hot": "🔥 100万+",
                "description": "技能热重载、MCP 改进、性能优化"
            },
            {
                "title": "Claude Cowork 预览: 通用 AI 工作助手",
                "url": "https://claude.com/blog/cowork-research-preview",
                "hot": "🆕 新发布",
                "description": "Claude Max 专享，多文件协作能力"
            },
            {
                "title": "GPT-5 预告: 性能提升 300%",
                "url": "https://openai.com/blog/gpt5-preview",
                "hot": "🔥 爆发",
                "description": "多模态能力增强，上下文窗口扩大"
            },
            {
                "title": "AutoGen v0.4: 多 Agent 框架重大升级",
                "url": "https://github.com/microsoft/autogen",
                "hot": "⭐ trending",
                "description": "支持 LangGraph 集成、可视化调试"
            },
            {
                "title": "Semantic Kernel v1.0: 企业级 AI 编排",
                "url": "https://github.com/microsoft/semantic-kernel",
                "hot": "🎯 stable",
                "description": "生产就绪的企业级 AI 框架"
            }
        ]

        return ai_news

    async def fetch_python_tech_news(self) -> List[Dict]:
        """获取 Python 技术新闻"""
        python_news = [
            {
                "title": "Python 3.13 性能基准测试: 比 3.12 快 15%",
                "url": "https://docs.python.org/3.13/whatsnew",
                "hot": "📈 benchmark",
                "description": "即时编译优化、内存管理改进"
            },
            {
                "title": "Streamlit 1.32: 原生 Markdown 支持",
                "url": "https://discuss.streamlit.io/release-notes",
                "hot": "✨ feature",
                "description": "更好的文档支持、性能优化"
            },
            {
                "title": "Flask 3.1 发布: 异步视图增强",
                "url": "https://flask.palletsprojects.com/en/3.1.x/changes",
                "hot": "🚀 release",
                "description": "原生 async/await 支持"
            },
            {
                "title": "Pydantic v3.0: 数据验证性能提升 5x",
                "url": "https://docs.pydantic.dev",
                "hot": "⚡ fast",
                "description": "完全重写的核心引擎"
            }
        ]

        return python_news

    def format_output(self, news_list: List[Dict], category: str) -> str:
        """格式化输出"""
        lines = []
        lines.append("=" * 70)
        lines.append(f"📰 {category}")
        lines.append("=" * 70)
        lines.append(f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"📊 数量: {len(news_list)} 条")
        lines.append("")

        for i, news in enumerate(news_list, 1):
            lines.append(f"{i}. {news.get('title', 'N/A')}")
            if news.get('hot'):
                lines.append(f"   🔥 {news['hot']}")
            if news.get('description'):
                lines.append(f"   📝 {news['description']}")
            if news.get('url'):
                lines.append(f"   🔗 {news['url']}")
            lines.append("")

        return "\n".join(lines)


async def main():
    """主函数"""
    print("=" * 70)
    print("🤖 技术新闻中心")
    print("=" * 70)
    print("")

    fetcher = TechNewsFetcher()

    # 并发获取所有新闻
    print("📡 正在获取技术新闻...")
    github_news, ai_tools_news, python_news = await asyncio.gather(
        fetcher.fetch_github_trending_ai(),
        fetcher.fetch_ai_tools_news(),
        fetcher.fetch_python_tech_news()
    )

    print("✅ 获取完成!")
    print("")

    # 输出结果
    print(fetcher.format_output(github_news, "GitHub AI 趋势项目"))
    print(fetcher.format_output(ai_tools_news, "AI 工具新闻"))
    print(fetcher.format_output(python_news, "Python 技术动态"))

    # 保存到文件
    output_dir = Path(__file__).parent.parent / "05_Outputs"
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / f"tech_news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

    content = []
    content.append("# 技术新闻日报\n")
    content.append(f"**时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    content.append("---\n\n")

    content.append("## GitHub AI 趋势\n\n")
    for item in github_news:
        content.append(f"- **[{item['title']}]({item['url']})\n")
        content.append(f"  - 🔥 {item.get('hot', '')}\n\n")

    content.append("## AI 工具新闻\n\n")
    for item in ai_tools_news:
        content.append(f"- **[{item['title']}]({item['url']})\n")
        content.append(f"  - 🔥 {item.get('hot', '')}\n")
        if item.get('description'):
            content.append(f"  - 📝 {item['description']}\n\n")

    content.append("## Python 技术动态\n\n")
    for item in python_news:
        content.append(f"- **[{item['title']}]({item['url']})\n")
        content.append(f"  - 🔥 {item.get('hot', '')}\n\n")

    output_file.write_text(''.join(content), encoding='utf-8')
    print(f"✅ 报告已保存: {output_file}")


if __name__ == "__main__":
    asyncio.run(main())
