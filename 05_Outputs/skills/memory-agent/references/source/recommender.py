#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能推荐模块
提供相似问题关联和智能推荐
"""

import yaml
from pathlib import Path
from typing import List, Dict, Tuple
from datetime import datetime

from embedder import TextEmbedder
from vector_store import VectorStore


class SmartRecommender:
    """智能推荐系统"""

    def __init__(self, config_path="config.yaml"):
        """初始化推荐系统"""
        # 加载配置
        config_path = Path(__file__).parent / config_path
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

        # 初始化组件
        self.embedder = TextEmbedder(config_path)
        self.vector_store = VectorStore(config_path)

    def find_similar_problems(self, problem_desc: str, top_k: int = 5) -> List[Dict]:
        """
        查找相似的历史问题

        Args:
            problem_desc: 问题描述
            top_k: 返回结果数

        Returns:
            相似问题列表，每个包含:
            - content: 问题内容
            - metadata: 元数据
            - similarity: 相似度
        """
        # 生成查询向量
        query_embedding = self.embedder.embed_text(problem_desc)

        # 搜索（优先查找challenges_solved）
        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k * 2
        )

        # 过滤并格式化
        similar_problems = []
        for result in results:
            similarity = 1 - result['distance']

            # 只返回相似度>0.4的结果
            if similarity > 0.4:
                similar_problems.append({
                    'content': result['document'],
                    'metadata': result['metadata'],
                    'similarity': similarity
                })

        # 按相似度排序
        similar_problems.sort(key=lambda x: x['similarity'], reverse=True)
        return similar_problems[:top_k]

    def relate_documents(self, doc_id: str, top_k: int = 5) -> List[Dict]:
        """
        查找与指定文档相关的其他文档

        Args:
            doc_id: 文档ID
            top_k: 返回结果数

        Returns:
            相关文档列表
        """
        # 获取文档
        doc = self.vector_store.get_document(doc_id)
        if not doc:
            return []

        # 使用文档内容进行搜索
        query_embedding = self.embedder.embed_text(doc['document'])

        # 搜索相似文档（排除自己）
        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k + 1
        )

        # 移除自己并格式化
        related_docs = []
        for result in results:
            if result['id'] != doc_id:
                similarity = 1 - result['distance']
                related_docs.append({
                    'content': result['document'],
                    'metadata': result['metadata'],
                    'similarity': similarity,
                    'id': result['id']
                })

        return related_docs[:top_k]

    def get_learning_path(self, topic: str, depth: int = 2) -> Dict:
        """
        生成学习路径推荐

        Args:
            topic: 学习主题
            depth: 路径深度（层级数）

        Returns:
            学习路径字典
        """
        # 搜索相关文档
        query_embedding = self.embedder.embed_text(topic)
        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=10
        )

        if not results:
            return {
                'topic': topic,
                'message': '未找到相关学习资料',
                'path': []
            }

        # 构建学习路径
        path = []
        for i, result in enumerate(results[:5]):
            similarity = 1 - result['distance']

            # 只包含高相关性文档
            if similarity > 0.5:
                # 查找相关文档
                related = self.relate_documents(result['id'], top_k=2)

                path.append({
                    'order': i + 1,
                    'title': result['metadata'].get('title', 'N/A'),
                    'path': result['metadata'].get('path', 'N/A'),
                    'similarity': similarity,
                    'related': [
                        {
                            'title': r['metadata'].get('title', 'N/A'),
                            'path': r['metadata'].get('path', 'N/A')
                        }
                        for r in related
                    ]
                })

        return {
            'topic': topic,
            'total_steps': len(path),
            'path': path
        }

    def suggest_related_topics(self, doc_id: str) -> List[str]:
        """
        推荐相关主题标签

        Args:
            doc_id: 文档ID

        Returns:
            主题标签列表
        """
        # 获取相关文档
        related = self.relate_documents(doc_id, top_k=5)

        # 提取主题
        topics = set()
        for doc in related:
            # 从分类中提取
            category = doc['metadata'].get('category')
            if category:
                topics.add(category)

            # 从标题中提取关键词（简单实现）
            title = doc['metadata'].get('title', '')
            if 'Python' in title:
                topics.add('Python')
            if '文件' in title:
                topics.add('文件操作')
            if 'Agent' in title:
                topics.add('Agent开发')

        return list(topics)[:5]

    def format_similar_problems(self, problems: List[Dict]) -> str:
        """格式化相似问题结果"""
        if not problems:
            return "💭 未找到相似的历史问题"

        output = []
        output.append("=" * 70)
        output.append("💭 相似的历史问题")
        output.append("=" * 70)

        for i, problem in enumerate(problems, 1):
            metadata = problem['metadata']
            similarity = problem['similarity']

            output.append(f"\n{i}. {metadata.get('title', 'N/A')}")
            output.append(f"   📁 {metadata.get('path', 'N/A')}")
            output.append(f"   🎯 相似度: {similarity:.2%}")

            # 内容预览
            content = problem['content']
            preview = content[:150] + "..." if len(content) > 150 else content
            output.append(f"   📝 {preview}")

        return '\n'.join(output)

    def format_learning_path(self, path_data: Dict) -> str:
        """格式化学习路径"""
        output = []
        output.append("=" * 70)
        output.append(f"📚 学习路径: {path_data['topic']}")
        output.append("=" * 70)

        if path_data.get('message'):
            output.append(f"\n{path_data['message']}")
        elif not path_data['path']:
            output.append("\n暂无推荐路径")
        else:
            output.append(f"\n推荐 {path_data['total_steps']} 个学习步骤:\n")

            for step in path_data['path']:
                output.append(f"{step['order']}. {step['title']}")
                output.append(f"   📁 {step['path']}")
                output.append(f"   🎯 相关度: {step['similarity']:.2%}")

                if step['related']:
                    output.append(f"   🔗 相关:")
                    for rel in step['related']:
                        output.append(f"      → {rel['title']}")

                output.append("")

        return '\n'.join(output)


def main():
    """测试推荐系统"""
    import sys

    recommender = SmartRecommender()

    if len(sys.argv) < 2:
        # 示例查询
        print("🧪 智能推荐系统测试\n")

        # 测试1: 相似问题
        print("=" * 70)
        print("测试1: 查找相似问题")
        print("=" * 70)
        problem = "如何批量重命名文件？"
        print(f"问题: {problem}\n")

        similar = recommender.find_similar_problems(problem)
        print(recommender.format_similar_problems(similar))

        # 测试2: 学习路径
        print("\n" + "=" * 70)
        print("测试2: 生成学习路径")
        print("=" * 70)
        topic = "文件操作"
        print(f"主题: {topic}\n")

        path = recommender.get_learning_path(topic)
        print(recommender.format_learning_path(path))

    else:
        command = sys.argv[1]

        if command == "similar" and len(sys.argv) > 2:
            problem = ' '.join(sys.argv[2:])
            results = recommender.find_similar_problems(problem)
            print(recommender.format_similar_problems(results))

        elif command == "path" and len(sys.argv) > 2:
            topic = ' '.join(sys.argv[2:])
            path = recommender.get_learning_path(topic)
            print(recommender.format_learning_path(path))

        else:
            print("用法:")
            print("  python recommender.py similar <问题描述>")
            print("  python recommender.py path <学习主题>")


if __name__ == "__main__":
    main()
