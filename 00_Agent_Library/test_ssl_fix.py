#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSL修复验证测试脚本

作者: Claude Code
日期: 2026-01-16
"""

import sys
import os
from pathlib import Path

# Windows 终端编码修复
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    except:
        pass


def test_ssl_fix():
    """测试SSL修复是否成功"""
    print("\n" + "="*60)
    print("🧪 SSL修复验证测试")
    print("="*60)

    # 设置镜像源
    print("\n1️⃣ 设置HF-Mirror镜像...")
    os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
    print(f"   ✅ HF_ENDPOINT = {os.environ.get('HF_ENDPOINT')}")

    # 测试导入
    print("\n2️⃣ 测试sentence_transformers导入...")
    try:
        from sentence_transformers import SentenceTransformer
        print("   ✅ sentence_transformers导入成功")
    except Exception as e:
        print(f"   ❌ 导入失败: {e}")
        return False

    # 测试模型加载
    print("\n3️⃣ 测试模型加载...")
    try:
        print("   🔄 正在加载模型 paraphrase-multilingual-MiniLM-L12-v2")
        print("   (首次运行会自动下载模型，约100MB)")
        model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        print("   ✅ 模型加载成功")

        # 测试编码
        print("\n4️⃣ 测试语义编码...")
        embeddings = model.encode(["测试文本", "test text"])
        print(f"   ✅ 编码成功，维度: {embeddings.shape}")

        # 测试语义搜索
        print("\n5️⃣ 测试语义搜索...")
        query = "人工智能"
        docs = ["机器学习", "深度学习", "自然语言处理", "计算机视觉"]
        query_embedding = model.encode([query])
        doc_embeddings = model.encode(docs)

        import numpy as np
        similarities = np.dot(query_embedding, doc_embeddings.T).flatten()
        top_indices = similarities.argsort()[-3:][::-1]

        print(f"   查询: {query}")
        print("   最相关的文档:")
        for i, idx in enumerate(top_indices, 1):
            print(f"     {i}. {docs[idx]} (相似度: {similarities[idx]:.3f})")

        print("\n" + "="*60)
        print("✅ 所有测试通过！SSL问题已修复")
        print("="*60)
        return True

    except Exception as e:
        print(f"   ❌ 测试失败: {e}")
        print("\n💡 备选方案:")
        print("   1. 检查网络连接")
        print("   2. 尝试禁用语义搜索: memory = ClaudeMemory(enable_semantic=False)")
        print("   3. 使用本地模型")
        return False


def main():
    """主函数"""
    success = test_ssl_fix()

    if success:
        print("\n✨ 语义记忆系统已就绪！")
        print("\n📝 使用方法:")
        print("   ```python")
        print("   from claude_memory import ClaudeMemory")
        print("   memory = ClaudeMemory()  # 语义搜索已自动启用")
        print("   ```")
    else:
        print("\n⚠️ SSL问题仍未解决，使用关键词搜索模式:")
        print("   ```python")
        print("   from claude_memory import ClaudeMemory")
        print("   memory = ClaudeMemory(enable_semantic=False)")
        print("   ```")

    print("\n")


if __name__ == "__main__":
    main()
