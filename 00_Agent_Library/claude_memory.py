#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Claude Code 记忆持久化系统

让Claude Code拥有跨会话的持久化记忆能力：
1. 上下文记忆 - 记住每次对话的上下文
2. 决策记忆 - 记住工具选择和决策逻辑
3. 用户偏好 - 记住用户的习惯和偏好
4. 项目知识 - 记住项目特定的知识
5. 演进轨迹 - 记住系统和项目的演进

作者: Claude Code
日期: 2026-01-15
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import defaultdict

# Windows 终端编码修复
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass


# ============================================================================
# 记忆存储
# ============================================================================

class MemoryStore:
    """记忆存储 - 持久化Claude Code的所有记忆"""

    def __init__(self, workspace_root: Path):
        self.workspace_root = Path(workspace_root)
        self.memory_dir = self.workspace_root / "06_Learning_Journal" / "claude_memory"

        # 确保目录存在
        self.memory_dir.mkdir(parents=True, exist_ok=True)

        # 记忆文件
        self.files = {
            'contexts': self.memory_dir / "contexts.json",      # 上下文记忆
            'decisions': self.memory_dir / "decisions.json",    # 决策记忆
            'preferences': self.memory_dir / "preferences.json", # 用户偏好
            'projects': self.memory_dir / "projects.json",      # 项目知识
            'evolution': self.memory_dir / "evolution.json",    # 演进轨迹
            'conversations': self.memory_dir / "conversations.json" # 对话历史
        }

        # 加载记忆
        self.memory = self._load_all()

    def _load_all(self) -> Dict[str, Any]:
        """加载所有记忆"""
        memory = {}
        for key, path in self.files.items():
            if path.exists():
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        memory[key] = json.load(f)
                except Exception as e:
                    print(f"⚠️ 加载 {key} 失败: {e}")
                    memory[key] = self._get_default_structure(key)
            else:
                memory[key] = self._get_default_structure(key)
        return memory

    def _get_default_structure(self, memory_type: str) -> Any:
        """获取默认结构"""
        defaults = {
            'contexts': {
                'total_contexts': 0,
                'contexts_by_topic': defaultdict(int),
                'contexts': []
            },
            'decisions': {
                'total_decisions': 0,
                'tool_usage_stats': defaultdict(int),
                'decisions': []
            },
            'preferences': {
                'coding_style': {},
                'preferred_tools': {},
                'communication_style': {},
                'frequently_used_commands': {}
            },
            'projects': {
                'active_projects': [],
                'project_knowledge': {},
                'project_patterns': {}
            },
            'evolution': {
                'version_history': [],
                'capability_changes': [],
                'milestones': []
            },
            'conversations': {
                'total_conversations': 0,
                'conversations': []
            }
        }
        return defaults.get(memory_type, {})

    def save(self, memory_type: str = None):
        """保存记忆"""
        if memory_type:
            self._save_one(memory_type)
        else:
            for key in self.files.keys():
                self._save_one(key)

    def _save_one(self, memory_type: str):
        """保存单个记忆类型"""
        if memory_type not in self.files:
            return

        path = self.files[memory_type]
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self.memory[memory_type], f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ 保存 {memory_type} 失败: {e}")

    def add_context(self, context: Dict[str, Any]):
        """添加上下文记忆"""
        ctx = {
            'timestamp': datetime.now().isoformat(),
            'session_id': context.get('session_id', ''),
            'topic': context.get('topic', ''),
            'summary': context.get('summary', ''),
            'key_points': context.get('key_points', []),
            'tools_used': context.get('tools_used', []),
            'decisions_made': context.get('decisions_made', []),
            'outcomes': context.get('outcomes', '')
        }

        self.memory['contexts']['contexts'].append(ctx)
        self.memory['contexts']['total_contexts'] += 1

        # 统计主题
        topic = context.get('topic', 'unknown')
        if topic not in self.memory['contexts']['contexts_by_topic']:
            self.memory['contexts']['contexts_by_topic'][topic] = 0
        self.memory['contexts']['contexts_by_topic'][topic] += 1

        self.save('contexts')

    def add_decision(self, decision: Dict[str, Any]):
        """添加决策记忆"""
        dec = {
            'timestamp': datetime.now().isoformat(),
            'task_type': decision.get('task_type', ''),
            'tool_chosen': decision.get('tool_chosen', ''),
            'alternatives': decision.get('alternatives', []),
            'reasoning': decision.get('reasoning', ''),
            'success': decision.get('success', True),
            'lesson_learned': decision.get('lesson_learned', '')
        }

        self.memory['decisions']['decisions'].append(dec)
        self.memory['decisions']['total_decisions'] += 1

        # 统计工具使用
        tool = decision.get('tool_chosen', '')
        if tool:
            if tool not in self.memory['decisions']['tool_usage_stats']:
                self.memory['decisions']['tool_usage_stats'][tool] = 0
            self.memory['decisions']['tool_usage_stats'][tool] += 1

        self.save('decisions')

    def update_preferences(self, preferences: Dict[str, Any]):
        """更新用户偏好"""
        for key, value in preferences.items():
            if key in self.memory['preferences']:
                if isinstance(value, dict):
                    self.memory['preferences'][key].update(value)
                else:
                    self.memory['preferences'][key] = value

        self.save('preferences')

    def add_conversation(self, conversation: Dict[str, Any]):
        """添加对话记录"""
        conv = {
            'timestamp': datetime.now().isoformat(),
            'session_id': conversation.get('session_id', ''),
            'user_query': conversation.get('user_query', ''),
            'my_response': conversation.get('my_response', ''),
            'tools_used': conversation.get('tools_used', []),
            'outcome': conversation.get('outcome', ''),
            'user_satisfaction': conversation.get('user_satisfaction', None),
            'follow_up_actions': conversation.get('follow_up_actions', [])
        }

        self.memory['conversations']['conversations'].append(conv)
        self.memory['conversations']['total_conversations'] += 1

        self.save('conversations')

    def get_relevant_contexts(self, topic: str, limit: int = 5) -> List[Dict]:
        """获取相关的上下文"""
        contexts = self.memory['contexts']['contexts']

        # 简单的关键词匹配（实际应该用语义搜索）
        relevant = []
        for ctx in contexts:
            if topic.lower() in ctx.get('topic', '').lower() or \
               topic.lower() in ctx.get('summary', '').lower():
                relevant.append(ctx)
                if len(relevant) >= limit:
                    break

        return relevant

    def get_tool_preferences(self, task_type: str) -> Optional[str]:
        """获取工具偏好"""
        # 从决策历史中学习
        decisions = self.memory['decisions']['decisions']

        # 统计该任务类型下最常用的工具
        tool_counts = defaultdict(int)
        for dec in decisions:
            if dec.get('task_type') == task_type and dec.get('success'):
                tool = dec.get('tool_chosen', '')
                tool_counts[tool] += 1

        if tool_counts:
            return max(tool_counts.items(), key=lambda x: x[1])[0]
        return None

    def get_statistics(self) -> Dict[str, Any]:
        """获取记忆统计"""
        return {
            'total_contexts': self.memory['contexts']['total_contexts'],
            'total_decisions': self.memory['decisions']['total_decisions'],
            'total_conversations': self.memory['conversations']['total_conversations'],
            'topics_covered': list(self.memory['contexts']['contexts_by_topic'].keys()),
            'most_used_tools': dict(self.memory['decisions']['tool_usage_stats']),
            'memory_size_kb': sum(f.stat().st_size for f in self.files.values() if f.exists()) / 1024
        }


# ============================================================================
# 记忆管理器
# ============================================================================

class ClaudeMemory:
    """Claude Code 记忆管理器"""

    def __init__(self, workspace_root: Optional[Path] = None):
        if workspace_root is None:
            # 自动检测工作区根目录
            workspace_root = Path(__file__).parent.parent

        self.store = MemoryStore(workspace_root)
        self.current_session = self._generate_session_id()

    def _generate_session_id(self) -> str:
        """生成会话ID"""
        return f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    def remember_context(self, topic: str, summary: str, key_points: List[str],
                        tools_used: List[str], decisions_made: List[str],
                        outcomes: str):
        """记住对话上下文"""
        context = {
            'session_id': self.current_session,
            'topic': topic,
            'summary': summary,
            'key_points': key_points,
            'tools_used': tools_used,
            'decisions_made': decisions_made,
            'outcomes': outcomes
        }
        self.store.add_context(context)

    def remember_decision(self, task_type: str, tool_chosen: str,
                         alternatives: List[str], reasoning: str,
                         success: bool, lesson_learned: str = ""):
        """记住决策"""
        decision = {
            'task_type': task_type,
            'tool_chosen': tool_chosen,
            'alternatives': alternatives,
            'reasoning': reasoning,
            'success': success,
            'lesson_learned': lesson_learned
        }
        self.store.add_decision(decision)

    def remember_conversation(self, user_query: str, my_response: str,
                            tools_used: List[str], outcome: str):
        """记住对话"""
        conversation = {
            'session_id': self.current_session,
            'user_query': user_query,
            'my_response': my_response,
            'tools_used': tools_used,
            'outcome': outcome
        }
        self.store.add_conversation(conversation)

    def recall(self, topic: str) -> List[Dict]:
        """回忆相关上下文"""
        return self.store.get_relevant_contexts(topic)

    def suggest_tool(self, task_type: str) -> Optional[str]:
        """基于历史建议工具"""
        return self.store.get_tool_preferences(task_type)

    def learn_preferences(self, preferences: Dict[str, Any]):
        """学习用户偏好"""
        self.store.update_preferences(preferences)

    def get_memory_stats(self) -> Dict[str, Any]:
        """获取记忆统计"""
        return self.store.get_statistics()

    def print_memory_summary(self):
        """打印记忆摘要"""
        stats = self.get_memory_stats()

        print("\n" + "=" * 70)
        print("🧠 Claude Code 记忆系统")
        print("=" * 70)

        print(f"\n📊 统计信息:")
        print(f"   - 对话上下文: {stats['total_contexts']} 条")
        print(f"   - 决策记录: {stats['total_decisions']} 条")
        print(f"   - 对话历史: {stats['total_conversations']} 条")
        print(f"   - 记忆占用: {stats['memory_size_kb']:.1f} KB")

        if stats['topics_covered']:
            print(f"\n📚 涵盖主题:")
            for topic in list(stats['topics_covered'])[:10]:
                count = self.store.memory['contexts']['contexts_by_topic'][topic]
                print(f"   - {topic} ({count} 次)")

        if stats['most_used_tools']:
            print(f"\n🛠️ 常用工具:")
            for tool, count in sorted(stats['most_used_tools'].items(),
                                     key=lambda x: x[1], reverse=True)[:5]:
                print(f"   - {tool} ({count} 次)")

        print("\n" + "=" * 70)


# ============================================================================
# 记忆增强Agent
# ============================================================================

class MemoryEnhancedAgent:
    """
    记忆增强的Agent基类

    任何继承此类的Agent都将获得持久化记忆能力
    """

    def __init__(self, workspace_root: Optional[Path] = None):
        self.memory = ClaudeMemory(workspace_root)

    def recall_before_action(self, topic: str) -> List[Dict]:
        """在行动前回忆相关经验"""
        return self.memory.recall(topic)

    def learn_from_action(self, task_type: str, tool_used: str,
                         reasoning: str, success: bool):
        """从行动中学习"""
        self.memory.remember_decision(
            task_type=task_type,
            tool_chosen=tool_used,
            alternatives=[],
            reasoning=reasoning,
            success=success,
            lesson_learned=f"使用{tool_used}{'成功' if success else '失败'}"
        )

    def suggest_based_on_experience(self, task_type: str) -> Optional[str]:
        """基于经验建议工具"""
        return self.memory.suggest_tool(task_type)

    # 代理ClaudeMemory的其他方法
    def remember_context(self, topic: str, summary: str, key_points: List[str],
                        tools_used: List[str], decisions_made: List[str],
                        outcomes: str):
        """记住对话上下文"""
        self.memory.remember_context(topic, summary, key_points, tools_used, decisions_made, outcomes)

    def remember_conversation(self, user_query: str, my_response: str,
                            tools_used: List[str], outcome: str):
        """记住对话"""
        self.memory.remember_conversation(user_query, my_response, tools_used, outcome)

    def learn_preferences(self, preferences: Dict[str, Any]):
        """学习用户偏好"""
        self.memory.learn_preferences(preferences)

    def get_memory_stats(self) -> Dict[str, Any]:
        """获取记忆统计"""
        return self.memory.get_memory_stats()

    # 代理ClaudeMemory的recall方法
    def recall(self, topic: str) -> List[Dict]:
        """回忆相关上下文"""
        return self.memory.recall(topic)


# ============================================================================
# 演示程序
# ============================================================================

def demo_memory_system():
    """演示记忆系统"""

    print("""
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║              Claude Code 记忆持久化系统演示                         ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
    """)

    # 创建记忆系统
    memory = ClaudeMemory()

    print("\n📝 模拟学习过程...")
    print("-" * 70)

    # 模拟1: 学习文件读取偏好
    print("\n1️⃣ 学习: 文件读取任务")
    memory.remember_decision(
        task_type="read_file",
        tool_chosen="Read",
        alternatives=["Bash: cat", "Grep"],
        reasoning="Read工具是专门为文件读取设计的，更快更准确",
        success=True,
        lesson_learned="优先使用Read工具读取文件"
    )

    # 模拟2: 学习代码搜索偏好
    print("2️⃣ 学习: 代码搜索任务")
    memory.remember_decision(
        task_type="search_code",
        tool_chosen="Grep",
        alternatives=["Glob", "Task: Explore"],
        reasoning="Grep支持正则表达式，适合精确搜索",
        success=True
    )

    # 模拟3: 记住对话上下文
    print("3️⃣ 学习: 多Agent系统对话")
    memory.remember_context(
        topic="多Agent系统开发",
        summary="创建了基于WorkflowEngine的多Agent演示系统",
        key_points=[
            "实现了4个专门Agent：Coordinator, Analyst, Processor, Reviewer",
            "使用WorkflowGraph进行工作流编排",
            "状态在Agent之间传递"
        ],
        tools_used=["Write", "Bash", "Read"],
        decisions_made=["使用workflow_engine而非LangGraph", "选择串行协作模式"],
        outcomes="成功运行演示，展示了Agent协作能力"
    )

    # 模拟4: 记住用户偏好
    print("4️⃣ 学习: 用户偏好")
    memory.learn_preferences({
        'coding_style': {
            'language': 'Python',
            'naming_convention': 'snake_case'
        },
        'preferred_tools': {
            'file_operations': 'Read/Edit/Write专用工具'
        }
    })

    # 模拟5: 记住对话
    print("5️⃣ 学习: 对话历史")
    memory.remember_conversation(
        user_query="演示一个简单的多Agent系统原型？",
        my_response="创建了multi_agent_demo.py，包含4个Agent...",
        tools_used=["Write", "Bash", "Read"],
        outcome="成功演示了多Agent协作"
    )

    # 显示记忆摘要
    print("\n" + "=" * 70)
    print("📊 记忆系统学习完成")
    print("=" * 70)
    memory.print_memory_summary()

    # 演示回忆
    print("\n🔮 演示记忆回忆...")
    print("-" * 70)

    print("\n💭 回忆: 关于'多Agent'的上下文")
    contexts = memory.recall("多Agent")
    for ctx in contexts:
        print(f"\n   时间: {ctx['timestamp']}")
        print(f"   主题: {ctx['topic']}")
        print(f"   摘要: {ctx['summary']}")

    print("\n🛠️ 建议: 基于经验，文件读取应该用")
    suggested = memory.suggest_tool("read_file")
    print(f"   → {suggested or '无历史数据'}")

    print("\n" + "=" * 70)
    print("✅ 演示完成！")
    print("\n💡 说明:")
    print("   - 所有记忆已保存到: 06_Learning_Journal/claude_memory/")
    print("   - 下次会话可以继续使用这些记忆")
    print("   - 记忆会持续累积和进化")
    print("=" * 70)


if __name__ == "__main__":
    demo_memory_system()
