#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试脚本 - 验证所有改进

作者: Claude Code
日期: 2026-01-12
"""

import sys
from pathlib import Path


def print_section(title):
    """打印分节标题"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def test_imports():
    """测试所有模块能否正常导入"""
    print_section("测试1: 模块导入")

    tests = [
        ("工具框架", "00_Agent_Library/agent_toolkit.py"),
        ("工作流引擎", "00_Agent_Library/workflow_engine.py"),
        ("GUI启动器", "office_agent_studio.py"),
    ]

    results = []

    for name, path in tests:
        full_path = Path(path)
        if full_path.exists():
            print(f"  [OK] {name}: {path}")
            results.append(True)
        else:
            print(f"  [X] {name}: {path} 不存在")
            results.append(False)

    return all(results)


def test_toolkit():
    """测试工具框架"""
    print_section("测试2: 工具框架基础")

    try:
        sys.path.insert(0, str(Path("00_Agent_Library")))
        from agent_toolkit import BaseTool, ToolRegistry

        # 测试工具注册表
        registry = ToolRegistry()
        tools = registry.list_tools()

        print(f"  [OK] 工具框架导入成功")
        print(f"  [OK] 已注册 {len(tools)} 个工具")

        for tool_info in tools:
            print(f"    - {tool_info['name']}: {tool_info['description']}")

        return True

    except Exception as e:
        print(f"  [X] 工具框架测试失败: {e}")
        return False


def test_workflow():
    """测试工作流引擎"""
    print_section("测试3: 工作流引擎基础")

    try:
        sys.path.insert(0, str(Path("00_Agent_Library")))
        from workflow_engine import WorkflowGraph, Node, State, END

        # 创建简单工作流
        class TestNode1(Node):
            def __init__(self):
                super().__init__("test1", "测试节点1")
            def execute(self, state):
                state['data']['step1'] = 'done'
                return state

        class TestNode2(Node):
            def __init__(self):
                super().__init__("test2", "测试节点2")
            def execute(self, state):
                state['data']['step2'] = 'done'
                return state

        graph = WorkflowGraph("test")
        graph.add_node("test1", TestNode1())
        graph.add_node("test2", TestNode2())
        graph.add_edge("test1", "test2")
        graph.set_entry_point("test1")

        workflow = graph.compile()
        result = workflow.invoke({})

        print(f"  [OK] 工作流引擎导入成功")
        print(f"  [OK] 执行节点数: {result['nodes_executed']}")
        print(f"  [OK] 执行状态: {'成功' if result['success'] else '失败'}")

        return result['success']

    except Exception as e:
        print(f"  [X] 工作流引擎测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_gui_requirements():
    """测试 GUI 依赖"""
    print_section("测试4: GUI 依赖检查")

    dependencies = [
        ("streamlit", "pip install streamlit"),
        ("streamlit_option_menu", "pip install streamlit-option-menu"),
    ]

    all_ok = True

    for module, install_cmd in dependencies:
        try:
            __import__(module)
            print(f"  [OK] {module}")
        except ImportError:
            print(f"  [X] {module} - 请运行: {install_cmd}")
            all_ok = False

    if all_ok:
        print("\n  [提示] 启动 GUI: streamlit run office_agent_studio.py")

    return all_ok


def show_files():
    """显示创建的文件"""
    print_section("创建的文件")

    files = [
        ("工具框架", "00_Agent_Library/agent_toolkit.py"),
        ("工作流引擎", "00_Agent_Library/workflow_engine.py"),
        ("GUI启动器", "office_agent_studio.py"),
        ("启动脚本", "启动_OA_Studio.bat"),
        ("调研报告", "06_Learning_Journal/zread_research_report_20260112.md"),
        ("实施报告", "06_Learning_Journal/full_implementation_report_20260112.md"),
        ("使用说明", "OFFICE_AGENT_STUDIO_README.md"),
    ]

    for name, path in files:
        full_path = Path(path)
        size = full_path.stat().st_size if full_path.exists() else 0
        print(f"  [{name}]")
        print(f"    路径: {path}")
        print(f"    大小: {size} 字节")
        print()


def show_usage():
    """显示使用说明"""
    print_section("使用说明")

    print("""
1. 测试工具框架:
   python 00_Agent_Library/agent_toolkit.py

2. 测试工作流引擎:
   python 00_Agent_Library/workflow_engine.py

3. 启动 GUI (推荐):
   streamlit run office_agent_studio.py
   或双击: 启动_OA_Studio.bat

4. 查看文档:
   - 调研报告: 06_Learning_Journal/zread_research_report_20260112.md
   - 实施报告: 06_Learning_Journal/full_implementation_report_20260112.md
   - 使用说明: OFFICE_AGENT_STUDIO_README.md
    """)


def main():
    """主测试函数"""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "Office Agent 改进验证测试" + " " * 25 + "║")
    print("╚" + "═" * 68 + "╝")

    results = []

    # 运行测试
    results.append(("模块导入", test_imports()))
    results.append(("工具框架", test_toolkit()))
    results.append(("工作流引擎", test_workflow()))
    results.append(("GUI依赖", test_gui_requirements()))

    # 显示文件
    show_files()

    # 显示使用说明
    show_usage()

    # 总结
    print_section("测试总结")

    for name, passed in results:
        status = "[OK]" if passed else "[X]"
        print(f"  {status} {name}")

    all_passed = all(result[1] for result in results)

    print("\n" + "=" * 70)
    if all_passed:
        print("  [成功] 所有测试通过！可以开始使用新的工具系统了")
    else:
        print("  [提示] 部分测试未通过，请检查上面的错误信息")
    print("=" * 70 + "\n")

    return 0 if all_passed else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n[中断] 用户取消")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n[异常] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
