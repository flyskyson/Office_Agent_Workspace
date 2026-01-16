#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
记忆自动触发器

每次会话开始/结束时自动触发记忆操作：
- 会话开始：自动加载相关记忆
- 会话结束：自动保存对话上下文

作者: Claude Code
日期: 2026-01-15
"""

import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

# Windows 终端编码修复
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass

# 添加路径
sys.path.insert(0, str(Path(__file__).parent))

from claude_memory import ClaudeMemory


# ============================================================================
# 记忆触发器
# ============================================================================

class MemoryTrigger:
    """记忆自动触发器"""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.memory = ClaudeMemory(workspace_root)
        self.session_start_time = None
        self.session_context = {
            'topics_discussed': [],
            'tools_used': [],
            'decisions_made': [],
            'key_points': []
        }

    def on_session_start(self, initial_query: str = "") -> Dict[str, Any]:
        """
        会话开始时触发

        推理过程:
        1. 获取最近的高优先级记忆
        2. 搜索相关上下文
        3. 加载用户偏好
        4. 返回摘要信息
        """
        from datetime import datetime
        self.session_start_time = datetime.now()

        print("\n" + "=" * 70)
        print("🧠 记忆系统自动加载")
        print("=" * 70)

        # 1. 获取高优先级记忆
        high_priority = self.memory.recall_high_priority(limit=5)
        if high_priority:
            print(f"\n⭐ 高优先级记忆 ({len(high_priority)} 条):")
            for ctx in high_priority:
                print(f"   - {ctx['topic']}: {ctx['summary'][:50]}...")

        # 2. 获取最近的上下文
        recent = self.memory.recall_recent(limit=3)
        if recent:
            print(f"\n📅 最近活动 ({len(recent)} 条):")
            for ctx in recent:
                print(f"   - {ctx['timestamp'][:10]}: {ctx['topic']}")

        # 3. 搜索相关内容（基于初始查询）
        if initial_query:
            relevant = self.memory.search_memory(initial_query, limit=3)
            if relevant:
                print(f"\n🔍 相关记忆 ({len(relevant)} 条):")
                for ctx in relevant:
                    print(f"   - {ctx['topic']}: {ctx['summary'][:50]}...")

        # 4. 显示记忆统计
        stats = self.memory.get_memory_stats()
        print(f"\n📊 记忆统计:")
        print(f"   - 上下文: {stats['total_contexts']} 条")
        print(f"   - 决策: {stats['total_decisions']} 条")
        print(f"   - 对话: {stats['total_conversations']} 条")

        print("\n" + "=" * 70)
        print("✅ 记忆加载完成，准备服务")
        print("=" * 70 + "\n")

        return {
            'high_priority': high_priority,
            'recent': recent,
            'stats': stats
        }

    def on_session_end(self, session_summary: str, outcomes: str) -> str:
        """
        会话结束时触发

        推理过程:
        1. 汇总会话上下文
        2. 保存到记忆系统
        3. 生成会话报告
        """
        from datetime import datetime

        # 如果没有开始时间，说明是手动调用
        if not self.session_start_time:
            self.session_start_time = datetime.now()

        session_duration = datetime.now() - self.session_start_time

        print("\n" + "=" * 70)
        print("💾 记忆系统自动保存")
        print("=" * 70)

        # 构建主题（基于讨论的关键词）
        topic = self._infer_topic()

        # 保存会话上下文
        self.memory.remember_context(
            topic=topic,
            summary=session_summary,
            key_points=self.session_context['key_points'],
            tools_used=self.session_context['tools_used'],
            decisions_made=self.session_context['decisions_made'],
            outcomes=outcomes
        )

        print(f"\n✅ 会话已保存:")
        print(f"   - 主题: {topic}")
        print(f"   - 时长: {session_duration}")
        print(f"   - 工具: {', '.join(self.session_context['tools_used'][:5])}")
        print(f"   - 要点: {len(self.session_context['key_points'])} 个")

        print("\n" + "=" * 70)
        print("✅ 记忆保存完成")
        print("=" * 70 + "\n")

        return f"会话已保存: {topic}"

    def track_topic(self, topic: str):
        """跟踪讨论的主题"""
        if topic not in self.session_context['topics_discussed']:
            self.session_context['topics_discussed'].append(topic)

    def track_tool(self, tool: str):
        """跟踪使用的工具"""
        if tool not in self.session_context['tools_used']:
            self.session_context['tools_used'].append(tool)

    def track_decision(self, decision: str):
        """跟踪做出的决策"""
        if decision not in self.session_context['decisions_made']:
            self.session_context['decisions_made'].append(decision)

    def track_key_point(self, point: str):
        """跟踪关键点"""
        if point not in self.session_context['key_points']:
            self.session_context['key_points'].append(point)

    def _infer_topic(self) -> str:
        """推断会话主题"""
        topics = self.session_context['topics_discussed']
        if topics:
            # 返回出现频率最高的主题
            from collections import Counter
            return Counter(topics).most_common(1)[0][0]
        return "未分类会话"


# ============================================================================
# 便捷函数
# ============================================================================

def create_session_trigger() -> MemoryTrigger:
    """创建会话触发器"""
    return MemoryTrigger()


# ============================================================================
# 演示程序
# ============================================================================

def demo_memory_trigger():
    """演示记忆触发器"""

    print("""
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║              记忆自动触发器演示                                      ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
    """)

    trigger = create_session_trigger()

    # 模拟会话开始
    print("\n1️⃣ 模拟会话开始...")
    trigger.on_session_start("多Agent系统开发")

    # 模拟会话过程
    print("\n2️⃣ 模拟会话过程...")
    trigger.track_topic("多Agent系统开发")
    trigger.track_topic("记忆系统")
    trigger.track_tool("Write")
    trigger.track_tool("Read")
    trigger.track_tool("Bash")
    trigger.track_decision("使用WorkflowEngine")
    trigger.track_decision("创建记忆系统")
    trigger.track_key_point("实现了4个Agent")
    trigger.track_key_point("记忆持久化完成")

    # 模拟会话结束
    print("\n3️⃣ 模拟会话结束...")
    trigger.on_session_end(
        session_summary="演示了记忆自动触发器，实现了会话开始/结束的自动记忆",
        outcomes="成功演示自动记忆功能"
    )

    print("\n✅ 演示完成！")


if __name__ == "__main__":
    demo_memory_trigger()
