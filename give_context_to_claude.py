#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速上下文加载器
给 Claude AI 提供完整的工作区上下文

使用方法:
在每次新对话开始时，运行此脚本，然后将输出粘贴给 Claude
"""

import sys
from pathlib import Path


def print_section(title):
    """打印分节标题"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def load_context():
    """加载完整的上下文信息"""

    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║     Office Agent Workspace - Claude AI 上下文信息                ║
║                                                                  ║
║     在新对话开始时，将此输出粘贴给 Claude                        ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)

    workspace_root = Path(__file__).parent

    # 1. 系统状态
    print_section("1. 当前系统状态")

    system_guide = workspace_root / "COMPLETE_SYSTEM_GUIDE.md"
    if system_guide.exists():
        print(f"[文件] {system_guide.name}")
        print("说明: 完整系统指南，包含所有工具和使用方式")
        print()

    # 2. 演进历史
    print_section("2. 最近演进历史")

    evolution_log = workspace_root / "06_Learning_Journal" / "evolution_log.json"
    if evolution_log.exists():
        import json
        with open(evolution_log, 'r', encoding='utf-8') as f:
            log = json.load(f)

        print(f"里程碑数量: {len(log.get('milestones', []))}")
        print()

        # 显示最近3个里程碑
        for milestone in log.get('milestones', [])[-3:]:
            print(f"[{milestone['date'][:10]}] {milestone['title']}")
            print(f"  影响: {', '.join(milestone.get('tools_affected', [])[:3])}")
            print()

    # 3. 工具列表
    print_section("3. 核心工具状态")

    tools = [
        ("file_organizer", "v1.0.0", "文件整理"),
        ("market_supervision_agent", "v3.0.0", "申请书生成"),
        ("memory_agent", "v1.0.0", "记忆助手"),
        ("agent_toolkit", "v1.0.0", "工具框架"),
        ("workflow_engine", "v1.0.0", "工作流引擎"),
        ("office_agent_studio", "v1.0.0", "统一GUI"),
    ]

    for name, version, desc in tools:
        print(f"  {name:25} {version:8} - {desc}")

    # 4. 工作区统计
    print_section("4. 工作区统计")

    index_file = workspace_root / "06_Learning_Journal" / "workspace_memory" / "workspace_index_latest.md"
    if index_file.exists():
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # 提取统计信息
            if "统计概览" in content:
                start = content.index("统计概览")
                end = content.index("##", start + 1) if "##" in content[start+1:] else len(content)
                print(content[start:end].strip())

    # 5. 下一步计划
    print_section("5. 下一步计划")

    if evolution_log.exists():
        for step in log.get('next_steps', [])[:3]:
            if step.get('status') == 'planned':
                priority = step.get('priority', '')
                print(f"  [{priority.upper()}] {step['title']}")
                print(f"       {step['description'][:60]}...")
                print()

    # 6. 关键文件位置
    print_section("6. 关键文件位置")

    key_files = [
        ("系统指南", "COMPLETE_SYSTEM_GUIDE.md"),
        ("演进系统说明", "00_Agent_Library/EVOLUTION_GUIDE.md"),
        ("版本管理", "00_Agent_Library/version_manager.py"),
        ("工具框架", "00_Agent_Library/agent_toolkit.py"),
        ("工作流引擎", "00_Agent_Library/workflow_engine.py"),
        ("统一GUI", "office_agent_studio.py"),
        ("版本注册表", "06_Learning_Journal/version_registry.json"),
        ("演进日志", "06_Learning_Journal/evolution_log.json"),
    ]

    for name, path in key_files:
        full_path = workspace_root / path
        exists = "✓" if full_path.exists() else "✗"
        print(f"  {exists} {name:15} - {path}")

    # 7. 快速命令
    print_section("7. 快速命令")

    commands = [
        ("启动GUI", "streamlit run office_agent_studio.py"),
        ("查看状态", "python 00_Agent_Library/version_manager.py"),
        ("运行测试", "python test_all_improvements.py"),
        ("文件整理", "python 01_Active_Projects/file_organizer/file_organizer.py"),
        ("申请书生成", "python 01_Active_Projects/market_supervision_agent/jinja2_filler.py --test"),
    ]

    for name, cmd in commands:
        print(f"  {name:10} : {cmd}")

    # 8. 给 Claude 的提示
    print_section("8. 给 Claude AI 的指示")

    print("""
Claude，现在你知道了工作区的完整状态。

关键点：
1. 我有 3 个核心工具 + 3 个框架
2. 最近进行了基于 zread 的全面升级
3. 有了完整的版本管理和演进追踪系统
4. 所有旧代码都保持兼容

我的期望：
- 你知道工作区的一切
- 你在做改动前会告诉我
- 你会保持向后兼容
- 你会记录所有变化

现在，等待我的具体指示。
    """)


if __name__ == "__main__":
    try:
        load_context()
    except Exception as e:
        print(f"\n[错误] {e}")
        import traceback
        traceback.print_exc()
