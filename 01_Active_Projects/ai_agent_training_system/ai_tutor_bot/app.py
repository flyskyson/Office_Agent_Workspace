#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI培训老师 - Streamlit应用
提供结构化学习路径和进度追踪

作者: Claude Code
日期: 2026-01-16
版本: 1.0.0
"""

import sys
from pathlib import Path

# 添加库路径
LIB_PATH = Path(__file__).parent.parent.parent / "00_Agent_Library"
sys.path.insert(0, str(LIB_PATH))

import streamlit as st
import json
from datetime import datetime
from typing import Dict, List, Any


# ============================================================================
# 页面配置
# ============================================================================

st.set_page_config(
    page_title="AI培训老师",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================================
# 学习路径定义
# ============================================================================

LEARNING_PATH = {
    "name": "AI Agent全栈开发实战",
    "description": "通过网上业务自动化项目，掌握AI Agent开发技能",
    "duration": "2-3周",
    "weeks": [
        {
            "week": 1,
            "title": "基础入门",
            "days": [
                {
                    "day": 1,
                    "title": "环境搭建与Playwright基础",
                    "tasks": [
                        "安装Python 3.12+",
                        "安装Playwright和浏览器",
                        "理解浏览器自动化概念",
                        "运行第一个Playwright脚本"
                    ],
                    "resources": [
                        "Playwright官方文档: https://playwright.dev/python/",
                        "项目文档: test_site/README.md"
                    ],
                    "exercises": [
                        "启动测试网站: python test_site/server.py",
                        "运行简单测试: python test_automation.py"
                    ],
                    "code_example": """
# 简单的Playwright示例
from playwright.async_api import async_playwright

async with async_playwright() as p:
    browser = await p.chromium.launch(headless=False)
    page = await browser.new_page()
    await page.goto("http://127.0.0.1:5555/login")
    await page.screenshot(path="screenshot.png")
    await browser.close()
                    """
                },
                {
                    "day": 2,
                    "title": "元素定位与页面操作",
                    "tasks": [
                        "学习CSS选择器",
                        "掌握元素定位方法",
                        "学习页面交互操作",
                        "理解等待机制"
                    ],
                    "resources": [
                        "CSS选择器指南",
                        "supervisor.py - LoginAgent代码"
                    ],
                    "exercises": [
                        "定位登录页面元素",
                        "实现自动填写用户名密码"
                    ]
                },
                {
                    "day": 3,
                    "title": "Streamlit入门",
                    "tasks": [
                        "安装Streamlit",
                        "理解Streamlit组件",
                        "创建简单应用",
                        "学习状态管理"
                    ],
                    "resources": [
                        "Streamlit文档: https://docs.streamlit.io/",
                        "本文件源码: ai_tutor_bot/app.py"
                    ],
                    "exercises": [
                        "创建Hello World应用",
                        "添加侧边栏和页面"
                    ]
                },
                {
                    "day": 4,
                    "title": "登录自动化实战",
                    "tasks": [
                        "分析登录页面结构",
                        "实现自动登录脚本",
                        "处理登录失败情况",
                        "添加截图和日志"
                    ],
                    "resources": [
                        "LoginAgent源码",
                        "测试网站: login.html"
                    ],
                    "exercises": [
                        "完成登录Agent开发",
                        "测试各种登录场景"
                    ]
                },
                {
                    "day": 5,
                    "title": "表单基础操作",
                    "tasks": [
                        "理解表单结构",
                        "学习表单元素定位",
                        "实现简单表单填写",
                        "理解数据映射"
                    ],
                    "resources": [
                        "FormAgent源码",
                        "HTML表单教程"
                    ],
                    "exercises": [
                        "填写测试表单",
                        "验证填写结果"
                    ]
                },
                {
                    "day": 6,
                    "title": "综合练习 - 简单自动化",
                    "tasks": [
                        "整合登录和表单",
                        "实现完整工作流",
                        "添加错误处理",
                        "编写测试用例"
                    ],
                    "exercises": [
                        "完成登录+表单自动化",
                        "通过所有测试"
                    ]
                },
                {
                    "day": 7,
                    "title": "周总结与回顾",
                    "tasks": [
                        "回顾本周学习内容",
                        "整理笔记和代码",
                        "完成周测验",
                        "准备下周学习"
                    ]
                }
            ]
        },
        {
            "week": 2,
            "title": "核心技术",
            "days": [
                {
                    "day": 8,
                    "title": "LangGraph基础",
                    "tasks": [
                        "理解状态机概念",
                        "学习LangGraph架构",
                        "理解WorkflowGraph",
                        "创建简单工作流"
                    ],
                    "resources": [
                        "LangGraph文档",
                        "workflow_engine.py源码"
                    ],
                    "code_example": """
# LangGraph工作流示例
from workflow_engine import WorkflowGraph, WorkflowStatus

class MyState:
    def __init__(self):
        self.value = 0

def increment(state: MyState) -> MyState:
    state.value += 1
    return state

# 创建工作流
workflow = WorkflowGraph("MyWorkflow", MyState)
workflow.add_step("increment", increment)
                    """
                },
                {
                    "day": 9,
                    "title": "Agent设计模式",
                    "tasks": [
                        "理解Agent概念",
                        "学习BaseAgent设计",
                        "实现自定义Agent",
                        "理解AgentResponse"
                    ],
                    "resources": [
                        "supervisor.py - BaseAgent",
                        "Agent设计模式文章"
                    ]
                },
                {
                    "day": 10,
                    "title": "多Agent协作",
                    "tasks": [
                        "理解监督者模式",
                        "学习Agent间通信",
                        "实现Agent协调",
                        "处理工作流状态"
                    ],
                    "resources": [
                        "AutomationSupervisor源码",
                        "多Agent架构图"
                    ]
                },
                {
                    "day": 11,
                    "title": "表单Agent深入",
                    "tasks": [
                        "处理复杂表单",
                        "动态表单识别",
                        "批量数据处理",
                        "添加数据验证"
                    ],
                    "resources": [
                        "FormAgent完整实现",
                        "表单验证最佳实践"
                    ]
                },
                {
                    "day": 12,
                    "title": "文件操作Agent",
                    "tasks": [
                        "理解文件上传机制",
                        "实现文件上传",
                        "实现文件下载",
                        "处理文件保存"
                    ],
                    "resources": [
                        "FileAgent源码",
                        "Playwright文件处理"
                    ]
                },
                {
                    "day": 13,
                    "title": "结果验证Agent",
                    "tasks": [
                        "设计验证策略",
                        "实现URL验证",
                        "实现内容验证",
                        "生成验证报告"
                    ],
                    "resources": [
                        "ValidationAgent源码",
                        "测试验证方法"
                    ]
                },
                {
                    "day": 14,
                    "title": "完整工作流实现",
                    "tasks": [
                        "整合所有Agent",
                        "实现完整自动化",
                        "添加日志系统",
                        "完成端到端测试"
                    ],
                    "exercises": [
                        "实现完整的申请自动化",
                        "通过所有测试用例"
                    ]
                }
            ]
        },
        {
            "week": 3,
            "title": "高级集成",
            "days": [
                {
                    "day": 15,
                    "title": "MCP工具集成",
                    "tasks": [
                        "理解MCP协议",
                        "学习MCP工具使用",
                        "集成MCP到Agent",
                        "实现工具调用"
                    ],
                    "resources": [
                        "MCP文档",
                        "mcp_tools.py示例"
                    ]
                },
                {
                    "day": 16,
                    "title": "错误处理与重试",
                    "tasks": [
                        "设计错误处理策略",
                        "实现自动重试",
                        "添加异常恢复",
                        "记录错误日志"
                    ]
                },
                {
                    "day": 17,
                    "title": "性能优化",
                    "tasks": [
                        "分析性能瓶颈",
                        "优化页面加载",
                        "减少等待时间",
                        "提升执行效率"
                    ]
                },
                {
                    "day": 18,
                    "title": "部署准备",
                    "tasks": [
                        "代码结构优化",
                        "添加配置管理",
                        "编写部署文档",
                        "准备生产环境"
                    ]
                },
                {
                    "day": 19,
                    "title": "系统测试",
                    "tasks": [
                        "编写完整测试套件",
                        "执行集成测试",
                        "性能压力测试",
                        "修复发现的问题"
                    ]
                },
                {
                    "day": 20,
                    "title": "项目总结",
                    "tasks": [
                        "整理项目文档",
                        "编写使用指南",
                        "总结学习心得",
                        "规划后续学习"
                    ]
                },
                {
                    "day": 21,
                    "title": "能力评估",
                    "tasks": [
                        "完成能力自评",
                        "进行项目演示",
                        "获得学习认证",
                        "开启下一段旅程"
                    ]
                }
            ]
        }
    ]
}


# ============================================================================
# 会话状态初始化
# ============================================================================

def init_session_state():
    """初始化会话状态"""
    if 'current_week' not in st.session_state:
        st.session_state.current_week = 1
    if 'current_day' not in st.session_state:
        st.session_state.current_day = 1
    if 'completed_tasks' not in st.session_state:
        st.session_state.completed_tasks = []
    if 'notes' not in st.session_state:
        st.session_state.notes = {}
    if 'progress' not in st.session_state:
        st.session_state.progress = 0
    if 'start_date' not in st.session_state:
        st.session_state.start_date = datetime.now().strftime("%Y-%m-%d")


# ============================================================================
# 辅助函数
# ============================================================================

def get_current_day_content():
    """获取当前天的学习内容"""
    for week in LEARNING_PATH["weeks"]:
        if week["week"] == st.session_state.current_week:
            for day in week["days"]:
                if day["day"] == st.session_state.current_day:
                    return day, week
    return None, None


def calculate_progress():
    """计算学习进度"""
    total_days = sum(len(week["days"]) for week in LEARNING_PATH["weeks"])
    completed_count = len(st.session_state.completed_tasks)
    return min(100, int((completed_count / total_days) * 100))


def toggle_task_wrapper(task_id):
    """切换任务状态的包装函数"""
    if task_id in st.session_state.completed_tasks:
        st.session_state.completed_tasks.remove(task_id)
    else:
        st.session_state.completed_tasks.append(task_id)
    st.session_state.progress = calculate_progress()


def save_progress():
    """保存学习进度"""
    progress_file = Path(__file__).parent / "data" / "progress.json"
    progress_file.parent.mkdir(exist_ok=True)

    progress_data = {
        "current_week": st.session_state.current_week,
        "current_day": st.session_state.current_day,
        "completed_tasks": st.session_state.completed_tasks,
        "notes": st.session_state.notes,
        "progress": st.session_state.progress,
        "start_date": st.session_state.start_date,
        "last_update": datetime.now().isoformat()
    }

    with open(progress_file, 'w', encoding='utf-8') as f:
        json.dump(progress_data, f, ensure_ascii=False, indent=2)


def load_progress():
    """加载学习进度"""
    progress_file = Path(__file__).parent / "data" / "progress.json"

    if progress_file.exists():
        with open(progress_file, 'r', encoding='utf-8') as f:
            progress_data = json.load(f)

        st.session_state.current_week = progress_data.get("current_week", 1)
        st.session_state.current_day = progress_data.get("current_day", 1)
        st.session_state.completed_tasks = progress_data.get("completed_tasks", [])
        st.session_state.notes = progress_data.get("notes", {})
        st.session_state.progress = progress_data.get("progress", 0)
        st.session_state.start_date = progress_data.get("start_date", datetime.now().strftime("%Y-%m-%d"))


# ============================================================================
# 页面渲染
# ============================================================================

def render_sidebar():
    """渲染侧边栏"""
    with st.sidebar:
        st.title("🎓 AI培训老师")

        # 学习进度
        st.subheader("📊 学习进度")
        progress_bar = st.progress(st.session_state.progress)
        st.caption(f"已完成: {st.session_state.progress}%")

        # 当前位置
        st.subheader("📍 当前位置")
        st.write(f"第 {st.session_state.current_week} 周")
        st.write(f"第 {st.session_state.current_day} 天")

        # 导航
        st.subheader("🧭 快速导航")

        # 选择周
        week_options = [f"第{w['week']}周: {w['title']}" for w in LEARNING_PATH["weeks"]]
        selected_week = st.selectbox("选择周", week_options, index=st.session_state.current_week - 1)

        # 选择天
        current_week_data = LEARNING_PATH["weeks"][st.session_state.current_week - 1]
        day_options = [f"第{d['day']}天: {d['title']}" for d in current_week_data["days"]]
        selected_day = st.selectbox("选择天", day_options, index=st.session_state.current_day - 1)

        # 更新位置
        if st.button("跳转到选中内容"):
            new_week = week_options.index(selected_week) + 1
            new_day = day_options.index(selected_day) + 1
            st.session_state.current_week = new_week
            st.session_state.current_day = new_day
            st.rerun()

        st.divider()

        # 操作按钮
        if st.button("💾 保存进度"):
            save_progress()
            st.success("进度已保存！")

        if st.button("📥 加载进度"):
            load_progress()
            st.success("进度已加载！")
            st.rerun()

        if st.button("🔄 重置进度"):
            st.session_state.current_week = 1
            st.session_state.current_day = 1
            st.session_state.completed_tasks = []
            st.session_state.notes = {}
            st.session_state.progress = 0
            st.success("进度已重置！")
            st.rerun()

        st.divider()

        # 项目链接
        st.subheader("🔗 项目链接")
        st.markdown("""
        - [测试网站](http://127.0.0.1:5555)
        - [源代码](../)
        - [文档](../../docs/)
        """)


def render_header(day_content, week_data):
    """渲染头部"""
    st.title(f"📚 第{day_content['day']}天: {day_content['title']}")
    st.caption(f"📅 第{week_data['week']}周 - {week_data['title']}")

    # 进度导航
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if st.button("⬅️ 上一天"):
            if st.session_state.current_day > 1:
                st.session_state.current_day -= 1
            else:
                if st.session_state.current_week > 1:
                    st.session_state.current_week -= 1
                    st.session_state.current_day = 7
            st.rerun()

    with col3:
        if st.button("下一天 ➡️"):
            if st.session_state.current_day < 7:
                st.session_state.current_day += 1
            else:
                if st.session_state.current_week < 3:
                    st.session_state.current_week += 1
                    st.session_state.current_day = 1
            st.rerun()

    st.divider()


def render_learning_content(day_content):
    """渲染学习内容"""
    # 学习任务
    st.subheader("📋 学习任务")
    task_key = f"w{st.session_state.current_week}_d{day_content['day']}"
    for i, task in enumerate(day_content.get("tasks", [])):
        task_id = f"{task_key}_task_{i}"
        is_completed = task_id in st.session_state.completed_tasks

        # 使用唯一的key，避免冲突
        checkbox_key = f"checkbox_{task_id}"

        col1, col2 = st.columns([1, 20])

        with col1:
            # 使用lambda捕获task_id，避免闭包问题
            st.checkbox(
                "",
                value=is_completed,
                key=checkbox_key,
                on_change=lambda tid=task_id: toggle_task_wrapper(tid)
            )

        with col2:
            st.write(task)

    # 学习资源
    if "resources" in day_content:
        st.subheader("📚 学习资源")
        for resource in day_content["resources"]:
            st.markdown(f"- {resource}")

    # 练习
    if "exercises" in day_content:
        st.subheader("✏️ 练习")
        for exercise in day_content["exercises"]:
            st.markdown(f"- {exercise}")

    # 代码示例
    if "code_example" in day_content:
        st.subheader("💻 代码示例")
        st.code(day_content["code_example"], language="python")


def render_notes_section(day_content):
    """渲染笔记区域"""
    st.subheader("📝 学习笔记")

    note_key = f"w{st.session_state.current_week}_d{day_content['day']}"
    current_note = st.session_state.notes.get(note_key, "")

    note = st.text_area(
        "记录你的学习心得、问题和想法...",
        value=current_note,
        height=200,
        key=f"note_{note_key}"
    )

    if st.button("保存笔记"):
        st.session_state.notes[note_key] = note
        st.success("笔记已保存！")


def render_chat_section():
    """渲染AI问答区域"""
    st.subheader("🤖 AI答疑")

    # 初始化聊天历史
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # 显示聊天历史
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # 聊天输入
    if prompt := st.chat_input("有什么问题，随时问我..."):
        # 添加用户消息
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        # 显示用户消息
        with st.chat_message("user"):
            st.write(prompt)

        # 模拟AI回复（实际应该调用AI模型）
        with st.chat_message("assistant"):
            response = f"这是一个很好的问题！关于'{prompt}'，我建议你...\n\n（注：这是模拟回复，实际应集成AI模型）"
            st.write(response)

        # 添加AI回复
        st.session_state.chat_history.append({"role": "assistant", "content": response})


# ============================================================================
# 主函数
# ============================================================================

def main():
    """主函数"""
    # 初始化会话状态
    init_session_state()

    # 尝试加载进度
    if st.session_state.start_date == datetime.now().strftime("%Y-%m-%d"):
        load_progress()

    # 渲染侧边栏
    render_sidebar()

    # 获取当前内容
    day_content, week_data = get_current_day_content()

    if day_content is None:
        st.error("找不到当前学习内容！")
        return

    # 渲染头部
    render_header(day_content, week_data)

    # 创建标签页
    tab1, tab2, tab3 = st.tabs(["📖 学习内容", "📝 笔记", "🤖 AI答疑"])

    with tab1:
        render_learning_content(day_content)

    with tab2:
        render_notes_section(day_content)

    with tab3:
        render_chat_section()


if __name__ == "__main__":
    main()
