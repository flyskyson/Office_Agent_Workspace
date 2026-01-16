#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
版本A: 使用 WorkflowEngine 实现 Supervisor 模式

任务: 文档处理团队
- Supervisor: 协调任务分配
- Researcher: 研究文档内容
- Writer: 撰写文档
- Reviewer: 审查文档

作者: Claude Code
日期: 2026-01-15
"""

import sys
from pathlib import Path
from typing import Dict, List, Any, Literal

# 导入 WorkflowEngine
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "00_Agent_Library"))
from workflow_engine import (
    WorkflowGraph, Node, State, END,
    ConditionalEdge
)

# Windows 编码修复
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    except:
        pass


# ============================================================================
# Agent 实现
# ============================================================================

class SupervisorAgent(Node):
    """
    Supervisor Agent - 协调任务分配

    职责:
    1. 接收用户请求
    2. 决定下一步调用哪个 Agent
    3. 监控任务进度
    """

    def __init__(self):
        super().__init__(
            "supervisor",
            "协调文档处理任务"
        )
        self.task_sequence = ["research", "write", "review"]
        self.current_step = 0

    def execute(self, state: State) -> State:
        """执行协调逻辑"""
        task = state['data'].get('task', '')

        if not state['data'].get('workflow_started', False):
            # 首次执行，初始化工作流
            state['data']['workflow_started'] = True
            state['data']['current_step'] = 'research'
            state['data']['step_index'] = 0
            print(f"  [Supervisor] 收到任务: {task}")
            print(f"  [Supervisor] 启动工作流，第一步: research")

        return state


class ResearcherAgent(Node):
    """
    Researcher Agent - 研究文档内容

    职责:
    1. 分析文档主题
    2. 收集相关资料
    3. 提取关键信息
    """

    def __init__(self):
        super().__init__(
            "researcher",
            "研究文档内容并收集资料"
        )

    def execute(self, state: State) -> State:
        """执行研究"""
        task = state['data'].get('task', '')
        print(f"  [Researcher] 正在研究: {task}")

        # 模拟研究过程
        research_data = {
            "topic": task,
            "key_points": [
                f"关于'{task}'的重点1",
                f"关于'{task}'的重点2",
                f"关于'{task}'的重点3"
            ],
            "sources": ["资料A", "资料B", "资料C"]
        }

        state['data']['research_data'] = research_data
        state['data']['research_completed'] = True

        print(f"  [Researcher] 研究完成，找到 {len(research_data['key_points'])} 个重点")

        return state


class WriterAgent(Node):
    """
    Writer Agent - 撰写文档

    职责:
    1. 根据研究资料撰写文档
    2. 组织内容结构
    3. 生成初稿
    """

    def __init__(self):
        super().__init__(
            "writer",
            "根据研究结果撰写文档"
        )

    def execute(self, state: State) -> State:
        """执行写作"""
        research_data = state['data'].get('research_data', {})
        print(f"  [Writer] 正在撰写文档...")

        # 模拟写作过程
        draft = f"""
# {research_data.get('topic', '未命名文档')}

## 概述
本文档主要讨论{research_data.get('topic', '相关主题')}。

## 主要内容
"""

        for point in research_data.get('key_points', []):
            draft += f"\n- {point}\n"

        draft += f"\n## 参考资料\n"
        for source in research_data.get('sources', []):
            draft += f"- {source}\n"

        state['data']['draft'] = draft
        state['data']['write_completed'] = True

        print(f"  [Writer] 初稿完成，字数: {len(draft)}")

        return state


class ReviewerAgent(Node):
    """
    Reviewer Agent - 审查文档

    职责:
    1. 审查文档质量
    2. 提出修改意见
    3. 决定是否通过
    """

    def __init__(self):
        super().__init__(
            "reviewer",
            "审查文档质量"
        )

    def execute(self, state: State) -> State:
        """执行审查"""
        draft = state['data'].get('draft', '')
        print(f"  [Reviewer] 正在审查文档...")

        # 模拟审查过程
        word_count = len(draft)
        issues = []

        if word_count < 100:
            issues.append("文档内容过短")
        if "参考资料" not in draft:
            issues.append("缺少参考资料")

        if issues:
            state['data']['review_passed'] = False
            state['data']['review_issues'] = issues
            print(f"  [Reviewer] 审查未通过，发现 {len(issues)} 个问题")
        else:
            state['data']['review_passed'] = True
            state['data']['review_comments'] = "文档质量良好"
            print(f"  [Reviewer] 审查通过！")

        return state


# ============================================================================
# 辅助函数
# ============================================================================

def supervisor_router(state: State) -> str:
    """
    Supervisor 路由函数

    根据当前状态决定下一个 Agent
    """
    step_index = state['data'].get('step_index', 0)

    if step_index == 0:
        return "research"
    elif step_index == 1:
        return "write"
    elif step_index == 2:
        return "review"
    else:
        return "end"


# ============================================================================
# 创建工作流
# ============================================================================

def create_supervisor_workflow(enable_checkpoints: bool = True, enable_visualization: bool = True):
    """
    创建 Supervisor 工作流

    参数:
        enable_checkpoints: 是否启用检查点
        enable_visualization: 是否启用可视化

    返回:
        编译后的工作流
    """
    # 创建工作流图
    graph = WorkflowGraph(
        "document_processing",
        enable_checkpoints=enable_checkpoints,
        enable_visualization=enable_visualization
    )

    # 添加节点
    graph.add_node("supervisor", SupervisorAgent())
    graph.add_node("research", ResearcherAgent())
    graph.add_node("write", WriterAgent())
    graph.add_node("review", ReviewerAgent())

    # 添加边 - Supervisor 调度流程
    graph.add_edge("supervisor", "research")
    graph.add_edge("research", "supervisor")
    graph.add_edge("write", "supervisor")
    graph.add_edge("review", "supervisor")

    # 添加条件边 - Supervisor 决策
    graph.add_conditional_edge(
        "supervisor",
        supervisor_router,
        {
            "research": "research",
            "write": "write",
            "review": "review",
            "end": END
        }
    )

    # 设置入口
    graph.set_entry_point("supervisor")

    return graph.compile()


# ============================================================================
# 主函数
# ============================================================================

def main():
    """运行版本A实验"""
    print("=" * 70)
    print("版本A: WorkflowEngine Supervisor 模式")
    print("=" * 70)

    # 创建工作流（启用所有功能）
    workflow = create_supervisor_workflow(
        enable_checkpoints=True,
        enable_visualization=True
    )

    # 准备测试数据
    test_data = {
        "task": "如何提高工作效率"
    }

    print("\n📋 测试任务: " + test_data["task"])
    print("\n开始执行...\n")

    # 执行工作流
    result = workflow.invoke(test_data)

    # 输出结果
    print("\n" + "=" * 70)
    print("执行结果")
    print("=" * 70)
    print(f"节点执行数: {result['nodes_executed']}")
    print(f"成功: {result['success']}")
    print(f"检查点数: {result['checkpoints_created']}")

    if result['success']:
        draft = result['state']['data'].get('draft', '')
        print(f"\n生成的文档:")
        print(draft)

    # 可视化
    print("\n" + "=" * 70)
    print("工作流可视化")
    print("=" * 70)
    graph = WorkflowGraph(
        "document_processing",
        enable_checkpoints=True,
        enable_visualization=True
    )
    # 重新创建图以获取可视化
    graph.add_node("supervisor", SupervisorAgent())
    graph.add_node("research", ResearcherAgent())
    graph.add_node("write", WriterAgent())
    graph.add_node("review", ReviewerAgent())
    graph.add_edge("supervisor", "research")
    graph.add_edge("research", "supervisor")
    graph.add_edge("write", "supervisor")
    graph.add_edge("review", "supervisor")
    graph.add_conditional_edge(
        "supervisor",
        supervisor_router,
        {"research": "research", "write": "write", "review": "review", "end": END}
    )
    graph.set_entry_point("supervisor")

    print("\nMermaid 图表:")
    print(graph.visualize("mermaid"))

    # 保存 HTML
    html_file = "version_a_workflow.html"
    graph.save_visualization(html_file)
    print(f"\n✅ HTML 可视化已保存: {html_file}")

    # 检查点统计
    stats = graph.get_checkpoint_stats()
    print(f"\n检查点统计:")
    print(f"  总数: {stats['total_checkpoints']}")
    print(f"  大小: {stats['total_size_mb']} MB")


if __name__ == "__main__":
    main()
