#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
记忆迁移工具 - 将现有JSON记忆迁移到向量数据库

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
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass

# 设置国内镜像
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "00_Agent_Library"))

from semantic_memory import SemanticMemory, MemoryMigrator


def main():
    print("""
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║              记忆迁移工具 - JSON到向量数据库                        ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
    """)

    # 初始化语义记忆
    print("\n🔄 初始化语义记忆系统...")
    semantic = SemanticMemory()
    migrator = MemoryMigrator(semantic)

    # 获取contexts.json路径
    contexts_file = (project_root / "06_Learning_Journal" / "claude_memory" / "contexts.json")

    if not contexts_file.exists():
        print(f"❌ 文件不存在: {contexts_file}")
        return False

    print(f"📂 读取: {contexts_file}")

    # 显示当前状态
    import json
    with open(contexts_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total_contexts = data.get('total_contexts', 0)
    print(f"📊 现有记忆数: {total_contexts}")

    # 执行迁移
    print("\n🚀 开始迁移...")
    print("-" * 70)

    result = migrator.migrate_from_json(contexts_file, batch_size=10)

    # 显示结果
    print("\n" + "=" * 70)
    print("📊 迁移结果")
    print("=" * 70)
    print(f"✅ 总数: {result.get('total', 0)}")
    print(f"✅ 成功: {result.get('success', 0)}")
    print(f"❌ 失败: {result.get('failed', 0)}")

    # 显示统计
    stats = semantic.get_stats()
    print(f"\n📊 向量数据库统计:")
    print(f"   记忆总数: {stats['total_memories']}")
    print(f"   模型: {stats['model_name']}")

    # 验证搜索
    print("\n" + "=" * 70)
    print("🔍 验证语义搜索")
    print("=" * 70)

    test_queries = [
        "Agent相关",
        "工作区状态",
        "角色定义",
        "记忆系统"
    ]

    for query in test_queries:
        results = semantic.search(query, top_k=2)
        print(f"\n💭 查询: '{query}'")
        if results:
            for i, r in enumerate(results, 1):
                print(f"   {i}. {r['similarity_score']:.2%} - {r['text'][:60]}...")
        else:
            print("   ⚠️ 未找到结果")

    print("\n" + "=" * 70)
    print("🎉 迁移完成！所有记忆现在支持语义搜索")
    print("=" * 70)

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
