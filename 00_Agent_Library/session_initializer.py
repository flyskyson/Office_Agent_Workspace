#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Claude Code 会话初始化器

每次会话开始时自动执行：
1. 加载角色定义
2. 加载用户偏好
3. 加载高优先级记忆
4. 显示最近活动
5. 准备好服务

使用方法:
    在每次会话开始时运行此脚本

作者: Claude Code
日期: 2026-01-15
"""

import sys
from pathlib import Path
from typing import Dict, List, Any

# Windows 终端编码修复
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    except:
        pass

# 添加路径
sys.path.insert(0, str(Path(__file__).parent))

from claude_memory import ClaudeMemory


# ============================================================================
# 会话初始化器
# ============================================================================

class SessionInitializer:
    """会话初始化器 - 自动加载记忆和角色"""

    def __init__(self, workspace_root: Path = None):
        self.memory = ClaudeMemory(workspace_root)
        self.workspace_root = workspace_root or Path.cwd()

    def initialize_session(self, show_details: bool = True, export_markdown: bool = True) -> Dict[str, Any]:
        """
        初始化会话

        推理过程:
        1. 首先显示角色定义（最重要）
        2. 然后显示用户偏好
        3. 接着加载高优先级记忆
        4. 最后显示最近活动
        5. 自动导出 Markdown（可选）
        6. 返回完整上下文
        """
        if show_details:
            self._print_header()

        # 1. 角色定义
        role_definition = self._load_role_definition(show_details)

        # 2. 用户偏好
        user_preferences = self._load_user_preferences(show_details)

        # 3. 高优先级记忆
        high_priority_memories = self._load_high_priority_memories(show_details)

        # 4. 最近活动
        recent_activity = self._load_recent_activity(show_details)

        # 5. 记忆统计
        memory_stats = self.memory.get_memory_stats()

        # 6. 自动导出 Markdown
        markdown_files = {}
        if export_markdown:
            try:
                from markdown_exporter import MarkdownExporter
                exporter = MarkdownExporter(self.workspace_root)
                markdown_files = exporter.export_all()
                if show_details:
                    print("\n📝 已导出 Markdown:")
                    for name, path in markdown_files.items():
                        print(f"   - {name}: {path}")
            except Exception as e:
                if show_details:
                    print(f"\n⚠️ Markdown 导出失败: {e}")

        if show_details:
            self._print_footer(memory_stats)

        return {
            'role_definition': role_definition,
            'user_preferences': user_preferences,
            'high_priority_memories': high_priority_memories,
            'recent_activity': recent_activity,
            'memory_stats': memory_stats,
            'markdown_files': markdown_files
        }

    def _print_header(self):
        """打印会话头部"""
        print("\n" + "═" * 80)
        print("🤖 Claude Code 会话初始化")
        print("═" * 80)
        print(f"⏰ 时间: {self._get_current_time()}")
        print(f"📂 工作区: {self.workspace_root}")
        print("═" * 80)

    def _load_role_definition(self, show_details: bool = True) -> str:
        """加载角色定义"""
        # 从记忆中获取角色定义
        contexts = self.memory.recall("Claude Code核心角色定义")

        if contexts:
            role = contexts[0]['summary']
            if show_details:
                print("\n🎯 我的角色")
                print("─" * 80)
                print(f"   \"{role}\"")
                print("\n💡 三大核心:")
                for point in contexts[0]['key_points']:
                    print(f"   {point}")
                print("\n⚠️ 您强调:")
                print(f"   {contexts[0]['outcomes']}")
            return role
        else:
            if show_details:
                print("\n⚠️ 角色定义未找到")
            return "未知"

    def _load_user_preferences(self, show_details: bool = True) -> Dict[str, Any]:
        """加载用户偏好"""
        prefs = self.memory.store.memory.get('preferences', {})

        if show_details:
            print("\n📝 您的工作偏好")
            print("─" * 80)

            # 工作方式偏好
            if 'work_style_priority' in prefs:
                work_style = prefs['work_style_priority']
                print(f"   🎯 优先方向: {work_style.get('primary_focus', '未设置')}")
                print(f"   🚀 主动性: {work_style.get('proactivity_level', '未设置')}")
                print(f"   🌪️  失败观: {work_style.get('failure_attitude', '未设置')}")
                print(f"   💬 交流方式: {work_style.get('communication_preference', '未设置')}")

        return prefs

    def _load_high_priority_memories(self, show_details: bool = True) -> List[Dict]:
        """加载高优先级记忆"""
        high_priority = self.memory.recall_high_priority(limit=10)

        if show_details and high_priority:
            print("\n⭐ 高优先级记忆")
            print("─" * 80)
            for i, ctx in enumerate(high_priority, 1):
                print(f"\n   {i}. {ctx['topic']}")
                print(f"      {ctx['summary'][:80]}...")
                if ctx.get('tags'):
                    print(f"      标签: {', '.join(ctx['tags'])}")

        return high_priority

    def _load_recent_activity(self, show_details: bool = True) -> List[Dict]:
        """加载最近活动"""
        recent = self.memory.recall_recent(limit=5)

        if show_details and recent:
            print("\n📅 最近活动")
            print("─" * 80)
            for ctx in recent:
                timestamp = ctx['timestamp'][:10] if 'timestamp' in ctx else '未知'
                print(f"   {timestamp}: {ctx['topic']}")

        return recent

    def _print_footer(self, memory_stats: Dict[str, Any]):
        """打印会话尾部"""
        print("\n📊 记忆统计")
        print("─" * 80)
        print(f"   上下文: {memory_stats['total_contexts']} 条")
        print(f"   决策: {memory_stats['total_decisions']} 条")
        print(f"   对话: {memory_stats['total_conversations']} 条")
        print(f"   大小: {memory_stats['memory_size_kb']:.1f} KB")

        print("\n" + "═" * 80)
        print("✅ 记忆加载完成，准备服务")
        print("═" * 80 + "\n")

    def _get_current_time(self) -> str:
        """获取当前时间"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ============================================================================
# 便捷函数
# ============================================================================

def initialize_session(show_details: bool = True) -> Dict[str, Any]:
    """初始化会话（便捷函数）"""
    initializer = SessionInitializer()
    return initializer.initialize_session(show_details)


# ============================================================================
# 命令行入口
# ============================================================================

def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description='Claude Code 会话初始化器')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='安静模式，只显示关键信息')

    args = parser.parse_args()

    # 初始化会话
    initializer = SessionInitializer()
    context = initializer.initialize_session(show_details=not args.quiet)

    # 返回上下文（可用于脚本）
    return context


if __name__ == "__main__":
    main()
