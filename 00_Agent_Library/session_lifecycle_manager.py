#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
会话生命周期管理器 (Session Lifecycle Manager)

让Claude Code拥有"生命"：
- 会话开始时：主动加载记忆和上下文
- 会话进行中：实时提炼和保存关键信息
- 会话结束时：总结、反思、学习、进化

这是让记忆系统"活"起来的核心组件！

作者: Claude Code
日期: 2026-01-16
版本: v1.0.0
哲学: 不止是工具，而是协作伙伴
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import traceback

# Windows 终端编码修复
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass


# ============================================================================
# 会话生命周期管理器
# ============================================================================

class SessionLifecycleManager:
    """
    会话生命周期管理器

    职责:
    1. 会话初始化 - 加载记忆、理解上下文
    2. 实时学习 - 提炼关键信息、更新用户画像
    3. 会话总结 - 反思、学习、进化
    4. 记忆触发 - 主动发现相关知识
    """

    def __init__(self, workspace_root: Path):
        self.workspace_root = Path(workspace_root)

        # 导入现有模块
        sys.path.insert(0, str(self.workspace_root / "00_Agent_Library"))
        from claude_memory import ClaudeMemory
        from auto_learner import AutoLearner

        # 核心组件
        self.memory = ClaudeMemory()
        self.learner = AutoLearner(workspace_root)

        # 会话状态
        self.session_id = self._generate_session_id()
        self.session_start_time = datetime.now()
        self.conversation_count = 0
        self.key_moments = []  # 关键时刻（高重要性对话）

        # 上下文理解
        self.current_context = {
            'project': None,
            'topic': None,
            'tech_stack': [],
            'user_goal': None
        }

    def _generate_session_id(self) -> str:
        """生成会话ID"""
        now = datetime.now()
        return f"session_{now.strftime('%Y%m%d_%H%M%S')}"

    # ========================================================================
    # 阶段1: 会话初始化
    # ========================================================================

    def session_start(self, user_first_message: str) -> Dict[str, Any]:
        """
        会话开始 - 第一步！理解用户和上下文

        这应该是每次新对话时的第一个调用：
        ```python
        manager = SessionLifecycleManager(workspace)
        context = manager.session_start("用户的第一条消息")
        # 现在我知道了：
        # - 用户的偏好
        # - 相关的历史记忆
        # - 可能的技术栈
        # - 用户的长期兴趣
        ```

        返回:
            {
                'session_id': str,
                'user_summary': str,  # 用户画像摘要
                'relevant_memories': List[Dict],  # 相关记忆
                'suggestions': List[str],  # 主动建议
                'context': Dict  # 当前上下文
            }
        """
        print(f"\n{'='*60}")
        print(f"🔄 会话开始: {self.session_id}")
        print(f"{'='*60}\n")

        # 1. 分析第一条消息，理解意图
        intent_analysis = self._analyze_first_message(user_first_message)

        # 2. 加载用户画像
        user_profile = self.learner.user_profile
        user_summary = self.learner.get_user_summary()

        # 3. 搜索相关记忆
        relevant_memories = self._search_relevant_memories(
            user_first_message, intent_analysis
        )

        # 4. 生成主动建议
        suggestions = self._generate_proactive_suggestions(
            intent_analysis, user_profile, relevant_memories
        )

        # 5. 更新当前上下文
        self.current_context.update({
            'project': intent_analysis.get('project'),
            'topic': intent_analysis.get('topic'),
            'tech_stack': intent_analysis.get('tech_stack', []),
            'user_goal': intent_analysis.get('goal')
        })

        # 6. 记录会话开始
        self._log_session_start(user_first_message, intent_analysis)

        result = {
            'session_id': self.session_id,
            'user_summary': user_summary,
            'relevant_memories': relevant_memories[:5],  # 最多5条
            'suggestions': suggestions,
            'context': self.current_context
        }

        print(f"✅ 会话初始化完成")
        print(f"📊 用户画像: {user_profile.get('name', 'User')}")
        print(f"🧠 相关记忆: {len(relevant_memories)} 条")
        print(f"💡 主动建议: {len(suggestions)} 条\n")

        return result

    def _analyze_first_message(self, message: str) -> Dict[str, Any]:
        """分析第一条消息，理解意图"""
        from auto_learner import ConversationDistiller
        distiller = ConversationDistiller()

        analysis = {
            'intent': distiller._extract_intent(message),
            'tech_stack': distiller._extract_tech_stack(message),
            'preferences': distiller._extract_preferences(message),
            'goal': self._extract_goal(message),
            'project': self._infer_project(message),
            'topic': self._infer_topic(message)
        }

        return analysis

    def _extract_goal(self, message: str) -> Optional[str]:
        """提取用户目标"""
        # 简单实现：寻找关键词
        if any(word in message for word in ['创建', '添加', '实现', '开发']):
            return 'create'
        elif any(word in message for word in ['修复', '解决', '调试']):
            return 'fix'
        elif any(word in message for word in ['学习', '了解', '查看']):
            return 'learn'
        elif any(word in message for word in ['更新', '升级', '改进']):
            return 'improve'
        return None

    def _infer_project(self, message: str) -> Optional[str]:
        """推断项目名称"""
        # 从消息中提取项目名称
        projects = {
            '市场监管': 'market_supervision_agent',
            '记忆助手': 'memory_agent',
            '训练系统': 'ai_agent_training_system',
            '工作流': 'workflow_engine',
            '记忆系统': 'claude_memory'
        }

        for keyword, project in projects.items():
            if keyword in message:
                return project

        return None

    def _infer_topic(self, message: str) -> Optional[str]:
        """推断主题"""
        topics = {
            '记忆': 'memory_system',
            '工作流': 'workflow',
            'Agent': 'multi_agent',
            '学习': 'learning',
            '进化': 'evolution'
        }

        for keyword, topic in topics.items():
            if keyword in message:
                return topic

        return None

    def _search_relevant_memories(self, query: str,
                                   intent_analysis: Dict) -> List[Dict]:
        """搜索相关记忆"""
        relevant = []

        # 1. 从语义记忆搜索
        try:
            semantic_results = self.memory.semantic_search(
                query, top_k=5
            )
            relevant.extend([
                {
                    'type': 'semantic',
                    'topic': r.get('topic', 'unknown'),
                    'summary': r.get('summary', '')[:100],
                    'relevance': r.get('similarity', 0.0)
                }
                for r in semantic_results
            ])
        except Exception as e:
            print(f"⚠️ 语义搜索失败: {e}")

        # 2. 使用混合搜索
        try:
            hybrid_results = self.memory.hybrid_search(
                query, top_k=5
            )
            for r in hybrid_results:
                if r.get('similarity', 0) > 0.5:
                    relevant.append({
                        'type': 'hybrid',
                        'topic': r.get('topic', 'unknown'),
                        'summary': r.get('summary', '')[:100],
                        'relevance': r.get('similarity', 0.0) * 0.9
                    })
        except Exception as e:
            print(f"⚠️ 混合搜索失败: {e}")

        # 按相关性排序
        relevant.sort(key=lambda x: x.get('relevance', 0), reverse=True)

        return relevant[:10]

    def _generate_proactive_suggestions(self, intent_analysis: Dict,
                                        user_profile: Dict,
                                        memories: List[Dict]) -> List[str]:
        """生成主动建议"""
        suggestions = []

        # 基于意图的建议
        intent = intent_analysis.get('intent', '')
        if intent == 'create_feature':
            suggestions.append("使用想法落地工作流来规划新功能")
        elif intent == 'debug_problem':
            suggestions.append("检查相关的错误记忆和解决方案")

        # 基于用户偏好的建议
        if user_profile['preferences'].get('detail_level') == 'high':
            suggestions.append("提供详细的解释和步骤说明")

        # 基于历史记忆的建议
        if len(memories) > 0:
            suggestions.append(f"参考 {len(memories)} 条相关历史记忆")

        # 基于技术栈的建议
        tech_stack = intent_analysis.get('tech_stack', [])
        if 'frameworks:LangGraph' in tech_stack:
            suggestions.append("使用 LangGraph 工作流引擎")

        return suggestions[:5]

    def _log_session_start(self, first_message: str, analysis: Dict):
        """记录会话开始"""
        log_entry = {
            'session_id': self.session_id,
            'timestamp': self.session_start_time.isoformat(),
            'first_message': first_message,
            'intent': analysis.get('intent'),
            'context': self.current_context
        }

        log_file = self.workspace_root / "06_Learning_Journal" / "auto_learning" / "session_log.jsonl"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')

    # ========================================================================
    # 阶段2: 实时学习
    # ========================================================================

    def on_conversation(self, user_query: str, assistant_response: str,
                       tools_used: List[str]) -> Dict[str, Any]:
        """
        每次对话后调用 - 实时学习

        这应该在每次对话结束后调用：
        ```python
        result = manager.on_conversation(
            user_query="用户的问题",
            assistant_response="我的回答",
            tools_used=["Read", "Write"]
        )
        ```

        返回:
            {
                'learned': bool,
                'importance_score': float,
                'insights_extracted': int,
                'should_remember': bool
            }
        """
        self.conversation_count += 1

        # 1. 提炼对话
        distilled = self.learner.distiller.distill(
            user_query, assistant_response, tools_used, self.current_context
        )

        # 2. 判断是否重要
        importance = distilled['importance_score']
        is_important = importance > 50  # 阈值

        if is_important:
            self.key_moments.append({
                'conversation_num': self.conversation_count,
                'timestamp': datetime.now().isoformat(),
                'importance': importance,
                'intent': distilled['intent'],
                'insights': distilled['insights']
            })

        # 3. 学习（只对重要的对话进行深度学习）
        if is_important:
            self.learner.learn_from_conversation(
                user_query, assistant_response, tools_used, self.current_context
            )

        # 4. 更新上下文
        self.current_context['tech_stack'].extend(distilled['tech_stack'])
        self.current_context['tech_stack'] = list(set(self.current_context['tech_stack']))

        return {
            'learned': is_important,
            'importance_score': importance,
            'insights_extracted': len(distilled['insights']),
            'should_remember': is_important
        }

    # ========================================================================
    # 阶段3: 会话总结
    # ========================================================================

    def session_end(self, final_summary: str = None) -> Dict[str, Any]:
        """
        会话结束 - 总结、反思、进化

        这应该在会话结束时调用：
        ```python
        report = manager.session_end()
        # 生成完整的学习报告
        ```

        返回:
            {
                'session_summary': str,
                'key_learnings': List[str],
                'user_insights': Dict,
                'evolution_metrics': Dict,
                'recommendations': List[str]
            }
        """
        print(f"\n{'='*60}")
        print(f"🎬 会话结束: {self.session_id}")
        print(f"{'='*60}\n")

        session_duration = (datetime.now() - self.session_start_time).total_seconds()

        # 1. 生成会话总结
        session_summary = self._generate_session_summary(session_duration)

        # 2. 提取关键学习
        key_learnings = self._extract_key_learnings()

        # 3. 分析用户洞察
        user_insights = self._analyze_user_insights()

        # 4. 计算进化指标
        evolution_metrics = self._calculate_evolution_metrics()

        # 5. 生成建议
        recommendations = self._generate_recommendations()

        # 6. 保存会话报告
        report = {
            'session_id': self.session_id,
            'timestamp': datetime.now().isoformat(),
            'duration_seconds': session_duration,
            'conversation_count': self.conversation_count,
            'key_moments_count': len(self.key_moments),
            'session_summary': session_summary,
            'key_learnings': key_learnings,
            'user_insights': user_insights,
            'evolution_metrics': evolution_metrics,
            'recommendations': recommendations
        }

        self._save_session_report(report)
        self._update_evolution_log(report)

        print(f"📊 会话统计:")
        print(f"  - 对话数: {self.conversation_count}")
        print(f"  - 关键时刻: {len(self.key_moments)}")
        print(f"  - 时长: {session_duration:.0f} 秒")
        print(f"\n✅ 会话总结完成\n")

        return report

    def _generate_session_summary(self, duration: float) -> str:
        """生成会话总结"""
        summary_parts = [
            f"会话 {self.session_id} 持续 {duration:.0f} 秒",
            f"包含 {self.conversation_count} 次对话",
            f"识别了 {len(self.key_moments)} 个关键时刻"
        ]

        if self.key_moments:
            top_moment = max(self.key_moments, key=lambda x: x['importance'])
            summary_parts.append(
                f"最高重要性: {top_moment['importance']:.0f} "
                f"({top_moment['intent']})"
            )

        return "；".join(summary_parts) + "。"

    def _extract_key_learnings(self) -> List[str]:
        """提取关键学习"""
        learnings = []

        # 从关键时刻提取
        for moment in self.key_moments:
            if moment['importance'] > 70:
                learnings.append(
                    f"[{moment['intent']}] "
                    f"重要性 {moment['importance']:.0f}: "
                    f"{', '.join(moment['insights'][:2])}"
                )

        return learnings[:5]

    def _analyze_user_insights(self) -> Dict[str, Any]:
        """分析用户洞察"""
        profile = self.learner.user_profile
        progress = self.learner.learning_progress

        return {
            'communication_style': profile['preferences'].get('communication_style', []),
            'detail_level_preference': profile['preferences'].get('detail_level', 'medium'),
            'top_interests': profile['interests'][:5],
            'skill_growth': self._get_top_skills(progress),
            'conversation_patterns': self._analyze_patterns()
        }

    def _get_top_skills(self, progress: Dict) -> List[Tuple[str, float]]:
        """获取成长最快的技能"""
        skills = progress.get('skill_levels', {})
        return sorted(skills.items(), key=lambda x: x[1], reverse=True)[:5]

    def _analyze_patterns(self) -> Dict[str, Any]:
        """分析对话模式"""
        if not self.key_moments:
            return {}

        intent_counts = {}
        for moment in self.key_moments:
            intent = moment['intent']
            intent_counts[intent] = intent_counts.get(intent, 0) + 1

        return {
            'top_intent': max(intent_counts.items(), key=lambda x: x[1])[0] if intent_counts else None,
            'intent_distribution': intent_counts
        }

    def _calculate_evolution_metrics(self) -> Dict[str, Any]:
        """计算进化指标"""
        progress = self.learner.learning_progress

        return {
            'total_conversations_learned': progress.get('total_conversations_learned', 0),
            'total_insights_extracted': progress.get('total_insights_extracted', 0),
            'knowledge_domains': len(progress.get('knowledge_domains', {})),
            'skill_diversity': len(progress.get('skill_levels', {})),
            'learning_velocity': len(self.key_moments) / max(self.conversation_count, 1)
        }

    def _generate_recommendations(self) -> List[str]:
        """生成建议"""
        recommendations = []

        # 基于学习速度
        velocity = len(self.key_moments) / max(self.conversation_count, 1)
        if velocity < 0.3:
            recommendations.append("考虑增加对话深度，提炼更多有价值的信息")

        # 基于技能多样性
        progress = self.learner.learning_progress
        if len(progress.get('skill_levels', {})) < 5:
            recommendations.append("尝试更多不同的技术栈，扩展技能覆盖")

        # 基于用户偏好
        profile = self.learner.user_profile
        if not profile['preferences'].get('communication_style'):
            recommendations.append("继续观察用户沟通偏好，提供个性化服务")

        return recommendations

    def _save_session_report(self, report: Dict):
        """保存会话报告"""
        report_dir = self.workspace_root / "06_Learning_Journal" / "auto_learning" / "session_reports"
        report_dir.mkdir(parents=True, exist_ok=True)

        report_file = report_dir / f"{self.session_id}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

    def _update_evolution_log(self, report: Dict):
        """更新进化日志"""
        evolution_log = self.workspace_root / "06_Learning_Journal" / "evolution_log.json"

        # 读取现有日志
        if evolution_log.exists():
            with open(evolution_log, 'r', encoding='utf-8') as f:
                log = json.load(f)
        else:
            log = {
                'total_sessions': 0,
                'sessions': [],
                'capabilities': [],
                'milestones': []
            }

        # 确保所有必需的键都存在
        if 'total_sessions' not in log:
            log['total_sessions'] = 0
        if 'sessions' not in log:
            log['sessions'] = []
        if 'capabilities' not in log:
            log['capabilities'] = []
        if 'milestones' not in log:
            log['milestones'] = []

        # 添加新会话
        log['total_sessions'] += 1
        log['sessions'].append({
            'session_id': report['session_id'],
            'timestamp': report['timestamp'],
            'conversation_count': report['conversation_count'],
            'key_learnings_count': len(report['key_learnings'])
        })

        # 更新能力
        for skill, level in report['user_insights'].get('skill_growth', []):
            log['capabilities'].append({
                'timestamp': report['timestamp'],
                'skill': skill,
                'level': level
            })

        # 保存
        with open(evolution_log, 'w', encoding='utf-8') as f:
            json.dump(log, f, ensure_ascii=False, indent=2)


# ============================================================================
# 便捷函数
# ============================================================================

def quick_session_start(workspace_root: Path, first_message: str) -> SessionLifecycleManager:
    """
    快速开始会话

    用法:
    ```python
    from session_lifecycle_manager import quick_session_start

    manager = quick_session_start(
        workspace_root=Path(__file__).parent.parent,
        first_message="我想添加一个新功能"
    )
    # 现在可以开始对话了
    ```
    """
    manager = SessionLifecycleManager(workspace_root)
    manager.session_start(first_message)
    return manager


# ============================================================================
# 主程序（测试）
# ============================================================================

def main():
    """测试会话生命周期管理器"""

    workspace_root = Path(__file__).parent.parent
    manager = SessionLifecycleManager(workspace_root)

    # 模拟一个完整会话
    print("\n" + "="*60)
    print("测试会话生命周期管理器")
    print("="*60)

    # 1. 会话开始
    first_message = "我想让Claude能够记住我的偏好，并且持续学习"
    init_result = manager.session_start(first_message)

    print("\n用户画像摘要:")
    print(init_result['user_summary'])

    print("\n相关记忆:")
    for mem in init_result['relevant_memories'][:3]:
        print(f"  - [{mem['type']}] {mem['topic']}: {mem['summary'][:50]}...")

    print("\n主动建议:")
    for suggestion in init_result['suggestions']:
        print(f"  💡 {suggestion}")

    # 2. 模拟对话
    conversations = [
        {
            'user': "帮我实现一个自动学习系统",
            'assistant': "好的，我来创建 auto_learner.py",
            'tools': ['Write', 'Read']
        },
        {
            'user': "现在它能自动运行吗？",
            'assistant': "需要手动调用，我们可以改进",
            'tools': ['Read']
        },
        {
            'user': "那就创建一个会话生命周期管理器吧",
            'assistant': "好主意！这样就能自动学习了",
            'tools': ['Write', 'Edit']
        }
    ]

    for conv in conversations:
        result = manager.on_conversation(
            conv['user'], conv['assistant'], conv['tools']
        )
        if result['learned']:
            print(f"\n✅ 已学习对话 (重要性: {result['importance_score']:.0f})")

    # 3. 会话结束
    report = manager.session_end()

    print("\n会话总结:")
    print(report['session_summary'])

    print("\n关键学习:")
    for learning in report['key_learnings']:
        print(f"  - {learning}")

    print("\n进化指标:")
    for key, value in report['evolution_metrics'].items():
        print(f"  - {key}: {value}")

    print("\n建议:")
    for rec in report['recommendations']:
        print(f"  💡 {rec}")


if __name__ == "__main__":
    main()
