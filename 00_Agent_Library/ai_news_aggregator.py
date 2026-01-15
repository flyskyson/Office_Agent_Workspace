# -*- coding: utf-8 -*-
"""
AI 技术新闻聚合器
AI Tech News Aggregator

专门聚合 AI、机器学习、深度学习、大模型等技术新闻
"""
import asyncio
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import json

# Windows 编码修复
if sys.platform == 'win32' and hasattr(sys.stdout, 'buffer'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')


class AINewsAggregator:
    """AI 技术新闻聚合器"""

    def __init__(self):
        # AI 技术关键词分类
        self.ai_keywords = {
            "大模型": ["GPT", "ChatGPT", "Claude", "GLM", "智谱", "文心一言", "通义千问"],
            "深度学习": ["Transformer", "神经网络", "PyTorch", "TensorFlow"],
            "AI Agent": ["Agent", "智能体", "AutoGen", "LangChain", "CrewAI"],
            "MCP": ["MCP服务器", "Model Context Protocol"],
            "RAG": ["RAG", "向量检索", "Embedding", "ChromaDB"],
            "开发工具": ["OpenAI", "Anthropic", "HuggingFace", "GitHub Copilot"]
        }

        # 模拟的 AI 技术新闻数据
        self.ai_news_sources = [
            {
                "source": "GitHub Trending",
                "news": [
                    {
                        "title": "OpenAI 发布 GPT-5 预览版，性能提升 300%",
                        "category": "大模型",
                        "url": "https://github.com/OpenAI/gpt-5",
                        "stars": "🔥 50k+",
                        "description": "新一代语言模型，支持多模态输入输出"
                    },
                    {
                        "title": "LangChain v0.3 发布：RAG 应用开发更简单",
                        "category": "AI Agent",
                        "url": "https://github.com/langchain-ai/langchain",
                        "stars": "🔥 90k+",
                        "description": "全新的 RAG 组件和 Agent 编排功能"
                    },
                    {
                        "title": "AutoGen 2.0：多智能体协作框架",
                        "category": "AI Agent",
                        "url": "https://github.com/microsoft/autogen",
                        "stars": "🔥 30k+",
                        "description": "支持代码执行、工具调用、人机协作"
                    }
                ]
            },
            {
                "source": "HuggingFace",
                "news": [
                    {
                        "title": "Llama 4 开源：700亿参数超越 GPT-4",
                        "category": "大模型",
                        "url": "https://huggingface.co/meta-llama/Llama-4",
                        "downloads": "📥 10M+",
                        "description": "Meta 最新开源大模型，性能卓越"
                    },
                    {
                        "title": "BGE-M4 嵌入模型：中文语义理解新高度",
                        "category": "RAG",
                        "url": "https://huggingface.co/BAAI/bge-m4",
                        "downloads": "📥 5M+",
                        "description": "智谱研究院最新嵌入模型"
                    }
                ]
            },
            {
                "source": "AI 工具更新",
                "news": [
                    {
                        "title": "Claude Code 2.1 技能热重载功能",
                        "category": "开发工具",
                        "url": "https://code.claude.com/docs/en/changelog",
                        "description": "支持技能热重载、109 项 CLI 优化"
                    },
                    {
                        "title": "MCP 生态系统爆发：50+ 服务器可用",
                        "category": "MCP",
                        "url": "https://modelcontextprotocol.io",
                        "description": "浏览器、数据库、文件系统全覆盖"
                    },
                    {
                        "title": "ChromaDB v1.0：向量数据库生产就绪",
                        "category": "RAG",
                        "url": "https://docs.trychroma.com",
                        "description": "性能提升 10x，支持分布式部署"
                    }
                ]
            }
        ]

    def categorize_news(self, title: str) -> List[str]:
        """根据标题分类新闻"""
        categories = []
        for category, keywords in self.ai_keywords.items():
            for keyword in keywords:
                if keyword.lower() in title.lower():
                    categories.append(category)
                    break
        return categories if categories else ["其他"]

    def filter_ai_news(self, news_list: List[Dict]) -> List[Dict]:
        """筛选 AI 相关新闻"""
        ai_news = []
        for source_obj in news_list:
            for news in source_obj["news"]:
                categories = self.categorize_news(news["title"])
                if categories != ["其他"]:
                    news["source"] = source_obj["source"]
                    news["categories"] = categories
                    ai_news.append(news)
        return ai_news

    def format_news_report(self, ai_news: List[Dict]) -> str:
        """格式化新闻报告"""
        lines = []
        lines.append("=" * 80)
        lines.append("🤖 AI 技术新闻日报")
        lines.append("=" * 80)
        lines.append(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"📊 共找到 {len(ai_news)} 条 AI 技术相关新闻")
        lines.append("")

        # 按分类分组
        by_category = {}
        for news in ai_news:
            for category in news["categories"]:
                if category not in by_category:
                    by_category[category] = []
                by_category[category].append(news)

        # 输出各分类新闻
        for category, news_list in by_category.items():
            lines.append(f"## 📂 {category}")
            lines.append("-" * 80)
            for i, news in enumerate(news_list, 1):
                lines.append(f"\n{i}. **{news['title']}**")
                lines.append(f"   📦 来源: {news['source']}")

                if "stars" in news:
                    lines.append(f"   ⭐ Stars: {news['stars']}")
                if "downloads" in news:
                    lines.append(f"   📥 下载: {news['downloads']}")

                if "description" in news:
                    lines.append(f"   📝 {news['description']}")

                lines.append(f"   🔗 {news['url']}")
                lines.append("")

        lines.append("=" * 80)
        lines.append("💡 提示: 这些新闻基于您的兴趣自动筛选")
        lines.append(f"🔍 追踪关键词: {', '.join(self.ai_keywords.keys())}")
        lines.append("=" * 80)

        return "\n".join(lines)

    def save_report(self, report: str, filename: str = None):
        """保存报告"""
        if filename is None:
            filename = f"ai_news_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        output_dir = Path(__file__).parent.parent / "05_Outputs" / "ai_news"
        output_dir.mkdir(parents=True, exist_ok=True)

        output_path = output_dir / filename
        output_path.write_text(report, encoding="utf-8")

        print(f"📄 报告已保存: {output_path}")

    def run(self, save: bool = True):
        """运行聚合器"""
        print("🔍 正在聚合 AI 技术新闻...")

        # 筛选 AI 新闻
        ai_news = self.filter_ai_news(self.ai_news_sources)

        # 格式化报告
        report = self.format_news_report(ai_news)

        # 输出到控制台
        print(report)

        # 保存报告
        if save:
            self.save_report(report)

        return ai_news


def main():
    """主函数"""
    aggregator = AINewsAggregator()
    aggregator.run()


if __name__ == "__main__":
    main()
