#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强的记忆助手 - 支持自然语言搜索
"""

import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "00_Agent_Library"))

from memory_agent import MemoryAgent
from natural_language_search import EnhancedSearchEngine, QueryType


class EnhancedMemoryAgent(MemoryAgent):
    """增强的记忆助手 - 支持自然语言搜索"""

    def __init__(self):
        """初始化增强助手"""
        super().__init__()

        # 创建自然语言搜索引擎
        self.nl_search_engine = EnhancedSearchEngine(
            base_search_engine=self.search_engine
        )

        print("✅ 增强记忆助手已启动（支持自然语言搜索）")

    def natural_search(self, query: str, top_k: int = 10):
        """
        自然语言搜索

        Args:
            query: 自然语言查询
            top_k: 返回结果数量
        """
        print(f"\n{'='*70}")
        print(f"🔍 自然语言搜索: '{query}'")
        print(f"{'='*70}\n")

        # 执行搜索
        result = self.nl_search_engine.search(query, top_k=top_k)

        # 显示解析结果
        parsed = result['parsed']
        print(f"📋 查询类型: {parsed.query_type.value}")

        if parsed.time_range:
            print(f"⏰ 时间范围: {parsed.time_range.get('label', '未知')}")

        if parsed.file_types:
            print(f"📄 文件类型: {', '.join(parsed.file_types)}")

        if parsed.topics:
            print(f"🏷️  主题: {', '.join(parsed.topics)}")

        if parsed.keywords:
            print(f"🔑 关键词: {', '.join(parsed.keywords)}")

        # 显示搜索结果
        print(f"\n📊 搜索结果 ({result['count']} 条):\n")

        for i, item in enumerate(result['results'], 1):
            if isinstance(item, dict):
                title = item.get('title', item.get('name', '未知'))
                content = item.get('content', item.get('snippet', ''))
                score = item.get('score', item.get('similarity', 0))
                print(f"{i}. {title}")
                print(f"   相似度: {score:.2f}")
                if content:
                    preview = content[:100] + "..." if len(content) > 100 else content
                    print(f"   预览: {preview}")
                print()

    def search_last_week(self, topic: str = ""):
        """搜索上周的内容"""
        query = f"上周 {topic}" if topic else "上周的所有内容"
        self.natural_search(query)

    def search_today(self, topic: str = ""):
        """搜索今天的内容"""
        query = f"今天 {topic}" if topic else "今天的所有内容"
        self.natural_search(query)

    def search_by_type(self, file_type: str, topic: str = ""):
        """按文件类型搜索"""
        query = f"{file_type} {topic}".strip()
        self.natural_search(query)


# 使用示例
if __name__ == "__main__":
    # 创建增强助手
    agent = EnhancedMemoryAgent()

    print("\n=== 增强记忆助手 - 自然语言搜索演示 ===\n")

    # 测试查询
    test_queries = [
        "上周添加的 Python 笔记",
        "今天的 AI 相关内容",
        "最近的 Flask 代码",
        "关于 OCR 的所有文档"
    ]

    for query in test_queries:
        print(f"\n{'─'*70}")
        agent.natural_search(query, top_k=5)

    print("\n✅ 测试完成！")
