#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多Agent系统原型 - 智能文档处理团队

演示如何使用多个专门的Agent协作完成任务:
- 协调者(Coordinator): 分配任务和协调工作
- 分析师(Analyst): 分析文档内容和结构
- 处理器(Processor): 执行具体的文档处理操作
- 审查师(Reviewer): 审查结果并生成报告

基于现有的 WorkflowEngine 框架

作者: Claude Code
日期: 2026-01-15
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Windows 终端编码修复
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass

# 导入工作流引擎
sys.path.insert(0, str(Path(__file__).parent))
from workflow_engine import (
    WorkflowGraph, Node, State, WorkflowStatus,
    ConditionalEdge, Edge, END
)


# ============================================================================
# Agent 基类
# ============================================================================

class BaseAgent(Node):
    """Agent基类"""

    def __init__(self, name: str, role: str, expertise: List[str]):
        super().__init__(name, f"{role} - {', '.join(expertise)}")
        self.role = role
        self.expertise = expertise
        self.agent_type = self.__class__.__name__

    def log(self, message: str, level: str = "INFO"):
        """记录日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [{self.agent_type}] {message}")

    def execute(self, state: State) -> State:
        """执行Agent任务"""
        self.log(f"开始执行任务: {self.name}")
        self.log(f"当前状态: {state['metadata'].get('phase', 'unknown')}")

        try:
            result = self.process(state)
            self.log(f"任务完成: {self.name}")
            return result
        except Exception as e:
            self.log(f"任务失败: {str(e)}", "ERROR")
            state['errors'].append(f"{self.name}: {str(e)}")
            return state

    def process(self, state: State) -> State:
        """具体的处理逻辑，由子类实现"""
        raise NotImplementedError


# ============================================================================
# 具体Agent实现
# ============================================================================

class CoordinatorAgent(BaseAgent):
    """协调者Agent - 负责任务分配和工作流协调"""

    def __init__(self):
        super().__init__(
            name="coordinator",
            role="项目协调者",
            expertise=["任务规划", "资源分配", "进度跟踪"]
        )

    def process(self, state: State) -> State:
        """协调整个工作流程"""
        data = state['data']

        # 初始化任务
        if 'tasks' not in data:
            data['tasks'] = []
            data['current_task_index'] = 0

            # 分析输入，创建任务列表
            input_text = data.get('input_text', '')
            if input_text:
                # 简单的分词和分析
                words = input_text.split()
                data['total_words'] = len(words)
                data['tasks'] = [
                    {'id': 1, 'type': 'analyze', 'description': '分析文档结构'},
                    {'id': 2, 'type': 'extract', 'description': '提取关键信息'},
                    {'id': 3, 'type': 'process', 'description': '处理和优化'},
                    {'id': 4, 'type': 'review', 'description': '审查和报告'}
                ]

            self.log(f"创建了 {len(data['tasks'])} 个任务")
            state['metadata']['phase'] = 'planning_complete'
            state['metadata']['progress'] = '0%'

        return state


class AnalystAgent(BaseAgent):
    """分析师Agent - 负责文档内容分析"""

    def __init__(self):
        super().__init__(
            name="analyst",
            role="文档分析师",
            expertise=["内容分析", "结构识别", "关键词提取"]
        )

    def process(self, state: State) -> State:
        """分析文档内容"""
        data = state['data']

        # 获取输入文本
        text = data.get('input_text', '')

        if not text:
            state['errors'].append("没有可分析的文本")
            return state

        # 执行分析
        analysis = {
            'word_count': len(text.split()),
            'char_count': len(text),
            'line_count': text.count('\n') + 1,
            'avg_word_length': sum(len(word) for word in text.split()) / max(len(text.split()), 1),
            'keywords': self._extract_keywords(text),
            'sentiment': self._analyze_sentiment(text),
            'complexity': self._assess_complexity(text)
        }

        data['analysis'] = analysis
        state['metadata']['phase'] = 'analysis_complete'
        state['metadata']['progress'] = '25%'

        self.log(f"分析完成: {analysis['word_count']} 词, {analysis['line_count']} 行")
        self.log(f"关键词: {', '.join(analysis['keywords'][:5])}")

        return state

    def _extract_keywords(self, text: str) -> List[str]:
        """简单的关键词提取"""
        # 停用词
        stopwords = {'的', '了', '是', '在', '我', '有', '和', '就', '不', '人', '都', '一',
                    'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being'}

        # 分词并过滤
        words = [w for w in text.split() if len(w) > 2 and w.lower() not in stopwords]

        # 统计词频
        freq = {}
        for word in words:
            word_lower = word.lower()
            freq[word_lower] = freq.get(word_lower, 0) + 1

        # 返回前10个高频词
        sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, count in sorted_words[:10]]

    def _analyze_sentiment(self, text: str) -> str:
        """简单的情感分析"""
        positive_words = {'好', '优秀', '成功', '喜欢', '棒', 'excellent', 'good', 'great', 'love'}
        negative_words = {'差', '失败', '讨厌', '糟糕', 'bad', 'fail', 'hate', 'terrible'}

        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)

        if positive_count > negative_count:
            return "积极"
        elif negative_count > positive_count:
            return "消极"
        else:
            return "中性"

    def _assess_complexity(self, text: str) -> str:
        """评估文本复杂度"""
        words = text.split()
        avg_length = sum(len(w) for w in words) / max(len(words), 1)

        if avg_length < 4:
            return "简单"
        elif avg_length < 6:
            return "中等"
        else:
            return "复杂"


class ProcessorAgent(BaseAgent):
    """处理器Agent - 负责文档处理和优化"""

    def __init__(self):
        super().__init__(
            name="processor",
            role="文档处理器",
            expertise=["文本优化", "格式整理", "内容增强"]
        )

    def process(self, state: State) -> State:
        """处理和优化文档"""
        data = state['data']

        text = data.get('input_text', '')
        if not text:
            return state

        # 执行处理
        processed = {
            'cleaned': self._clean_text(text),
            'summarized': self._summarize(text),
            'enhanced': self._enhance(text),
            'formatted': self._format(text)
        }

        data['processing'] = processed
        state['metadata']['phase'] = 'processing_complete'
        state['metadata']['progress'] = '75%'

        self.log("处理完成: 清理, 摘要, 增强, 格式化")

        return state

    def _clean_text(self, text: str) -> str:
        """清理文本"""
        # 去除多余空格
        lines = text.split('\n')
        cleaned = [line.strip() for line in lines if line.strip()]
        return '\n'.join(cleaned)

    def _summarize(self, text: str) -> str:
        """生成摘要"""
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        if len(sentences) <= 3:
            return text

        # 返回前两句作为摘要
        return '. '.join(sentences[:2]) + '.'

    def _enhance(self, text: str) -> str:
        """增强文本"""
        # 添加元数据
        word_count = len(text.split())
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header = f"# 文档增强版本\n生成时间: {timestamp}\n词数: {word_count}\n\n"

        return header + text

    def _format(self, text: str) -> Dict[str, Any]:
        """格式化信息"""
        return {
            'paragraphs': len([p for p in text.split('\n\n') if p.strip()]),
            'sentences': len([s for s in text.split('.') if s.strip()]),
            'words': len(text.split()),
            'characters': len(text)
        }


class ReviewerAgent(BaseAgent):
    """审查师Agent - 负责质量审查和报告生成"""

    def __init__(self):
        super().__init__(
            name="reviewer",
            role="质量审查师",
            expertise=["质量评估", "报告生成", "建议提供"]
        )

    def process(self, state: State) -> State:
        """审查工作结果并生成报告"""
        data = state['data']

        # 收集所有Agent的工作结果
        analysis = data.get('analysis', {})
        processing = data.get('processing', {})

        # 生成评分
        scores = self._calculate_scores(analysis, processing)

        # 生成建议
        recommendations = self._generate_recommendations(analysis, processing)

        # 创建报告
        report = {
            'timestamp': datetime.now().isoformat(),
            'input_summary': {
                'original_text': data.get('input_text', '')[:100] + '...',
                'word_count': analysis.get('word_count', 0)
            },
            'analysis_results': analysis,
            'processing_results': {
                'cleaned_preview': processing.get('cleaned', '')[:100] + '...',
                'summary': processing.get('summarized', ''),
                'stats': processing.get('formatted', {})
            },
            'quality_scores': scores,
            'recommendations': recommendations,
            'agent_contributions': {
                'coordinator': '任务规划和协调',
                'analyst': '内容分析和特征提取',
                'processor': '文本处理和优化',
                'reviewer': '质量审查和报告生成'
            }
        }

        data['report'] = report
        state['metadata']['phase'] = 'review_complete'
        state['metadata']['progress'] = '100%'

        self.log("审查完成，已生成最终报告")
        self.log(f"总体评分: {scores['overall']}/100")

        return state

    def _calculate_scores(self, analysis: Dict, processing: Dict) -> Dict[str, float]:
        """计算质量评分"""
        scores = {}

        # 文本质量分（基于分析结果）
        complexity_bonus = {
            '简单': 0.8,
            '中等': 1.0,
            '复杂': 1.2
        }.get(analysis.get('complexity', '中等'), 1.0)

        sentiment_bonus = {
            '积极': 1.1,
            '中性': 1.0,
            '消极': 0.9
        }.get(analysis.get('sentiment', '中性'), 1.0)

        text_quality = 50.0 * complexity_bonus * sentiment_bonus
        scores['text_quality'] = min(100.0, text_quality)

        # 处理完整性分
        processing_completeness = 0
        if processing.get('cleaned'):
            processing_completeness += 25
        if processing.get('summarized'):
            processing_completeness += 25
        if processing.get('enhanced'):
            processing_completeness += 25
        if processing.get('formatted'):
            processing_completeness += 25

        scores['processing_completeness'] = processing_completeness

        # 分析深度分
        analysis_depth = 0
        if analysis.get('keywords'):
            analysis_depth += min(30, len(analysis['keywords']) * 3)
        if analysis.get('sentiment'):
            analysis_depth += 20
        if analysis.get('complexity'):
            analysis_depth += 20
        if analysis.get('word_count'):
            analysis_depth += 30

        scores['analysis_depth'] = min(100.0, analysis_depth)

        # 总体评分
        scores['overall'] = (
            scores['text_quality'] * 0.3 +
            scores['processing_completeness'] * 0.4 +
            scores['analysis_depth'] * 0.3
        )

        return scores

    def _generate_recommendations(self, analysis: Dict, processing: Dict) -> List[str]:
        """生成改进建议"""
        recommendations = []

        # 基于分析的建议
        if analysis.get('word_count', 0) < 50:
            recommendations.append("文本较短，建议扩展内容")
        elif analysis.get('word_count', 0) > 1000:
            recommendations.append("文本较长，建议分段处理")

        if analysis.get('complexity') == '简单':
            recommendations.append("文本简单，适合快速阅读")
        elif analysis.get('complexity') == '复杂':
            recommendations.append("文本复杂，建议增加解释说明")

        # 基于情感的建议
        if analysis.get('sentiment') == '消极':
            recommendations.append("检测到消极情感，建议调整语气")

        return recommendations if recommendations else ["文档质量良好，无需特别改进"]


# ============================================================================
# 多Agent系统编排器
# ============================================================================

class MultiAgentSystem:
    """多Agent系统 - 协调多个Agent协作"""

    def __init__(self):
        self.agents = {
            'coordinator': CoordinatorAgent(),
            'analyst': AnalystAgent(),
            'processor': ProcessorAgent(),
            'reviewer': ReviewerAgent()
        }
        self.workflow = None

    def build_workflow(self) -> WorkflowGraph:
        """构建多Agent工作流"""
        graph = WorkflowGraph("document_processing_team")

        # 添加所有Agent节点
        for agent_name, agent in self.agents.items():
            graph.add_node(agent_name, agent)

        # 定义工作流程：串行协作
        # 协调者 → 分析师 → 处理器 → 审查师 → 结束
        graph.add_edge("coordinator", "analyst")
        graph.add_edge("analyst", "processor")
        graph.add_edge("processor", "reviewer")
        graph.add_edge("reviewer", END)

        # 设置入口点
        graph.set_entry_point("coordinator")

        return graph.compile()

    def process(self, input_text: str) -> Dict[str, Any]:
        """处理输入文本"""
        print("=" * 70)
        print("🤖 多Agent文档处理团队启动")
        print("=" * 70)
        print()

        # 构建工作流
        if not self.workflow:
            self.workflow = self.build_workflow()

        # 准备初始数据（会自动包装成State）
        initial_data = {
            'input_text': input_text,
            'phase': 'initializing',
            'progress': '0%'
        }

        # 执行工作流
        result = self.workflow.invoke(initial_data)

        # 打印结果摘要
        self._print_summary(result)

        return result

    def _print_summary(self, result: Dict[str, Any]):
        """打印处理摘要"""
        print()
        print("=" * 70)
        print("📊 处理完成摘要")
        print("=" * 70)

        # result就是data部分
        data = result
        report = data.get('report', {})
        analysis = data.get('analysis', {})

        if report:
            print(f"\n⏰ 处理时间: {report.get('timestamp', 'N/A')}")

            if 'input_summary' in report:
                print(f"📝 词数统计: {report['input_summary'].get('word_count', 0)} 词")

            if analysis:
                print(f"\n🔍 分析结果:")
                print(f"   - 词数: {analysis.get('word_count', 0)}")
                print(f"   - 行数: {analysis.get('line_count', 0)}")
                print(f"   - 情感: {analysis.get('sentiment', 'N/A')}")
                print(f"   - 复杂度: {analysis.get('complexity', 'N/A')}")
                keywords = analysis.get('keywords', [])[:3]
                print(f"   - 关键词: {', '.join(keywords)}")

            if 'quality_scores' in report:
                scores = report['quality_scores']
                print(f"\n📈 质量评分:")
                print(f"   - 文本质量: {scores['text_quality']:.1f}/100")
                print(f"   - 处理完整度: {scores['processing_completeness']:.1f}/100")
                print(f"   - 分析深度: {scores['analysis_depth']:.1f}/100")
                print(f"   - 综合评分: {scores['overall']:.1f}/100")

            if 'recommendations' in report:
                print(f"\n💡 改进建议:")
                for i, rec in enumerate(report['recommendations'], 1):
                    print(f"   {i}. {rec}")

        print("\n" + "=" * 70)


# ============================================================================
# 主程序
# ============================================================================

def main():
    """主程序 - 演示多Agent系统"""

    print("""
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║             多Agent系统原型 - 智能文档处理团队                       ║
║                                                                    ║
║  Agent团队成员:                                                    ║
║    🎯 协调者 (Coordinator) - 任务规划和资源分配                      ║
║    🔍 分析师 (Analyst) - 内容分析和特征提取                          ║
║    ⚙️ 处理器 (Processor) - 文本处理和优化                           ║
║    ✅ 审查师 (Reviewer) - 质量审查和报告生成                         ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
    """)

    # 创建多Agent系统
    mas = MultiAgentSystem()

    # 示例1: 简单文本
    print("\n🔵 示例1: 简单文本处理")
    print("-" * 70)
    sample1 = """
    多智能体系统是人工智能领域的一个热门研究方向。
    通过让多个专门的Agent协作，可以完成比单个Agent更复杂的任务。
    每个Agent都有自己的专长和职责，它们通过协调和通信来实现共同的目标。
    这种方式模拟了人类社会中的团队合作模式。
    """

    mas.process(sample1.strip())

    # 示例2: 复杂文本
    print("\n\n🟢 示例2: 复杂文档分析")
    print("-" * 70)
    sample2 = """
    # 人工智能技术的发展历程

    人工智能（Artificial Intelligence，简称AI）是计算机科学的一个重要分支，
    它致力于研究、开发用于模拟、延伸和扩展人的智能的理论、方法、技术及应用系统。

    ## 发展阶段

    人工智能的发展可以分为几个重要阶段：
    1. 诞生期（1950-1970年代）：图灵测试的提出，专家系统的出现
    2. 发展期（1980-1990年代）：机器学习算法的突破
    3. 爆发期（2000年代至今）：深度学习、大语言模型的快速发展

    ## 应用领域

    人工智能已经广泛应用于：
    - 自然语言处理
    - 计算机视觉
    - 智能推荐系统
    - 自动驾驶
    - 医疗诊断

    未来，人工智能将继续深刻改变我们的生活和工作方式。
    这是一个excellent的发展方向，我们都应该关注和拥抱这个趋势。
    """

    mas.process(sample2.strip())

    print("\n\n✅ 多Agent系统演示完成！")
    print("\n💡 提示:")
    print("   - 这个系统展示了4个Agent如何协作完成任务")
    print("   - 每个Agent专注于自己的职责范围")
    print("   - 通过WorkflowGraph实现工作流编排")
    print("   - 状态在Agent之间传递和更新")
    print("   - 可以扩展更多Agent或改变工作流程")


if __name__ == "__main__":
    main()
