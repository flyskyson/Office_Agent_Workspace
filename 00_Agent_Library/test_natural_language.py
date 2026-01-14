#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自然语言搜索测试脚本
"""

import sys
from pathlib import Path

# 添加模块路径
sys.path.insert(0, str(Path(__file__).parent))

print("\n" + "="*70)
print("自然语言搜索测试")
print("="*70 + "\n")

# 测试 1: 导入模块
print("测试 1: 导入自然语言搜索模块")
print("-" * 70)

try:
    from natural_language_search import NaturalLanguageParser, QueryType
    print("✅ 自然语言搜索模块导入成功")
    print(f"  模块: natural_language_search")
    print(f"  类: NaturalLanguageParser, QueryType")
except ImportError as e:
    print(f"❌ 模块导入失败: {e}")
    sys.exit(1)

print()

# 测试 2: 创建解析器
print("测试 2: 创建自然语言解析器")
print("-" * 70)

try:
    parser = NaturalLanguageParser()
    print("✅ 自然语言解析器创建成功")
except Exception as e:
    print(f"❌ 解析器创建失败: {e}")
    sys.exit(1)

print()

# 测试 3: 测试各种查询类型
print("测试 3: 测试各种查询类型")
print("-" * 70)

test_queries = [
    # 时间查询
    ("今天的笔记", QueryType.TIME_BASED),
    ("昨天的内容", QueryType.TIME_BASED),
    ("本周的文档", QueryType.TIME_BASED),
    ("上周的代码", QueryType.TIME_BASED),
    ("最近7天的 AI 相关", QueryType.TIME_BASED),

    # 文件类型查询
    ("Python 文件", QueryType.FILE_TYPE_BASED),
    ("Markdown 文档", QueryType.FILE_TYPE_BASED),
    ("Word 文档", QueryType.FILE_TYPE_BASED),

    # 主题查询
    ("关于 OCR 的内容", QueryType.TOPIC_BASED),
    ("AI 相关文档", QueryType.TOPIC_BASED),
    ("Flask 代码", QueryType.TOPIC_BASED),

    # 复合查询
    ("上周添加的 Python 笔记", QueryType.COMPLEX),
    ("今天的 AI 相关代码", QueryType.COMPLEX),
    ("最近的 Markdown 技术文档", QueryType.COMPLEX),
]

print(f"共有 {len(test_queries)} 个测试用例\n")

success_count = 0
for i, (query, expected_type) in enumerate(test_queries, 1):
    try:
        parsed = parser.parse(query)

        # 验证查询类型
        type_match = parsed.query_type == expected_type

        status = "✅" if type_match else "⚠️"
        print(f"{status} 测试 {i}: '{query}'")
        print(f"   类型: {parsed.query_type.value} (预期: {expected_type.value})")

        if parsed.time_range:
            print(f"   时间: {parsed.time_range.get('label', '未知')}")

        if parsed.file_types:
            print(f"   文件类型: {', '.join(parsed.file_types)}")

        if parsed.topics:
            print(f"   主题: {', '.join(parsed.topics)}")

        if parsed.keywords:
            print(f"   关键词: {', '.join(parsed.keywords)}")

        print()

        if type_match:
            success_count += 1

    except Exception as e:
        print(f"❌ 测试 {i} 失败: {e}")
        print()

# 测试 4: 高级查询测试
print("测试 4: 高级查询测试")
print("-" * 70)

advanced_queries = [
    "2026年1月添加的关于 Flask 和 AI 的 Python 笔记",
    "本周修改的 Markdown 格式的 OCR 相关文档",
    "昨天创建的 Word 文档",
]

for query in advanced_queries:
    try:
        parsed = parser.parse(query)
        print(f"✅ 查询: '{query}'")
        print(f"   类型: {parsed.query_type.value}")

        if parsed.keywords:
            print(f"   关键词: {', '.join(parsed.keywords)}")

        print()

    except Exception as e:
        print(f"⚠️  查询失败: {e}")
        print()

# 总结
print("="*70)
print("测试总结")
print("="*70)
print()
print(f"测试用例: {len(test_queries)}")
print(f"成功: {success_count}")
print(f"失败: {len(test_queries) - success_count}")
print(f"成功率: {success_count / len(test_queries) * 100:.1f}%")
print()

if success_count == len(test_queries):
    print("🎉 所有测试通过!")
else:
    print("⚠️  部分测试未通过，请检查")

print()
print("支持的查询模式:")
print("  • 时间查询: '今天的笔记', '上周的代码'")
print("  • 类型查询: 'Python 文件', 'Markdown 文档'")
print("  • 主题查询: '关于 OCR 的内容'")
print("  • 复合查询: '上周添加的 Python 笔记'")
print()
print("下一步:")
print("  1. 集成到记忆助手")
print("  2. 添加更多查询模式")
print("  3. 优化解析准确性")
print()
