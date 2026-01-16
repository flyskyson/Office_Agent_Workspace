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
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import defaultdict
import re

# Windows 终端编码修复
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass


# ============================================================================
# LangMem 风格增强功能
# ============================================================================

class ImportanceScorer:
    """
    重要性评分器 - LangMem 风格

    为记忆计算重要性分数 (0-100)，基于:
    - 关键词匹配度
    - 内容长度和质量
    - 时间新鲜度
    - 交互频率
    """

    # 高权重关键词（用户兴趣）
    HIGH_WEIGHT_KEYWORDS = [
        # 技术栈
        "LangGraph", "多Agent", "WorkflowEngine", "工作流引擎",
        "Playwright", "Jinja2", "ChromaDB", "Streamlit", "Flask",
        # 核心概念
        "记忆系统", "检查点", "状态管理", "可视化",
        "Supervisor", "Coordinator", "智能体",
        # 项目相关
        "市场监管", "记忆助手", "申请书生成",
        # 开发相关
        "架构设计", "最佳实践", "系统演进",
        "效率监控", "自动化", "工具集成"
    ]

    # 中等权重关键词
    MEDIUM_WEIGHT_KEYWORDS = [
        "Python", "JavaScript", "API", "数据库",
        "前端", "后端", "部署", "测试",
        "文档", "教程", "示例"
    ]

    def __init__(self):
        self.keyword_weights = self._build_keyword_weights()

    def _build_keyword_weights(self) -> Dict[str, float]:
        """构建关键词权重字典"""
        weights = {}
        for kw in self.HIGH_WEIGHT_KEYWORDS:
            weights[kw.lower()] = 3.0  # 高权重
        for kw in self.MEDIUM_WEIGHT_KEYWORDS:
            weights[kw.lower()] = 1.5  # 中权重
        return weights

    def calculate(self, memory: Dict[str, Any]) -> float:
        """
        计算记忆的重要性分数

        参数:
            memory: 记忆字典（包含 topic, summary, key_points 等）

        返回:
            重要性分数 (0-100)
        """
        score = 0.0

        # 1. 关键词匹配度 (0-40分)
        keyword_score = self._calculate_keyword_score(memory)
        score += keyword_score

        # 2. 内容质量 (0-25分)
        quality_score = self._calculate_quality_score(memory)
        score += quality_score

        # 3. 时间新鲜度 (0-20分)
        recency_score = self._calculate_recency_score(memory)
        score += recency_score

        # 4. 优先级 (0-15分)
        priority_score = self._calculate_priority_score(memory)
        score += priority_score

        return min(score, 100.0)

    def _calculate_keyword_score(self, memory: Dict[str, Any]) -> float:
        """计算关键词匹配分数"""
        # 合并所有文本字段
        text = ' '.join([
            memory.get('topic', ''),
            memory.get('summary', ''),
            ' '.join(memory.get('key_points', [])),
            ' '.join(memory.get('decisions_made', [])),
            memory.get('outcomes', '')
        ]).lower()

        # 计算匹配权重
        total_weight = 0.0
        for keyword, weight in self.keyword_weights.items():
            # 使用正则匹配完整单词
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, text):
                total_weight += weight

        # 转换为0-40分
        return min(total_weight * 5, 40.0)

    def _calculate_quality_score(self, memory: Dict[str, Any]) -> float:
        """计算内容质量分数"""
        score = 0.0

        # 长度分数 (0-10分)
        summary_len = len(memory.get('summary', ''))
        key_points_count = len(memory.get('key_points', []))

        if summary_len > 50:
            score += 5
        if summary_len > 150:
            score += 3
        if key_points_count >= 3:
            score += 2

        # 结构完整性 (0-15分)
        required_fields = ['topic', 'summary', 'outcomes']
        for field in required_fields:
            if memory.get(field):
                score += 3

        if memory.get('key_points'):
            score += 3
        if memory.get('tools_used'):
            score += 3

        return min(score, 25.0)

    def _calculate_recency_score(self, memory: Dict[str, Any]) -> float:
        """计算时间新鲜度分数"""
        timestamp_str = memory.get('timestamp', '')
        if not timestamp_str:
            return 0.0

        try:
            timestamp = datetime.fromisoformat(timestamp_str)
            age = datetime.now() - timestamp

            # 越新分数越高
            if age.days <= 1:
                return 20.0
            elif age.days <= 7:
                return 15.0
            elif age.days <= 30:
                return 10.0
            elif age.days <= 90:
                return 5.0
            else:
                return 2.0  # 旧记忆仍有一定价值
        except:
            return 0.0

    def _calculate_priority_score(self, memory: Dict[str, Any]) -> float:
        """计算优先级分数"""
        priority = memory.get('priority', 'normal')

        if priority == 'high':
            return 15.0
        elif priority == 'normal':
            return 10.0
        elif priority == 'low':
            return 5.0
        else:
            return 10.0


class SemanticRetriever:
    """
    语义检索器 - LangMem 风格

    基于关键词匹配的轻量级语义检索
    """

    def __init__(self, scorer: ImportanceScorer):
        self.scorer = scorer

    def search(self, memories: List[Dict[str, Any]], query: str,
               top_k: int = 5, min_score: float = 20.0) -> List[Dict[str, Any]]:
        """
        搜索相关记忆

        参数:
            memories: 记忆列表
            query: 搜索查询
            top_k: 返回前K个结果
            min_score: 最低相关性分数

        返回:
            排序后的相关记忆列表
        """
        # 计算每条记忆的相关性分数
        scored_memories = []
        for memory in memories:
            relevance = self._calculate_relevance(memory, query)
            if relevance >= min_score:
                scored_memories.append((memory, relevance))

        # 按相关性排序
        scored_memories.sort(key=lambda x: x[1], reverse=True)

        # 返回top_k结果（附带相关性分数）
        results = []
        for memory, score in scored_memories[:top_k]:
            memory_with_score = memory.copy()
            memory_with_score['_relevance_score'] = round(score, 2)
            results.append(memory_with_score)

        return results

    def _calculate_relevance(self, memory: Dict[str, Any], query: str) -> float:
        """
        计算记忆与查询的相关性

        综合考虑:
        - 文本匹配度
        - 记忆本身的重要性
        """
        # 1. 文本匹配度 (0-50分)
        text_match = self._calculate_text_match(memory, query)

        # 2. 记忆重要性加权 (0-50分)
        importance = self.scorer.calculate(memory) * 0.5

        return text_match + importance

    def _calculate_text_match(self, memory: Dict[str, Any], query: str) -> float:
        """计算文本匹配度"""
        query_lower = query.lower()

        # 合并所有文本字段
        text = ' '.join([
            memory.get('topic', ''),
            memory.get('summary', ''),
            ' '.join(memory.get('key_points', [])),
            ' '.join(memory.get('decisions_made', [])),
            memory.get('outcomes', ''),
            ' '.join(memory.get('tags', []))
        ]).lower()

        # 完全匹配
        if query_lower in text:
            base_score = 30.0

            # 检查匹配位置
            if query_lower in memory.get('topic', '').lower():
                base_score += 15.0  # 主题匹配权重最高
            elif query_lower in memory.get('summary', '').lower():
                base_score += 10.0  # 摘要匹配次之

            return base_score

        # 部分匹配（单词级别）
        query_words = set(query_lower.split())
        text_words = set(text.split())

        overlap = query_words & text_words
        if overlap:
            return len(overlap) / len(query_words) * 30.0

        return 0.0


class MemoryCleaner:
    """
    记忆清理器 - LangMem 风格

    自动清理低价值记忆，保持记忆库健康
    """

    def __init__(self, scorer: ImportanceScorer):
        self.scorer = scorer

    def cleanup_low_score(self, memories: List[Dict[str, Any]],
                         threshold: float = 30.0,
                         keep_recent_days: int = 30,
                         dry_run: bool = False) -> Dict[str, Any]:
        """
        清理低分记忆

        参数:
            memories: 记忆列表
            threshold: 重要性分数阈值（低于此分数将被清理）
            keep_recent_days: 保留最近N天的记忆（不管分数）
            dry_run: 仅模拟，不实际删除

        返回:
            清理统计信息
        """
        cutoff_date = datetime.now() - timedelta(days=keep_recent_days)
        to_remove = []
        to_keep = []

        for memory in memories:
            timestamp_str = memory.get('timestamp', '')
            try:
                timestamp = datetime.fromisoformat(timestamp_str)
                is_recent = timestamp > cutoff_date
            except:
                is_recent = False

            score = self.scorer.calculate(memory)

            # 决定是否保留
            if is_recent or score >= threshold:
                to_keep.append(memory)
            else:
                to_remove.append(memory)

        if not dry_run:
            # 实际清理：只保留to_keep
            cleaned_memories = to_keep
        else:
            # 模拟：保留所有
            cleaned_memories = memories

        return {
            'original_count': len(memories),
            'removed_count': len(to_remove),
            'kept_count': len(to_keep),
            'removed_scores': [self.scorer.calculate(m) for m in to_remove],
            'dry_run': dry_run,
            'cleaned_memories': cleaned_memories if not dry_run else memories
        }

    def suggest_cleanup(self, memories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        建议清理策略（不实际执行）

        分析记忆库状态，提供清理建议
        """
        # 统计分数分布
        scores = [self.scorer.calculate(m) for m in memories]

        if not scores:
            return {
                'total_memories': 0,
                'suggestion': '无需清理',
                'details': '记忆库为空'
            }

        avg_score = sum(scores) / len(scores)
        low_score_count = sum(1 for s in scores if s < 30)
        high_score_count = sum(1 for s in scores if s >= 70)

        # 生成建议
        if low_score_count > len(memories) * 0.3:
            suggestion = f"建议清理 {low_score_count} 条低分记忆（<30分）"
            threshold = 30.0
        elif low_score_count > len(memories) * 0.2:
            suggestion = f"建议清理 {low_score_count} 条低分记忆（<30分）"
            threshold = 30.0
        else:
            suggestion = "记忆库健康，无需清理"
            threshold = None

        return {
            'total_memories': len(memories),
            'average_score': round(avg_score, 2),
            'low_score_count': low_score_count,
            'high_score_count': high_score_count,
            'suggestion': suggestion,
            'suggested_threshold': threshold,
            'score_distribution': {
                'min': round(min(scores), 2),
                'max': round(max(scores), 2),
                'avg': round(avg_score, 2)
            }
        }


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

        # LangMem 增强组件
        self.scorer = ImportanceScorer()
        self.retriever = SemanticRetriever(self.scorer)
        self.cleaner = MemoryCleaner(self.scorer)

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
            'outcomes': context.get('outcomes', ''),
            'priority': context.get('priority', 'normal'),  # 新增：优先级
            'tags': context.get('tags', [])  # 新增：标签
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

    def get_high_priority_contexts(self, limit: int = 10) -> List[Dict]:
        """获取高优先级记忆"""
        contexts = self.memory['contexts']['contexts']
        high_priority = [ctx for ctx in contexts if ctx.get('priority') == 'high']
        return high_priority[:limit]

    def get_contexts_by_tag(self, tag: str, limit: int = 10) -> List[Dict]:
        """按标签获取记忆"""
        contexts = self.memory['contexts']['contexts']
        tagged = [ctx for ctx in contexts if tag in ctx.get('tags', [])]
        return tagged[:limit]

    def get_recent_contexts(self, limit: int = 10) -> List[Dict]:
        """获取最近的记忆"""
        contexts = self.memory['contexts']['contexts']
        return contexts[-limit:]

    def search_all_contexts(self, keyword: str, limit: int = 20) -> List[Dict]:
        """全局搜索记忆"""
        contexts = self.memory['contexts']['contexts']
        results = []
        keyword_lower = keyword.lower()

        for ctx in contexts:
            # 在多个字段中搜索
            searchable_text = ' '.join([
                ctx.get('topic', ''),
                ctx.get('summary', ''),
                ' '.join(ctx.get('key_points', [])),
                ' '.join(ctx.get('decisions_made', [])),
                ctx.get('outcomes', '')
            ]).lower()

            if keyword_lower in searchable_text:
                results.append(ctx)
                if len(results) >= limit:
                    break

        return results

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

    # ========================================================================
    # LangMem 增强方法
    # ========================================================================

    def calculate_importance(self, memory: Dict[str, Any]) -> float:
        """计算单条记忆的重要性分数"""
        return self.scorer.calculate(memory)

    def semantic_search(self, query: str, top_k: int = 5,
                        min_score: float = 20.0) -> List[Dict[str, Any]]:
        """
        语义搜索记忆

        参数:
            query: 搜索查询
            top_k: 返回前K个结果
            min_score: 最低相关性分数

        返回:
            相关记忆列表（包含 _relevance_score 字段）
        """
        contexts = self.memory['contexts']['contexts']
        return self.retriever.search(contexts, query, top_k, min_score)

    def get_top_memories(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取最重要的记忆（按重要性分数排序）"""
        contexts = self.memory['contexts']['contexts']

        # 计算所有记忆的重要性分数
        scored_memories = []
        for ctx in contexts:
            score = self.scorer.calculate(ctx)
            scored_memories.append((ctx, score))

        # 按分数排序
        scored_memories.sort(key=lambda x: x[1], reverse=True)

        # 返回top_k（附带分数）
        results = []
        for memory, score in scored_memories[:limit]:
            memory_with_score = memory.copy()
            memory_with_score['_importance_score'] = round(score, 2)
            results.append(memory_with_score)

        return results

    def analyze_memory_health(self) -> Dict[str, Any]:
        """分析记忆库健康状况"""
        contexts = self.memory['contexts']['contexts']
        return self.cleaner.suggest_cleanup(contexts)

    def cleanup_memories(self, threshold: float = 30.0,
                         keep_recent_days: int = 30,
                         dry_run: bool = True) -> Dict[str, Any]:
        """
        清理低分记忆

        参数:
            threshold: 重要性分数阈值（低于此分数将被清理）
            keep_recent_days: 保留最近N天的记忆
            dry_run: 模拟运行（不实际删除）

        返回:
            清理统计信息
        """
        contexts = self.memory['contexts']['contexts']
        result = self.cleaner.cleanup_low_score(
            contexts, threshold, keep_recent_days, dry_run
        )

        # 如果不是模拟运行，实际更新记忆
        if not dry_run:
            self.memory['contexts']['contexts'] = result['cleaned_memories']
            self.memory['contexts']['total_contexts'] = len(result['cleaned_memories'])
            self.save('contexts')

        return result

    def get_importance_distribution(self) -> Dict[str, Any]:
        """获取重要性分数分布统计"""
        contexts = self.memory['contexts']['contexts']
        scores = [self.scorer.calculate(ctx) for ctx in contexts]

        if not scores:
            return {'error': '无记忆数据'}

        # 分级统计
        high = sum(1 for s in scores if s >= 70)
        medium = sum(1 for s in scores if 50 <= s < 70)
        low = sum(1 for s in scores if 30 <= s < 50)
        very_low = sum(1 for s in scores if s < 30)

        return {
            'total': len(scores),
            'average': round(sum(scores) / len(scores), 2),
            'min': round(min(scores), 2),
            'max': round(max(scores), 2),
            'distribution': {
                'high (70-100)': high,
                'medium (50-69)': medium,
                'low (30-49)': low,
                'very_low (0-29)': very_low
            },
            'percentiles': {
                'p50': round(sorted(scores)[len(scores)//2], 2),
                'p75': round(sorted(scores)[int(len(scores)*0.75)], 2) if len(scores) > 1 else 0,
                'p90': round(sorted(scores)[int(len(scores)*0.9)], 2) if len(scores) > 1 else 0
            }
        }


# ============================================================================
# 记忆管理器
# ============================================================================

class ClaudeMemory:
    """Claude Code 记忆管理器 (v2.0 - 支持向量语义搜索)"""

    def __init__(self, workspace_root: Optional[Path] = None, enable_semantic: bool = True):
        if workspace_root is None:
            # 自动检测工作区根目录
            workspace_root = Path(__file__).parent.parent

        self.store = MemoryStore(workspace_root)
        self.current_session = self._generate_session_id()

        # v2.0新增：语义记忆（可选启用）
        self.enable_semantic = enable_semantic
        self.semantic_memory = None

        if enable_semantic:
            try:
                from semantic_memory import SemanticMemory
                self.semantic_memory = SemanticMemory(workspace_root)
                print("✅ 语义记忆已启用")
            except ImportError as e:
                print(f"⚠️ 语义记忆未启用: {e}")
                print("💡 提示: 运行 pip install chromadb sentence-transformers")
                self.enable_semantic = False

    def _generate_session_id(self) -> str:
        """生成会话ID"""
        return f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    def remember_context(self, topic: str, summary: str, key_points: List[str],
                        tools_used: List[str], decisions_made: List[str],
                        outcomes: str, priority: str = 'normal', tags: List[str] = None):
        """记住对话上下文 (v2.0 - 同时保存到向量数据库)"""
        context = {
            'session_id': self.current_session,
            'topic': topic,
            'summary': summary,
            'key_points': key_points,
            'tools_used': tools_used,
            'decisions_made': decisions_made,
            'outcomes': outcomes,
            'priority': priority,
            'tags': tags or []
        }

        # 保存到JSON存储
        self.store.add_context(context)

        # v2.0新增：同时保存到向量数据库
        if self.enable_semantic and self.semantic_memory:
            memory_id = f"ctx_{context['session_id']}_{datetime.now().timestamp()}"
            text = f"{topic}. {summary}"

            # 准备元数据
            metadata = {
                'topic': topic,
                'session_id': self.current_session,
                'priority': priority,
                'tags': ','.join(tags or []),
                'type': 'context'
            }

            self.semantic_memory.add_memory(memory_id, text, metadata)

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

    def recall_high_priority(self, limit: int = 10) -> List[Dict]:
        """回忆高优先级上下文"""
        return self.store.get_high_priority_contexts(limit)

    def recall_by_tag(self, tag: str, limit: int = 10) -> List[Dict]:
        """按标签回忆上下文"""
        return self.store.get_contexts_by_tag(tag, limit)

    def recall_recent(self, limit: int = 10) -> List[Dict]:
        """回忆最近的上下文"""
        return self.store.get_recent_contexts(limit)

    def search_memory(self, keyword: str, limit: int = 20) -> List[Dict]:
        """全局搜索记忆"""
        return self.store.search_all_contexts(keyword, limit)

    def suggest_tool(self, task_type: str) -> Optional[str]:
        """基于历史建议工具"""
        return self.store.get_tool_preferences(task_type)

    def learn_preferences(self, preferences: Dict[str, Any]):
        """学习用户偏好"""
        self.store.update_preferences(preferences)

    def get_memory_stats(self) -> Dict[str, Any]:
        """获取记忆统计"""
        return self.store.get_statistics()

    def calculate_importance(self, memory: Dict[str, Any]) -> float:
        """计算单条记忆的重要性分数"""
        return self.store.calculate_importance(memory)

    # ========================================================================
    # LangMem 增强方法（代理到 MemoryStore）
    # ========================================================================

    def semantic_search(self, query: str, top_k: int = 5,
                        min_score: float = 20.0) -> List[Dict[str, Any]]:
        """语义搜索记忆 (v2.0 - 向量语义搜索)"""
        # v2.0新增：优先使用向量语义搜索
        if self.enable_semantic and self.semantic_memory:
            return self.semantic_memory.search(query, top_k=top_k)
        else:
            # 回退到原有的关键词语义搜索
            return self.store.semantic_search(query, top_k, min_score)

    def hybrid_search(self, query: str, top_k: int = 5,
                     semantic_weight: float = 0.7) -> List[Dict[str, Any]]:
        """
        混合搜索 (v2.0新增)

        结合向量语义搜索和关键词搜索，提供最佳结果

        参数:
            query: 搜索查询
            top_k: 返回前K个结果
            semantic_weight: 语义搜索权重 (0-1，默认0.7)
        """
        if not (self.enable_semantic and self.semantic_memory):
            # 语义搜索未启用，使用关键词搜索
            return self.store.semantic_search(query, top_k)

        # 获取关键词搜索结果
        keyword_results = self.store.semantic_search(query, top_k * 2)

        # 转换为统一格式
        formatted_keyword_results = []
        for kw_result in keyword_results:
            formatted_keyword_results.append({
                'id': kw_result.get('timestamp', ''),
                'text': f"{kw_result.get('topic', '')}. {kw_result.get('summary', '')}",
                'metadata': kw_result,
                '_relevance_score': kw_result.get('_relevance_score', 0)
            })

        # 执行混合搜索
        hybrid_results = self.semantic_memory.hybrid_search(
            query=query,
            keyword_results=formatted_keyword_results,
            top_k=top_k,
            semantic_weight=semantic_weight
        )

        return hybrid_results

    def get_top_memories(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取最重要的记忆"""
        return self.store.get_top_memories(limit)

    def analyze_memory_health(self) -> Dict[str, Any]:
        """分析记忆库健康状况"""
        return self.store.analyze_memory_health()

    def cleanup_memories(self, threshold: float = 30.0,
                         keep_recent_days: int = 30,
                         dry_run: bool = True) -> Dict[str, Any]:
        """清理低分记忆"""
        return self.store.cleanup_memories(threshold, keep_recent_days, dry_run)

    def get_importance_distribution(self) -> Dict[str, Any]:
        """获取重要性分数分布"""
        return self.store.get_importance_distribution()

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
