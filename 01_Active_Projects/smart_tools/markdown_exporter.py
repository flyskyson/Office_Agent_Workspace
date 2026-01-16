#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown 导出器

将 JSON 记忆导出为 Markdown 文件，提供人类友好的阅读格式。

作者: Claude Code
日期: 2026-01-15
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

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
# Markdown 导出器
# ============================================================================

class MarkdownExporter:
    """将记忆导出为 Markdown 格式"""

    def __init__(self, workspace_root: Path = None):
        self.memory = ClaudeMemory(workspace_root)
        self.workspace_root = workspace_root or Path.cwd()
        self.memory_dir = self.workspace_root / "06_Learning_Journal" / "claude_memory"
        self.output_dir = self.workspace_root / "06_Learning_Journal" / "markdown_exports"

        # 确保输出目录存在
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export_all(self) -> Dict[str, str]:
        """导出所有记忆为 Markdown"""
        results = {}

        results['task_plan'] = self.export_task_plan()
        results['findings'] = self.export_findings()
        results['progress'] = self.export_progress()

        return results

    def export_task_plan(self) -> str:
        """导出任务计划（task_plan.md）

        包含：
        - 角色定义
        - 用户偏好
        - 高优先级记忆
        """
        lines = []

        # 标题
        lines.append("# 🎯 Claude Code 任务计划\n")
        lines.append(f"**更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        lines.append("---\n")

        # 1. 角色定义
        lines.append("## 🤖 我的角色\n")
        role_contexts = self.memory.recall("Claude Code核心角色定义")
        if role_contexts:
            ctx = role_contexts[0]
            lines.append(f"> {ctx['summary']}\n")
            lines.append("\n### 三大核心\n")
            for point in ctx['key_points']:
                lines.append(f"{point}\n")
        else:
            lines.append("角色定义未找到\n")

        lines.append("\n---\n")

        # 2. 用户偏好
        lines.append("## 📝 您的工作偏好\n")
        prefs = self.memory.store.memory.get('preferences', {})

        work_style = prefs.get('work_style_priority', {})
        if work_style:
            lines.append("- **优先方向**: " + work_style.get('primary_focus', '未设置') + "\n")
            lines.append("- **主动性**: " + work_style.get('proactivity_level', '未设置') + "\n")
            lines.append("- **失败观**: " + work_style.get('failure_attitude', '未设置') + "\n")
            lines.append("- **交流方式**: " + work_style.get('communication_preference', '未设置') + "\n")
        else:
            lines.append("用户偏好未设置\n")

        lines.append("\n---\n")

        # 3. 高优先级记忆
        lines.append("## ⭐ 高优先级记忆\n")
        high_priority = self.memory.recall_high_priority(limit=20)

        if high_priority:
            for i, ctx in enumerate(high_priority, 1):
                lines.append(f"\n### {i}. {ctx['topic']}\n")
                lines.append(f"{ctx['summary']}\n")

                if ctx.get('tags'):
                    tags_str = ' '.join([f'#{tag}' for tag in ctx['tags']])
                    lines.append(f"**标签**: {tags_str}\n")
        else:
            lines.append("暂无高优先级记忆\n")

        # 保存文件
        output_file = self.output_dir / "task_plan.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)

        return str(output_file)

    def export_findings(self) -> str:
        """导出发现和知识（findings.md）

        包含：
        - 项目知识
        - 决策经验
        - 学习成果
        """
        lines = []

        # 标题
        lines.append("# 📚 发现与知识\n")
        lines.append(f"**更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        lines.append("---\n")

        # 1. 项目知识
        lines.append("## 🎯 项目知识\n")
        projects = self.memory.store.memory.get('projects', {})
        project_knowledge = projects.get('project_knowledge', {})

        if project_knowledge:
            for project_name, info in project_knowledge.items():
                lines.append(f"\n### {project_name}\n")
                if isinstance(info, dict):
                    for key, value in info.items():
                        lines.append(f"- **{key}**: {value}\n")
                else:
                    lines.append(f"{info}\n")
        else:
            lines.append("暂无项目知识\n")

        lines.append("\n---\n")

        # 2. 决策经验
        lines.append("## 💡 决策经验\n")
        decisions = self.memory.store.memory.get('decisions', {}).get('decisions', [])

        # 只显示成功的决策
        successful_decisions = [d for d in decisions if d.get('success', True)]

        if successful_decisions:
            # 按工具分组
            from collections import defaultdict
            by_tool = defaultdict(list)
            for dec in successful_decisions:
                tool = dec.get('tool_chosen', 'Unknown')
                by_tool[tool].append(dec)

            for tool, decs in sorted(by_tool.items()):
                lines.append(f"\n### {tool}\n")
                for dec in decs[-3:]:  # 只显示最近3条
                    lines.append(f"- **{dec.get('task_type', 'N/A')}**: {dec.get('lesson_learned', dec.get('reasoning', ''))}\n")
        else:
            lines.append("暂无决策经验\n")

        lines.append("\n---\n")

        # 3. 学习成果
        lines.append("## 🎓 学习成果\n")
        all_contexts = self.memory.store.memory.get('contexts', {}).get('contexts', [])

        # 提取包含"学习"或"进化"的上下文
        learning_contexts = [
            ctx for ctx in all_contexts
            if '学习' in ctx.get('topic', '') or '进化' in ctx.get('topic', '') or '实现' in ctx.get('topic', '')
        ]

        if learning_contexts:
            for ctx in learning_contexts[-5:]:  # 最近5条
                lines.append(f"\n### {ctx['topic']}\n")
                lines.append(f"{ctx['summary']}\n")

                key_points = ctx.get('key_points', [])
                if key_points:
                    lines.append("\n**关键点**:\n")
                    for point in key_points[:3]:  # 前3个
                        lines.append(f"- {point}\n")
        else:
            lines.append("暂无学习成果\n")

        # 保存文件
        output_file = self.output_dir / "findings.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)

        return str(output_file)

    def export_progress(self) -> str:
        """导出进度日志（progress.md）

        包含：
        - 最近活动
        - 记忆统计
        - 性能指标
        """
        lines = []

        # 标题
        lines.append("# 📊 进度日志\n")
        lines.append(f"**更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        lines.append("---\n")

        # 1. 最近活动
        lines.append("## 📅 最近活动\n")
        recent = self.memory.recall_recent(limit=10)

        if recent:
            for ctx in recent:
                timestamp = ctx.get('timestamp', '')[:10]
                topic = ctx.get('topic', 'N/A')
                summary = ctx.get('summary', '')[:80]

                priority_icon = "⭐" if ctx.get('priority') == 'high' else "📝"
                lines.append(f"\n### {timestamp} {priority_icon} {topic}\n")
                lines.append(f"{summary}...\n")
        else:
            lines.append("暂无最近活动\n")

        lines.append("\n---\n")

        # 2. 记忆统计
        lines.append("## 📈 记忆统计\n")
        stats = self.memory.get_memory_stats()

        lines.append(f"- **上下文**: {stats['total_contexts']} 条\n")
        lines.append(f"- **决策**: {stats['total_decisions']} 条\n")
        lines.append(f"- **对话**: {stats['total_conversations']} 条\n")
        lines.append(f"- **记忆大小**: {stats['memory_size_kb']:.1f} KB\n")

        topics = stats.get('topics_covered', [])
        if topics:
            lines.append(f"\n**涵盖主题** ({len(topics)} 个):\n")
            for topic in topics[:10]:
                count = self.memory.store.memory['contexts']['contexts_by_topic'].get(topic, 0)
                lines.append(f"- {topic} ({count} 次)\n")

        lines.append("\n---\n")

        # 3. 性能指标
        lines.append("## ⚡ 性能指标\n")

        try:
            from memory_monitor import MemoryMonitor
            monitor = MemoryMonitor(self.workspace_root)
            perf = monitor.monitor_all()

            lines.append(f"- **加载时间**: {perf['load_time']['time_ms']} ms\n")
            lines.append(f"- **搜索时间**: {perf['search_time']['avg_time_ms']} ms\n")
            lines.append(f"- **记忆大小**: {perf['memory_size']['total_kb']} KB\n")
            lines.append(f"- **记录数量**: {perf['record_count']['total']} 条\n")
            lines.append(f"\n**状态**: {perf['load_time']['status']}\n")
        except Exception as e:
            lines.append(f"性能监控不可用: {e}\n")

        lines.append("\n---\n")

        # 4. 待办事项
        lines.append("## ✅ 待办事项\n")
        lines.append("基于当前记忆，建议关注：\n")

        # 检查是否有未完成的任务
        incomplete = [
            ctx for ctx in recent
            if 'TODO' in ctx.get('topic', '') or '待办' in ctx.get('topic', '')
        ]

        if incomplete:
            for ctx in incomplete[:5]:
                lines.append(f"- [ ] {ctx['topic']}: {ctx['summary'][:60]}...\n")
        else:
            lines.append("暂无待办事项\n")

        # 保存文件
        output_file = self.output_dir / "progress.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)

        return str(output_file)


# ============================================================================
# 便捷函数
# ============================================================================

def export_to_markdown() -> Dict[str, str]:
    """导出所有记忆为 Markdown（便捷函数）"""
    exporter = MarkdownExporter()
    return exporter.export_all()


# ============================================================================
# 命令行入口
# ============================================================================

def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description='将记忆导出为 Markdown')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='安静模式')

    args = parser.parse_args()

    if not args.quiet:
        print("\n" + "=" * 70)
        print("📝 导出记忆为 Markdown")
        print("=" * 70)

    exporter = MarkdownExporter()
    results = exporter.export_all()

    if not args.quiet:
        print("\n✅ 导出完成:")
        for name, path in results.items():
            print(f"   - {name}: {path}")
        print("\n" + "=" * 70)

    return 0


if __name__ == "__main__":
    sys.exit(main())
