#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自然语言搜索模块
支持时间范围、文件类型、主题等多维度搜索
"""

import re
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import json


class QueryType(Enum):
    """查询类型"""
    TIME_BASED = "time_based"          # 基于时间
    TOPIC_BASED = "topic_based"        # 基于主题
    FILE_TYPE_BASED = "file_type_based"  # 基于文件类型
    COMPLEX = "complex"                # 复合查询


@dataclass
class ParsedQuery:
    """解析后的查询"""
    original: str                      # 原始查询
    query_type: QueryType              # 查询类型
    keywords: List[str]                # 关键词
    time_range: Optional[Dict]         # 时间范围
    file_types: Optional[List[str]]    # 文件类型
    topics: Optional[List[str]]        # 主题
    filters: Dict[str, Any]            # 其他过滤条件


class NaturalLanguageParser:
    """自然语言查询解析器"""

    def __init__(self):
        """初始化解析器"""
        self.logger = logging.getLogger('NaturalLanguageParser')
        self._setup_patterns()

    def _setup_patterns(self):
        """设置匹配模式"""
        # 时间模式
        self.time_patterns = {
            'today': r'(今天|今日)',
            'yesterday': r'(昨天|昨日)',
            'this_week': r'(本周|这周)',
            'last_week': r'(上周|上周)',
            'this_month': r'(本月|这个月)',
            'last_month': r'(上月|上个月)',
            'this_year': r'(今年|今年)',
            'recent_days': r'最近(\d+)天',
            'recent_weeks': r'最近(\d+)周',
        }

        # 文件类型模式
        self.file_type_patterns = {
            'python': r'(python|\.py)',
            'markdown': r'(markdown|\.md)',
            'yaml': r'(yaml|\.yml)',
            'json': r'(json|\.json)',
            'docx': r'(word|\.docx)',
            'pdf': r'(pdf|\.pdf)',
        }

        # 主题模式
        self.topic_patterns = {
            'ocr': r'(ocr|文字识别|图像识别)',
            'ai': r'(ai|人工智能|智能)',
            'flask': r'(flask|web|网站)',
            'database': r'(数据库|sqlite|mysql)',
            'testing': r'(测试|test)',
        }

    def parse(self, query: str) -> ParsedQuery:
        """
        解析自然语言查询

        Args:
            query: 自然语言查询字符串

        Returns:
            解析后的查询对象
        """
        self.logger.info(f"🔍 解析查询: '{query}'")

        # 标准化查询
        query = query.strip().lower()

        # 提取时间范围
        time_range = self._extract_time_range(query)

        # 提取文件类型
        file_types = self._extract_file_types(query)

        # 提取主题
        topics = self._extract_topics(query)

        # 提取关键词
        keywords = self._extract_keywords(query)

        # 确定查询类型
        query_type = self._determine_query_type(time_range, file_types, topics)

        # 构建过滤条件
        filters = {
            'time_range': time_range,
            'file_types': file_types,
            'topics': topics
        }

        parsed = ParsedQuery(
            original=query,
            query_type=query_type,
            keywords=keywords,
            time_range=time_range,
            file_types=file_types,
            topics=topics,
            filters=filters
        )

        self.logger.info(f"✅ 查询解析完成: {query_type.value}")
        return parsed

    def _extract_time_range(self, query: str) -> Optional[Dict]:
        """提取时间范围"""
        now = datetime.now()

        for pattern_name, pattern in self.time_patterns.items():
            match = re.search(pattern, query)
            if match:
                if pattern_name == 'today':
                    return {
                        'start': now.replace(hour=0, minute=0, second=0),
                        'end': now,
                        'label': '今天'
                    }
                elif pattern_name == 'yesterday':
                    yesterday = now - timedelta(days=1)
                    return {
                        'start': yesterday.replace(hour=0, minute=0, second=0),
                        'end': yesterday.replace(hour=23, minute=59, second=59),
                        'label': '昨天'
                    }
                elif pattern_name == 'this_week':
                    start_of_week = now - timedelta(days=now.weekday())
                    return {
                        'start': start_of_week.replace(hour=0, minute=0, second=0),
                        'end': now,
                        'label': '本周'
                    }
                elif pattern_name == 'last_week':
                    start_of_this_week = now - timedelta(days=now.weekday())
                    start_of_last_week = start_of_this_week - timedelta(days=7)
                    return {
                        'start': start_of_last_week.replace(hour=0, minute=0, second=0),
                        'end': start_of_this_week - timedelta(seconds=1),
                        'label': '上周'
                    }
                elif pattern_name == 'recent_days':
                    days = int(match.group(1))
                    return {
                        'start': now - timedelta(days=days),
                        'end': now,
                        'label': f'最近{days}天'
                    }
                elif pattern_name == 'recent_weeks':
                    weeks = int(match.group(1))
                    return {
                        'start': now - timedelta(weeks=weeks),
                        'end': now,
                        'label': f'最近{weeks}周'
                    }

        return None

    def _extract_file_types(self, query: str) -> Optional[List[str]]:
        """提取文件类型"""
        found_types = []

        for type_name, pattern in self.file_type_patterns.items():
            if re.search(pattern, query):
                found_types.append(type_name)

        return found_types if found_types else None

    def _extract_topics(self, query: str) -> Optional[List[str]]:
        """提取主题"""
        found_topics = []

        for topic_name, pattern in self.topic_patterns.items():
            if re.search(pattern, query):
                found_topics.append(topic_name)

        return found_topics if found_topics else None

    def _extract_keywords(self, query: str) -> List[str]:
        """提取关键词"""
        # 移除时间、文件类型、主题相关的词
        cleaned = query

        for pattern in self.time_patterns.values():
            cleaned = re.sub(pattern, '', cleaned)

        for pattern in self.file_type_patterns.values():
            cleaned = re.sub(pattern, '', cleaned)

        for pattern in self.topic_patterns.values():
            cleaned = re.sub(pattern, '', cleaned)

        # 移除常用停用词
        stop_words = ['的', '了', '是', '在', '有', '和', '与', '或', '等']
        for word in stop_words:
            cleaned = cleaned.replace(word, ' ')

        # 分词
        keywords = [k.strip() for k in cleaned.split() if k.strip()]

        return keywords

    def _determine_query_type(
        self,
        time_range: Optional[Dict],
        file_types: Optional[List[str]],
        topics: Optional[List[str]]
    ) -> QueryType:
        """确定查询类型"""
        has_time = time_range is not None
        has_type = file_types is not None
        has_topic = topics is not None

        conditions = [has_time, has_type, has_topic]
        true_count = sum(conditions)

        if true_count == 0:
            return QueryType.TOPIC_BASED
        elif true_count == 1:
            if has_time:
                return QueryType.TIME_BASED
            elif has_type:
                return QueryType.FILE_TYPE_BASED
            else:
                return QueryType.TOPIC_BASED
        else:
            return QueryType.COMPLEX


class EnhancedSearchEngine:
    """增强的搜索引擎 - 支持自然语言查询"""

    def __init__(self, base_search_engine=None):
        """
        初始化搜索引擎

        Args:
            base_search_engine: 基础搜索引擎（如记忆助手的搜索引擎）
        """
        self.parser = NaturalLanguageParser()
        self.base_engine = base_search_engine
        self.logger = logging.getLogger('EnhancedSearchEngine')

    def search(self, query: str, top_k: int = 10) -> Dict[str, Any]:
        """
        自然语言搜索

        Args:
            query: 自然语言查询
            top_k: 返回结果数量

        Returns:
            搜索结果字典
        """
        # 解析查询
        parsed = self.parser.parse(query)

        self.logger.info(f"🔍 执行搜索: {parsed.query_type.value}")

        # 执行搜索
        if parsed.query_type == QueryType.TIME_BASED:
            results = self._search_by_time(parsed, top_k)
        elif parsed.query_type == QueryType.FILE_TYPE_BASED:
            results = self._search_by_file_type(parsed, top_k)
        elif parsed.query_type == QueryType.TOPIC_BASED:
            results = self._search_by_topic(parsed, top_k)
        else:  # COMPLEX
            results = self._search_complex(parsed, top_k)

        return {
            'query': query,
            'parsed': parsed,
            'results': results,
            'count': len(results)
        }

    def _search_by_time(self, parsed: ParsedQuery, top_k: int) -> List[Dict]:
        """按时间范围搜索"""
        # 这里可以集成文件系统的时间过滤
        # 示例：搜索特定时间范围内修改的文件

        results = []

        if self.base_engine:
            # 使用基础搜索引擎
            base_results = self.base_engine.search(' '.join(parsed.keywords))
            # 应用时间过滤
            results = self._filter_by_time(base_results, parsed.time_range)

        return results[:top_k]

    def _search_by_file_type(self, parsed: ParsedQuery, top_k: int) -> List[Dict]:
        """按文件类型搜索"""
        results = []

        # 示例：搜索特定文件类型
        for file_type in parsed.file_types:
            # 这里可以集成 Glob 搜索
            pass

        return results[:top_k]

    def _search_by_topic(self, parsed: ParsedQuery, top_k: int) -> List[Dict]:
        """按主题搜索"""
        results = []

        if self.base_engine:
            # 使用基础搜索引擎进行语义搜索
            query = ' '.join(parsed.keywords + (parsed.topics or []))
            results = self.base_engine.search(query)

        return results[:top_k]

    def _search_complex(self, parsed: ParsedQuery, top_k: int) -> List[Dict]:
        """复合查询"""
        results = []

        # 先按主题搜索
        topic_results = self._search_by_topic(parsed, top_k * 2)

        # 再应用其他过滤条件
        if parsed.time_range:
            topic_results = self._filter_by_time(topic_results, parsed.time_range)

        if parsed.file_types:
            topic_results = self._filter_by_file_type(topic_results, parsed.file_types)

        results = topic_results

        return results[:top_k]

    def _filter_by_time(self, results: List[Dict], time_range: Dict) -> List[Dict]:
        """按时间过滤结果"""
        filtered = []
        start = time_range['start']
        end = time_range['end']

        for result in results:
            # 这里需要根据实际结果结构提取时间戳
            # 示例假设结果有 'modified_time' 字段
            if 'modified_time' in result:
                file_time = result['modified_time']
                if start <= file_time <= end:
                    filtered.append(result)

        return filtered

    def _filter_by_file_type(self, results: List[Dict], file_types: List[str]) -> List[Dict]:
        """按文件类型过滤结果"""
        filtered = []

        for result in results:
            # 这里需要根据实际结果结构提取文件类型
            if 'file_path' in result:
                file_path = result['file_path']
                for ft in file_types:
                    if f'.{ft}' in file_path:
                        filtered.append(result)
                        break

        return filtered


# 使用示例
if __name__ == "__main__":
    # 创建搜索引擎
    engine = EnhancedSearchEngine()

    # 测试查询
    test_queries = [
        "上周添加的 Python 笔记",
        "今天关于 OCR 的文档",
        "最近7天的 Flask 代码",
        "关于 AI 的所有文件",
        "本周的 markdown 文档"
    ]

    print("\n=== 自然语言搜索测试 ===\n")

    for query in test_queries:
        print(f"\n🔍 查询: '{query}'")
        parsed = engine.parser.parse(query)

        print(f"  类型: {parsed.query_type.value}")
        print(f"  关键词: {parsed.keywords}")
        print(f"  时间: {parsed.time_range}")
        print(f"  文件类型: {parsed.file_types}")
        print(f"  主题: {parsed.topics}")

    print("\n✅ 自然语言搜索模块已创建！")
