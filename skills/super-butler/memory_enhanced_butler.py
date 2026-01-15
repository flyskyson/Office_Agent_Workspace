#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
记忆增强的超级管家系统

结合Claude Code记忆持久化功能，让超级管家能够：
1. 记住每次维护操作
2. 学习用户偏好
3. 智能推荐维护策略
4. 跨会话持续改进

作者: Claude Code
日期: 2026-01-15
"""

import sys
from pathlib import Path
from typing import Dict, List, Any

# 添加路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "00_Agent_Library"))

from claude_memory import MemoryEnhancedAgent, ClaudeMemory


# ============================================================================
# 记忆增强的超级管家
# ============================================================================

class MemoryEnhancedButler(MemoryEnhancedAgent):
    """拥有持久化记忆的超级管家"""

    def __init__(self, workspace_root: Path = None):
        super().__init__(workspace_root)
        self.workspace_root = workspace_root or Path.cwd()

    def perform_maintenance(self, task: str, context: Dict[str, Any] = None):
        """
        执行维护任务（带记忆学习）

        Args:
            task: 任务描述
            context: 上下文信息
        """
        print(f"\n🤖 记忆增强管家开始处理: {task}")

        # 1. 回忆相关经验
        print("🔍 正在回忆相关经验...")
        past_experiences = self.recall_before_action(task)

        if past_experiences:
            print(f"   ✅ 找到 {len(past_experiences)} 条相关经验")
            for exp in past_experiences[:3]:
                print(f"      - {exp.get('summary', '')[:60]}")
        else:
            print("   ℹ️ 这是首次处理此类任务")

        # 2. 获取基于经验的建议
        print("\n💡 基于历史的建议:")
        suggestion = self.suggest_based_on_experience(task)
        if suggestion:
            print(f"   → 推荐方案: {suggestion}")
        else:
            print("   → 暂无历史数据，使用默认策略")

        # 3. 执行任务（这里简化为记录）
        print(f"\n⚙️ 正在执行: {task}")
        # 实际执行逻辑...

        # 4. 学习本次决策
        print("\n📝 正在学习本次经验...")
        self.learn_from_action(
            task_type=task,
            tool_used="ButlerSystem",
            reasoning=f"基于{len(past_experiences)}条历史经验",
            success=True
        )

        # 5. 记住完整上下文
        self.remember_context(
            topic=task,
            summary=f"完成了{task}维护任务",
            key_points=context.get('key_points', []) if context else [],
            tools_used=context.get('tools_used', []) if context else [],
            decisions_made=context.get('decisions', []) if context else [],
            outcomes=context.get('outcome', '成功') if context else '已完成'
        )

        print("✅ 任务完成，已记住本次经验")

    def smart_git_cleanup(self):
        """智能Git清理（基于历史学习）"""

        # 回忆Git相关经验
        git_experiences = self.recall("git")

        if git_experiences:
            print("📊 基于历史数据分析:")
            # 统计最常用的Git操作
            operations = []
            for exp in git_experiences:
                operations.extend(exp.get('tools_used', []))

            if operations:
                from collections import Counter
                common_ops = Counter(operations).most_common(3)
                print("   最常用的Git操作:")
                for op, count in common_ops:
                    print(f"      - {op} ({count}次)")

        # 执行清理建议
        print("\n🧹 建议的清理操作:")
        print("   1. 清理未跟踪文件: git clean -fd")
        print("   2. 压缩历史: git gc --aggressive")
        print("   3. 修复引用: git fsck --full")

    def predict_user_needs(self, time_context: str) -> List[str]:
        """
        预测用户需求（基于历史模式）

        Args:
            time_context: 时间上下文（如"早晨", "项目开始"等）
        """
        # 从记忆中获取模式
        contexts = self.memory.store.memory['contexts']['contexts']

        # 简单的模式识别
        patterns = {}
        for ctx in contexts:
            summary = ctx.get('summary', '')
            if time_context.lower() in summary.lower():
                patterns[summary] = patterns.get(summary, 0) + 1

        # 排序并返回最可能的需求
        sorted_patterns = sorted(patterns.items(), key=lambda x: x[1], reverse=True)

        predictions = [item[0] for item in sorted_patterns[:5]]
        return predictions

    def show_memory_stats(self):
        """显示记忆统计"""
        stats = self.memory.get_memory_stats()

        print("\n" + "=" * 70)
        print("🧠 超级管家记忆系统")
        print("=" * 70)

        print(f"\n📊 累计服务:")
        print(f"   - 维护任务: {stats['total_contexts']} 次")
        print(f"   - 决策记录: {stats['total_decisions']} 次")
        print(f"   - 对话历史: {stats['total_conversations']} 次")

        if stats['topics_covered']:
            print(f"\n🔧 擅长的维护领域:")
            for topic in list(stats['topics_covered'])[:5]:
                count = self.memory.store.memory['contexts']['contexts_by_topic'][topic]
                print(f"   - {topic} ({count} 次)")

        if stats['most_used_tools']:
            print(f"\n🛠️ 熟练的工具:")
            for tool, count in sorted(stats['most_used_tools'].items(),
                                     key=lambda x: x[1], reverse=True)[:5]:
                print(f"   - {tool} ({count} 次)")

        print("\n" + "=" * 70)

    def learn_user_preferences(self, preferences: Dict[str, Any]):
        """学习用户偏好"""
        print("\n📚 正在学习用户偏好...")

        self.memory.learn_preferences(preferences)

        print("✅ 已记住以下偏好:")
        for key, value in preferences.items():
            if isinstance(value, dict):
                print(f"   {key}:")
                for k, v in value.items():
                    print(f"      - {k}: {v}")
            else:
                print(f"   - {key}: {value}")

    def remember_project_context(self, project_name: str, context: Dict[str, Any]):
        """记住项目上下文"""
        print(f"\n💾 正在记住项目 '{project_name}' 的上下文...")

        self.remember_context(
            topic=f"项目_{project_name}",
            summary=context.get('summary', f'{project_name}项目信息'),
            key_points=context.get('key_points', []),
            tools_used=context.get('tools_used', []),
            decisions_made=context.get('decisions', []),
            outcomes=context.get('status', '活跃')
        )

        # 更新项目知识
        self.memory.store.memory['projects']['project_knowledge'][project_name] = context
        self.memory.store.save('projects')

        print(f"✅ 已记住 '{project_name}' 的所有信息")

    def get_project_memory(self, project_name: str) -> Dict[str, Any]:
        """获取项目记忆"""
        # 从项目知识中获取
        project_knowledge = self.memory.store.memory['projects']['project_knowledge']
        if project_name in project_knowledge:
            return project_knowledge[project_name]

        # 从上下文中搜索
        contexts = self.recall(f"项目_{project_name}")
        if contexts:
            return contexts[0]

        return {}


# ============================================================================
# 演示程序
# ============================================================================

def demo_memory_butler():
    """演示记忆增强管家"""

    print("""
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║            记忆增强的超级管家系统演示                                ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
    """)

    # 创建记忆增强管家
    butler = MemoryEnhancedButler()

    print("\n" + "=" * 70)
    print("🎯 场景1: 日常维护任务")
    print("=" * 70)

    # 执行维护任务
    butler.perform_maintenance(
        task="工作区状态检查",
        context={
            'key_points': [
                "检查Git状态",
                "查看活跃项目",
                "扫描待处理文件"
            ],
            'tools_used': ["Bash: git status", "Glob", "Grep"],
            'decisions': [
                "使用Bash执行Git命令",
                "使用Glob搜索文件"
            ],
            'outcome': "发现9个未推送提交"
        }
    )

    print("\n" + "=" * 70)
    print("🎯 场景2: 学习用户偏好")
    print("=" * 70)

    # 学习用户偏好
    butler.learn_user_preferences({
        'coding_style': {
            'language': 'Python',
            'naming': 'snake_case',
            'indentation': '4空格'
        },
        'preferred_tools': {
            'file_read': 'Read工具',
            'file_edit': 'Edit工具',
            'code_search': 'Grep工具'
        },
        'communication': {
            'style': '简洁专业',
            'language': '中文',
            'detail_level': '适中'
        }
    })

    print("\n" + "=" * 70)
    print("🎯 场景3: 记住项目上下文")
    print("=" * 70)

    # 记住市场监管智能体项目
    butler.remember_project_context(
        project_name="market_supervision_agent",
        context={
            'summary': '市场监管智能体 - 自动填写申请书的Web应用',
            'key_points': [
                "Flask Web UI",
                "百度OCR集成",
                "Jinja2模板引擎",
                "端口5000"
            ],
            'tools_used': ["Flask", "PaddleOCR", "Jinja2"],
            'decisions': [
                "使用Flask而非Streamlit",
                "OCR降级到PaddleOCR"
            ],
            'status': '生产就绪'
        }
    )

    print("\n" + "=" * 70)
    print("🎯 场景4: 智能Git清理")
    print("=" * 70)

    butler.smart_git_cleanup()

    print("\n" + "=" * 70)
    print("🎯 场景5: 显示记忆统计")
    print("=" * 70)

    butler.show_memory_stats()

    print("\n" + "=" * 70)
    print("🎯 场景6: 预测用户需求")
    print("=" * 70)

    predictions = butler.predict_user_needs("项目")
    print(f"\n🔮 预测您可能需要:")
    for i, pred in enumerate(predictions, 1):
        print(f"   {i}. {pred}")

    if not predictions:
        print("   暂无足够数据进行预测")

    print("\n" + "=" * 70)
    print("🎯 场景7: 获取项目记忆")
    print("=" * 70)

    project_memory = butler.get_project_memory("market_supervision_agent")
    if project_memory:
        print(f"\n📋 市场监管智能体项目记忆:")
        print(f"   摘要: {project_memory.get('summary', 'N/A')}")
        print(f"   状态: {project_memory.get('outcomes', 'N/A')}")

        if project_memory.get('key_points'):
            print(f"   关键信息:")
            for point in project_memory['key_points']:
                print(f"      - {point}")

    print("\n" + "=" * 70)
    print("✅ 记忆增强管家演示完成！")
    print("\n💡 核心价值:")
    print("   ✅ 每次服务都记住经验")
    print("   ✅ 跨会话持续学习")
    print("   ✅ 智能预测用户需求")
    print("   ✅ 累积项目专业知识")
    print("   ✅ 提供个性化建议")
    print("\n📂 记忆存储位置:")
    print("   06_Learning_Journal/claude_memory/")
    print("=" * 70)


if __name__ == "__main__":
    demo_memory_butler()
