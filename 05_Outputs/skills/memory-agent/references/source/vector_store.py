#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
向量数据库模块
使用ChromaDB存储和检索向量嵌入
"""

import yaml
import chromadb
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime


class VectorStore:
    """向量数据库封装"""

    def __init__(self, config_path="config.yaml"):
        """初始化向量数据库"""
        # 加载配置
        config_path = Path(__file__).parent / config_path
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        db_config = config['vector_db']

        # 持久化目录（相对于工作区根目录）
        workspace_root = Path(__file__).parent.parent.parent
        persist_dir = workspace_root / db_config['persist_directory']
        persist_dir.mkdir(parents=True, exist_ok=True)

        print(f"📚 ChromaDB 数据目录: {persist_dir}")

        # 创建客户端
        self.client = chromadb.PersistentClient(path=str(persist_dir))

        # 获取或创建集合
        self.collection_name = db_config['collection_name']
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"description": "学习记忆向量数据库"}
        )

        print(f"✅ 向量数据库初始化完成")
        print(f"   集合: {self.collection_name}")
        print(f"   文档数: {self.collection.count()}")

    def add_documents(
        self,
        documents: List[str],
        embeddings: List[List[float]],
        metadatas: List[Dict],
        ids: List[str]
    ):
        """
        添加文档到向量数据库

        Args:
            documents: 文本内容列表
            embeddings: 向量嵌入列表
            metadatas: 元数据列表
            ids: 唯一ID列表
        """
        if len(documents) != len(embeddings) or len(documents) != len(metadatas) or len(documents) != len(ids):
            raise ValueError("documents, embeddings, metadatas, ids 长度必须一致")

        try:
            self.collection.add(
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            print(f"✅ 添加了 {len(documents)} 个文档")
        except Exception as e:
            print(f"❌ 添加文档失败: {e}")

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        filter: Optional[Dict] = None
    ) -> List[Dict]:
        """
        向量搜索

        Args:
            query_embedding: 查询向量
            top_k: 返回结果数
            filter: 元数据过滤条件

        Returns:
            搜索结果列表，每个结果包含:
            - document: 文本内容
            - metadata: 元数据
            - distance: 距离（越小越相似）
        """
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=filter
        )

        # 格式化结果
        formatted_results = []
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                formatted_results.append({
                    'document': doc,
                    'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                    'distance': results['distances'][0][i] if results['distances'] else 0,
                    'id': results['ids'][0][i] if results['ids'] else ''
                })

        return formatted_results

    def get_document(self, doc_id: str) -> Optional[Dict]:
        """根据ID获取文档"""
        results = self.collection.get(ids=[doc_id])

        if results['documents']:
            return {
                'document': results['documents'][0],
                'metadata': results['metadatas'][0] if results['metadatas'] else {},
                'id': doc_id
            }
        return None

    def update_document(
        self,
        doc_id: str,
        document: Optional[str] = None,
        embedding: Optional[List[float]] = None,
        metadata: Optional[Dict] = None
    ):
        """更新文档"""
        update_data = {}
        if document:
            update_data['documents'] = [document]
        if embedding:
            update_data['embeddings'] = [embedding]
        if metadata:
            update_data['metadatas'] = [metadata]

        try:
            self.collection.update(
                ids=[doc_id],
                **update_data
            )
            print(f"✅ 更新文档: {doc_id}")
        except Exception as e:
            print(f"❌ 更新失败: {e}")

    def delete_document(self, doc_id: str):
        """删除文档"""
        try:
            self.collection.delete(ids=[doc_id])
            print(f"✅ 删除文档: {doc_id}")
        except Exception as e:
            print(f"❌ 删除失败: {e}")

    def count(self) -> int:
        """返回文档总数"""
        return self.collection.count()

    def clear_all(self):
        """清空所有文档（危险操作）"""
        confirm = input("⚠️  确定要清空所有文档吗？(yes/no): ")
        if confirm.lower() == 'yes':
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "学习记忆向量数据库"}
            )
            print("✅ 已清空所有文档")
        else:
            print("❌ 取消操作")

    def get_stats(self) -> Dict:
        """获取数据库统计信息"""
        return {
            'collection_name': self.collection_name,
            'total_documents': self.collection.count(),
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }


def main():
    """测试向量数据库"""
    print("=" * 70)
    print("向量数据库测试")
    print("=" * 70)

    # 初始化
    store = VectorStore()

    # 显示统计信息
    stats = store.get_stats()
    print(f"\n📊 数据库统计:")
    print(f"   集合: {stats['collection_name']}")
    print(f"   文档数: {stats['total_documents']}")
    print(f"   时间: {stats['timestamp']}")

    # 测试搜索（如果有数据）
    if stats['total_documents'] > 0:
        from embedder import TextEmbedder
        import numpy as np

        embedder = TextEmbedder()

        # 测试查询
        query = "文件重命名"
        print(f"\n🔍 测试查询: '{query}'")

        query_embedding = embedder.embed_text(query)
        results = store.search(query_embedding, top_k=3)

        print(f"\n找到 {len(results)} 个结果:")
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['metadata'].get('title', 'N/A')}")
            print(f"   路径: {result['metadata'].get('path', 'N/A')}")
            print(f"   相似度: {1 - result['distance']:.2f}")
            print(f"   内容: {result['document'][:100]}...")


if __name__ == "__main__":
    main()
