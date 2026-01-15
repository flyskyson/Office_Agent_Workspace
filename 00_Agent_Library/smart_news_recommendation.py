# -*- coding: utf-8 -*-
"""
智能新闻推荐助手
Smart News Recommendation Assistant

根据用户兴趣关键词自动筛选和推荐AI技术新闻
"""
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set

# Windows 编码修复
if sys.platform == 'win32' and hasattr(sys.stdout, 'buffer'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')


class SmartNewsRecommender:
    """智能新闻推荐助手"""

    def __init__(self):
        # 加载用户兴趣
        interest_file = Path("06_Learning_Journal/workspace_memory/user_interests.json")
        if interest_file.exists():
            data = json.loads(interest_file.read_text(encoding="utf-8"))
            self.user_interests = set(data.get("long_term", [])) | set(data.get("short_term", []))
        else:
            self.user_interests = {
                "AI", "人工智能", "GPT", "ChatGPT", "Claude", "深度学习",
                "机器学习", "LLM", "大模型", "LangChain", "RAG", "Agent",
                "智能体", "向量数据库", "Embedding", "Transformer", "神经网络",
                "NLP", "自然语言处理", "OpenAI", "Anthropic", "GLM", "智谱"
            }

        # 模拟AI新闻数据
        self.ai_news_database = [
            {
                "title": "OpenAI 发布 GPT-5 预览版，性能提升 300%",
                "category": "大模型",
                "source": "GitHub Trending",
                "url": "https://github.com/OpenAI/gpt-5",
                "stars": "🔥 50k+",
                "description": "新一代语言模型，支持多模态输入输出",
                "keywords": ["OpenAI", "GPT", "GPT-5", "大模型", "AI", "LLM"]
            },
            {
                "title": "LangChain v0.3 发布：RAG 应用开发更简单",
                "category": "AI Agent",
                "source": "GitHub Trending",
                "url": "https://github.com/langchain-ai/langchain",
                "stars": "🔥 90k+",
                "description": "全新的 RAG 组件和 Agent 编排功能",
                "keywords": ["LangChain", "RAG", "AI Agent", "Agent", "LLM", "智能体"]
            },
            {
                "title": "AutoGen 2.0：多智能体协作框架",
                "category": "AI Agent",
                "source": "GitHub Trending",
                "url": "https://github.com/microsoft/autogen",
                "stars": "🔥 30k+",
                "description": "支持代码执行、工具调用、人机协作",
                "keywords": ["AutoGen", "Agent", "AI Agent", "智能体", "Microsoft", "多智能体"]
            },
            {
                "title": "Claude Code 2.1 技能热重载功能",
                "category": "开发工具",
                "source": "AI 工具更新",
                "url": "https://code.claude.com/docs/en/changelog",
                "description": "支持技能热重载、109 项 CLI 优化",
                "keywords": ["Claude", "Claude Code", "Anthropic", "开发工具", "AI"]
            },
            {
                "title": "ChromaDB v1.0：向量数据库生产就绪",
                "category": "RAG",
                "source": "AI 工具更新",
                "url": "https://docs.trychroma.com",
                "description": "性能提升 10x，支持分布式部署",
                "keywords": ["ChromaDB", "向量数据库", "RAG", "Embedding", "数据库"]
            },
            {
                "title": "Llama 4 开源：700亿参数超越 GPT-4",
                "category": "大模型",
                "source": "HuggingFace",
                "url": "https://huggingface.co/meta-llama/Llama-4",
                "downloads": "📥 10M+",
                "description": "Meta 最新开源大模型，性能卓越",
                "keywords": ["Llama", "Meta", "大模型", "LLM", "开源", "GPT"]
            },
            {
                "title": "BGE-M4 嵌入模型：中文语义理解新高度",
                "category": "RAG",
                "source": "HuggingFace",
                "url": "https://huggingface.co/BAAI/bge-m4",
                "downloads": "📥 5M+",
                "description": "智谱研究院最新嵌入模型",
                "keywords": ["BGE", "Embedding", "智谱", "GLM", "中文", "RAG", "语义理解"]
            },
            {
                "title": "MCP 生态系统爆发：50+ 服务器可用",
                "category": "MCP",
                "source": "AI 工具更新",
                "url": "https://modelcontextprotocol.io",
                "description": "浏览器、数据库、文件系统全覆盖",
                "keywords": ["MCP", "MCP服务器", "Model Context Protocol", "AI", "工具"]
            }
        ]

    def calculate_match_score(self, news: Dict) -> float:
        """计算新闻匹配度"""
        news_keywords = set(news.get("keywords", []))
        title = news["title"].lower()

        # 直接匹配关键词
        direct_matches = len(self.user_interests & news_keywords)

        # 标题中包含兴趣词
        title_matches = sum(1 for interest in self.user_interests
                           if interest.lower() in title)

        # 计算匹配分数 (0-100%)
        total_possible = len(self.user_interests)
        if total_possible == 0:
            return 0.0

        score = (direct_matches * 2 + title_matches) / total_possible
        return min(score, 1.0)  # 最多100%

    def get_recommendations(self, threshold: float = 0.3, limit: int = 5) -> List[Dict]:
        """获取推荐新闻

        Args:
            threshold: 匹配度阈值 (0-1)
            limit: 最大返回数量

        Returns:
            匹配的新闻列表，按匹配度排序
        """
        scored_news = []

        for news in self.ai_news_database:
            score = self.calculate_match_score(news)
            if score >= threshold:
                news_with_score = news.copy()
                news_with_score["match_score"] = score
                scored_news.append(news_with_score)

        # 按匹配度排序
        scored_news.sort(key=lambda x: x["match_score"], reverse=True)

        return scored_news[:limit]

    def format_summary(self, recommendations: List[Dict]) -> str:
        """格式化推荐摘要（简短版）"""
        lines = []
        lines.append("## 📰 今日AI新闻推荐")
        lines.append(f"🔔 发现 {len(recommendations)} 条与您兴趣相关的AI技术新闻：")

        for i, news in enumerate(recommendations, 1):
            lines.append(f"   {i}. {news['title']}")

        lines.append("")
        lines.append("💡 是否查看详细新闻？[查看详情] / [跳过]")

        return "\n".join(lines)

    def format_detailed(self, recommendations: List[Dict]) -> str:
        """格式化详细新闻"""
        lines = []
        lines.append("=" * 80)
        lines.append("🤖 AI 技术新闻日报")
        lines.append("=" * 80)
        lines.append(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"📊 共找到 {len(recommendations)} 条 AI 技术相关新闻")
        lines.append("")

        # 按分类分组
        by_category = {}
        for news in recommendations:
            category = news["category"]
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

        return "\n".join(lines)

    def get_greeting_summary(self) -> str:
        """获取管家启动时的问候摘要"""
        recommendations = self.get_recommendations(threshold=0.3, limit=5)

        return f"""# 🤖 超级管家模式已激活

您好！我是您的智能工作区管家。

## 📊 工作区状态
- 活跃项目: 4个
- 可用工具: 39个
- Python版本: 3.12.9

{self.format_summary(recommendations)}

## 💡 我还能帮您
- 启动任何智能体或工具
- 搜索代码和知识
- 诊断技术问题
- 管理工作区
- 生成文档报告

请问您需要什么帮助？
"""

    def run_interaction(self):
        """运行交互式推荐"""
        # 获取推荐
        recommendations = self.get_recommendations(threshold=0.3, limit=5)

        # 显示摘要
        print(self.get_greeting_summary())

        # 询问用户
        print("\n🤔 请选择：")
        print("  1. 查看详细新闻")
        print("  2. 跳过，继续其他服务")
        print()

        choice = input("请选择 (1-2): ").strip()

        if choice == "1":
            print("\n" + self.format_detailed(recommendations))
        else:
            print("\n✅ 已跳过新闻，为您准备其他服务...")


def main():
    """主函数"""
    recommender = SmartNewsRecommender()

    # 如果是命令行运行，显示交互式
    if len(sys.argv) == 1:
        recommender.run_interaction()
    else:
        # 否则只显示摘要（用于脚本调用）
        print(recommender.get_greeting_summary())


if __name__ == "__main__":
    main()
