#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语义搜索模块
提供智能的语义搜索功能
"""

import yaml
from pathlib import Path
from typing import List, Dict, Optional

from embedder import TextEmbedder
from vector_store import VectorStore


class SemanticSearch:
    """语义搜索引擎"""

    def __init__(self, config_path="config.yaml"):
        """初始化搜索引擎"""
        # 加载配置
        config_path = Path(__file__).parent / config_path
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

        # 初始化组件
        self.embedder = TextEmbedder(config_path)
        self.vector_store = VectorStore(config_path)

        # 搜索配置
        self.top_k = self.config['search']['top_k']
        self.similarity_threshold = self.config['search']['similarity_threshold']

    def search(
        self,
        query: str,
        top_k: Optional[int] = None,
        filter_type: Optional[str] = None,
        min_similarity: Optional[float] = None
    ) -> List[Dict]:
        """
        语义搜索

        Args:
            query: 搜索查询
            top_k: 返回结果数（默认使用配置文件中的值）
            filter_type: 过滤文档类型 ('journal', 'project', None)
            min_similarity: 最小相似度阈值

        Returns:
            搜索结果列表
        """
        if not query.strip():
            return []

        # 生成查询向量
        query_embedding = self.embedder.embed_text(query)

        # 设置参数
        k = top_k or self.top_k
        threshold = min_similarity or self.similarity_threshold

        # 构建过滤条件
        filter_dict = None
        if filter_type:
            filter_dict = {'type': filter_type}

        # 搜索
        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=k * 2,  # 获取更多结果，后续过滤
            filter=filter_dict
        )

        # 计算相似度并过滤
        formatted_results = []
        for result in results:
            # ChromaDB返回的是距离，需要转换为相似度
            similarity = 1 - result['distance']

            if similarity >= threshold:
                formatted_results.append({
                    'content': result['document'],
                    'metadata': result['metadata'],
                    'similarity': similarity,
                    'id': result['id']
                })

        # 按相似度排序并返回top_k
        formatted_results.sort(key=lambda x: x['similarity'], reverse=True)
        return formatted_results[:k]

    def search_code(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        搜索代码片段

        Args:
            query: 搜索查询
            top_k: 返回结果数

        Returns:
            代码搜索结果
        """
        return self.search(
            query=query,
            top_k=top_k,
            filter_type='project'
        )

    def search_notes(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        搜索学习笔记

        Args:
            query: 搜索查询
            top_k: 返回结果数

        Returns:
            笔记搜索结果
        """
        return self.search(
            query=query,
            top_k=top_k,
            filter_type='journal'
        )

    def format_results(self, results: List[Dict], show_content: bool = True) -> str:
        """
        格式化搜索结果

        Args:
            results: 搜索结果列表
            show_content: 是否显示完整内容

        Returns:
            格式化的字符串
        """
        if not results:
            return "🔍 未找到相关结果"

        output = []
        output.append("=" * 70)
        output.append(f"找到 {len(results)} 个相关结果")
        output.append("=" * 70)

        for i, result in enumerate(results, 1):
            metadata = result['metadata']
            similarity = result['similarity']

            # 标题行
            title = metadata.get('title', 'N/A')
            output.append(f"\n{i}. {title}")
            output.append(f"   📁 {metadata.get('path', 'N/A')}")
            output.append(f"   📅 {metadata.get('modified', 'N/A')}")
            output.append(f"   🎯 相似度: {similarity:.2%}")

            # 类型标签
            doc_type = metadata.get('type', 'unknown')
            type_label = {
                'journal': '📓 学习笔记',
                'project': '💻 项目代码'
            }.get(doc_type, doc_type)
            output.append(f"   🏷️  {type_label}")

            # 内容预览
            if show_content:
                content = result['content']
                preview_length = 200
                if len(content) > preview_length:
                    preview = content[:preview_length] + "..."
                else:
                    preview = content

                output.append(f"\n   📝 内容:")
                for line in preview.split('\n')[:5]:  # 最多5行
                    output.append(f"      {line}")

        return '\n'.join(output)

    def interactive_search(self):
        """交互式搜索模式"""
        print("\n" + "=" * 70)
        print("🔍 学习记忆助手 - 语义搜索")
        print("=" * 70)
        print("\n提示:")
        print("  - 输入搜索查询")
        print("  - 前缀 'code:' 搜索代码")
        print("  - 前缀 'note:' 搜索笔记")
        print("  - 输入 'quit' 退出")
        print()

        while True:
            try:
                query = input("🔎 搜索: ").strip()

                if not query:
                    continue

                if query.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 再见！")
                    break

                # 检测前缀
                if query.lower().startswith('code:'):
                    query_text = query[5:].strip()
                    results = self.search_code(query_text)
                    mode = "代码"
                elif query.lower().startswith('note:'):
                    query_text = query[5:].strip()
                    results = self.search_notes(query_text)
                    mode = "笔记"
                else:
                    results = self.search(query)
                    mode = "全部"

                # 显示结果
                print(f"\n📊 {mode}搜索结果:")
                print(self.format_results(results))
                print()

            except KeyboardInterrupt:
                print("\n\n👋 再见！")
                break
            except Exception as e:
                print(f"\n❌ 搜索出错: {e}\n")


def main():
    """主函数 - 用于测试"""
    import sys

    search_engine = SemanticSearch()

    if len(sys.argv) < 2:
        # 交互模式
        search_engine.interactive_search()
    else:
        # 命令行模式
        query = ' '.join(sys.argv[1:])

        print(f"\n🔍 搜索: '{query}'")
        results = search_engine.search(query)

        print(search_engine.format_results(results))


if __name__ == "__main__":
    main()
