#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文本嵌入模块
使用sentence-transformers生成本地向量嵌入
"""

import yaml
from pathlib import Path
from sentence_transformers import SentenceTransformer
from typing import List, Union


class TextEmbedder:
    """文本嵌入器 - 生成本地向量"""

    def __init__(self, config_path="config.yaml"):
        """初始化嵌入器"""
        # 加载配置
        config_path = Path(__file__).parent / config_path
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        embedding_config = config['embedding']

        print(f"📦 加载嵌入模型: {embedding_config['model_name']}")
        print(f"   设备: {embedding_config['device']}")

        # 加载模型（首次会下载，约500MB）
        self.model = SentenceTransformer(
            embedding_config['model_name'],
            device=embedding_config['device']
        )

        self.batch_size = embedding_config.get('batch_size', 32)

        # 获取向量维度
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        print(f"✅ 模型加载完成！向量维度: {self.embedding_dim}")

    def embed_texts(self, texts: List[str], show_progress=False) -> List[List[float]]:
        """
        嵌入文本列表

        Args:
            texts: 文本列表
            show_progress: 是否显示进度条

        Returns:
            向量列表
        """
        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            batch_size=self.batch_size,
            show_progress_bar=show_progress,
            convert_to_numpy=True
        )

        return embeddings.tolist()

    def embed_text(self, text: str) -> List[float]:
        """
        嵌入单个文本

        Args:
            text: 文本内容

        Returns:
            向量
        """
        embedding = self.model.encode(
            text,
            convert_to_numpy=True
        )
        return embedding.tolist()

    @property
    def dimension(self) -> int:
        """返回向量维度"""
        return self.embedding_dim


def main():
    """测试嵌入器"""
    print("=" * 70)
    print("文本嵌入器测试")
    print("=" * 70)

    embedder = TextEmbedder()

    # 测试文本
    test_texts = [
        "Python文件批量重命名技巧",
        "使用Path.rename()方法重命名文件",
        "机器学习模型训练",
        "今天天气很好"
    ]

    print("\n📝 测试文本:")
    for i, text in enumerate(test_texts, 1):
        print(f"  {i}. {text}")

    print("\n🔄 生成嵌入向量...")
    embeddings = embedder.embed_texts(test_texts, show_progress=True)

    print(f"\n✅ 生成了 {len(embeddings)} 个向量")
    print(f"   向量维度: {len(embeddings[0])}")

    # 计算相似度
    import numpy as np

    def cosine_similarity(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    print("\n📊 相似度矩阵:")
    print("   " + "  ".join([f"{i+1}" for i in range(len(test_texts))]))

    for i in range(len(test_texts)):
        row = []
        for j in range(len(test_texts)):
            if i == j:
                row.append("1.00")
            else:
                sim = cosine_similarity(embeddings[i], embeddings[j])
                row.append(f"{sim:.2f}")
        print(f" {i+1} " + "  ".join(row))


if __name__ == "__main__":
    main()
