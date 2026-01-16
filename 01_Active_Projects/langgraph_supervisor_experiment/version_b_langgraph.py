#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
版本B: 使用 LangGraph 实现 Supervisor 模式

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
from typing import TypedDict, Literal, Annotated
from operator import add

# LangGraph 导入
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent

# Windows 编码修复
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    except:
        pass


# ============================================================================
# 状态定义
# ============================================================================

class SupervisorState(TypedDict):
    """Supervisor 工作流状态"""
    task: str                          # 用户任务
    workflow_started: bool              # 工作流是否启动
    step_index: int                     # 当前步骤索引
    current_step: str                   # 当前步骤
    research_data: dict                 # 研究数据
    research_completed: bool            # 研究是否完成
    draft: str                          # 文档草稿
    write_completed: bool               # 写作是否完成
    review_passed: bool                 # 审查是否通过
    review_issues: list                 # 审查问题
    review_comments: str                # 审查意见


# ============================================================================
# Agent 实现 (节点函数)
# ============================================================================

def supervisor_node(state: SupervisorState) -> SupervisorState:
    """
    Supervisor 节点 - 协调任务分配

    这是 LangGraph 风格的节点: 接收状态，返回更新
    """
    task = state.get("task", "")
    step_index = state.get("step_index", 0)

    if not state.get("workflow_started", False):
        # 首次执行
        print(f"  [Supervisor] 收到任务: {task}")
        print(f"  [Supervisor] 启动工作流，第一步: research")

        return {
            **state,
            "workflow_started": True,
            "step_index": 0,
            "current_step": "research"
        }

    # 根据当前步骤决定下一步
    steps = ["research", "write", "review"]
    current_step_name = steps[step_index]

    print(f"  [Supervisor] 步骤 '{current_step_name}' 完成")

    # 移动到下一步
    next_index = step_index + 1
    if next_index < len(steps):
        next_step = steps[next_index]
        print(f"  [Supervisor] 下一步: {next_step}")
        return {
            **state,
            "step_index": next_index,
            "current_step": next_step
        }
    else:
        print(f"  [Supervisor] 所有步骤完成")
        return state


def research_node(state: SupervisorState) -> SupervisorState:
    """
    Researcher 节点 - 研究文档内容
    """
    task = state.get("task", "")
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

    print(f"  [Researcher] 研究完成，找到 {len(research_data['key_points'])} 个重点")

    return {
        **state,
        "research_data": research_data,
        "research_completed": True
    }


def write_node(state: SupervisorState) -> SupervisorState:
    """
    Writer 节点 - 撰写文档
    """
    research_data = state.get("research_data", {})
    print(f"  [Writer] 正在撰写文档...")

    # 模拟写作过程
    draft = f"""
# {research_data.get('topic', '未命名文档')}

## 概述
本文档主要讨论{research_data.get('topic', '相关主题')}。

## 主要内容
"""

    for point in research_data.get("key_points", []):
        draft += f"\n- {point}\n"

    draft += f"\n## 参考资料\n"
    for source in research_data.get("sources", []):
        draft += f"- {source}\n"

    print(f"  [Writer] 初稿完成，字数: {len(draft)}")

    return {
        **state,
        "draft": draft,
        "write_completed": True
    }


def review_node(state: SupervisorState) -> SupervisorState:
    """
    Reviewer 节点 - 审查文档
    """
    draft = state.get("draft", "")
    print(f"  [Reviewer] 正在审查文档...")

    # 模拟审查过程
    word_count = len(draft)
    issues = []

    if word_count < 100:
        issues.append("文档内容过短")
    if "参考资料" not in draft:
        issues.append("缺少参考资料")

    if issues:
        print(f"  [Reviewer] 审查未通过，发现 {len(issues)} 个问题")
        return {
            **state,
            "review_passed": False,
            "review_issues": issues
        }
    else:
        print(f"  [Reviewer] 审查通过！")
        return {
            **state,
            "review_passed": True,
            "review_comments": "文档质量良好"
        }


# ============================================================================
# 路由函数
# ============================================================================

def supervisor_router(state: SupervisorState) -> Literal["research", "write", "review", "__end__"]:
    """
    Supervisor 路由函数

    根据步骤索引决定下一个节点
    """
    step_index = state.get("step_index", 0)

    if step_index == 0:
        return "research"
    elif step_index == 1:
        return "write"
    elif step_index == 2:
        return "review"
    else:
        # 所有步骤完成，结束
        return "__end__"


def review_to_supervisor_router(state: SupervisorState) -> Literal["supervisor", "__end__"]:
    """
    Review 完成后的路由

    决定是继续下一轮还是结束
    """
    step_index = state.get("step_index", 0)

    # 检查是否完成所有步骤
    if step_index >= 2:  # 已经完成了 review (步骤 2)
        return "__end__"
    else:
        return "supervisor"


# ============================================================================
# 创建工作流
# ============================================================================

def create_langgraph_supervisor():
    """
    创建 LangGraph Supervisor 工作流

    返回:
        编译后的 LangGraph
    """
    # 创建状态图
    workflow = StateGraph(SupervisorState)

    # 添加节点
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("research", research_node)
    workflow.add_node("write", write_node)
    workflow.add_node("review", review_node)

    # 设置入口
    workflow.set_entry_point("supervisor")

    # 添加条件边 - Supervisor 决策
    workflow.add_conditional_edges(
        "supervisor",
        supervisor_router,
        {
            "research": "research",
            "write": "write",
            "review": "review",
            "__end__": END
        }
    )

    # 添加返回到 supervisor 的边
    workflow.add_edge("research", "supervisor")
    workflow.add_edge("write", "supervisor")

    # review 完成后，检查是否结束或回到 supervisor
    workflow.add_conditional_edges(
        "review",
        review_to_supervisor_router,
        {
            "supervisor": "supervisor",
            "__end__": END
        }
    )

    # 编译
    return workflow.compile()


# ============================================================================
# 主函数
# ============================================================================

def main():
    """运行版本B实验"""
    print("=" * 70)
    print("版本B: LangGraph Supervisor 模式")
    print("=" * 70)

    # 创建工作流
    workflow = create_langgraph_supervisor()

    # 准备初始状态
    initial_state: SupervisorState = {
        "task": "如何提高工作效率",
        "workflow_started": False,
        "step_index": 0,
        "current_step": "",
        "research_data": {},
        "research_completed": False,
        "draft": "",
        "write_completed": False,
        "review_passed": False,
        "review_issues": [],
        "review_comments": ""
    }

    print("\n📋 测试任务: " + initial_state["task"])
    print("\n开始执行...\n")

    # 执行工作流
    result = workflow.invoke(initial_state)

    # 输出结果
    print("\n" + "=" * 70)
    print("执行结果")
    print("=" * 70)

    draft = result.get("draft", "")
    review_passed = result.get("review_passed", False)

    print(f"审查通过: {review_passed}")

    if draft:
        print(f"\n生成的文档:")
        print(draft)

    if not review_passed:
        issues = result.get("review_issues", [])
        print(f"\n审查问题:")
        for issue in issues:
            print(f"  - {issue}")

    print("\n最终状态:")
    for key, value in result.items():
        if key not in ["draft", "research_data"]:
            print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
