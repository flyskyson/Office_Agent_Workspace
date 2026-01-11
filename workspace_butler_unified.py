#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工作区管家 - 统一主程序
整合所有管家功能，提供单一入口点
"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

# 设置控制台编码为UTF-8
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


class WorkspaceButler:
    """工作区管家 - 统一管理接口"""

    def __init__(self, workspace_root=None):
        if workspace_root is None:
            workspace_root = Path(__file__).parent
        self.workspace_root = Path(workspace_root)
        self.memory_dir = self.workspace_root / "06_Learning_Journal" / "workspace_memory"

        # 工具映射
        self.tools = {
            'scanner': 'workspace_scanner.py',
            'super_butler': '超级管家.py',
            'file_manager': 'file_manager_center.py',
            'project_tracker': 'project_tracker.py',
            'project_query': '智能管家项目查询.py',
            'daily_launcher': 'daily_launcher.py',
            'memory_agent': '01_Active_Projects/memory_agent/memory_agent.py',
        }

    def show_status(self):
        """显示工作区状态"""
        print("\n" + "=" * 70)
        print("🏠 工作区管家状态")
        print("=" * 70)
        print(f"\n📍 工作区: {self.workspace_root}")
        print(f"📅 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # 加载并显示项目进度
        try:
            result = subprocess.run(
                [sys.executable, str(self.workspace_root / self.tools['project_query']), 'list'],
                capture_output=True,
                encoding='utf-8',
                check=True
            )
            print(result.stdout)
        except Exception as e:
            print(f"\n⚠️  无法加载项目信息: {e}")

    def show_menu(self):
        """显示主菜单"""
        print("\n" + "=" * 70)
        print("🎯 管家服务菜单")
        print("=" * 70)
        print("\n📊 信息查询")
        print("  1. 查看工作区状态")
        print("  2. 查看所有项目进度")
        print("  3. 查看特定项目状态")
        print("  4. 生成智能推荐")
        print("\n🧠 知识管理")
        print("  5. 学习记忆助手")
        print("\n🛠️ 工具执行")
        print("  6. 扫描工作区")
        print("  7. 文件管理中心")
        print("  8. 今日启动器")
        print("\n📝 项目管理")
        print("  9. 记录项目进度")
        print("  10. 暂停/恢复项目")
        print("\n  0. 退出")
        print()

    def run_tool(self, tool_name, args=None):
        """运行工具"""
        if tool_name not in self.tools:
            print(f"❌ 未知工具: {tool_name}")
            return False

        tool_path = self.workspace_root / self.tools[tool_name]

        if not tool_path.exists():
            print(f"❌ 工具不存在: {tool_path}")
            return False

        cmd = [sys.executable, str(tool_path)]
        if args:
            cmd.extend(args)

        try:
            subprocess.run(cmd, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ 工具运行失败: {e}")
            return False

    def interactive_mode(self):
        """交互模式"""
        while True:
            self.show_status()
            self.show_menu()

            choice = input("请选择操作 (0-9): ").strip()

            if choice == '0':
                print("\n👋 再见！祝工作愉快！")
                break

            elif choice == '1':
                self.show_status()

            elif choice == '2':
                self.run_tool('project_query', ['list'])

            elif choice == '3':
                project = input("请输入项目名: ").strip()
                self.run_tool('project_query', ['status', project])

            elif choice == '4':
                self.run_tool('project_query', ['recommend'])

            elif choice == '5':
                print("\n启动学习记忆助手...")
                self.run_tool('memory_agent')

            elif choice == '6':
                print("\n正在扫描工作区...")
                self.run_tool('scanner')

            elif choice == '7':
                print("\n启动文件管理中心...")
                subprocess.run([sys.executable, str(self.workspace_root / 'file_manager_center.py')])

            elif choice == '8':
                print("\n启动今日启动器...")
                subprocess.run([sys.executable, str(self.workspace_root / 'daily_launcher.py')])

            elif choice == '9':
                project = input("项目名: ").strip()
                progress = input("进度%: ").strip()
                task = input("当前任务: ").strip()
                self.run_tool('project_tracker', ['update', project, progress, task])

            elif choice == '10':
                print("\n暂停项目: pause | 恢复项目: resume")
                action = input("操作 (pause/resume): ").strip()
                project = input("项目名: ").strip()
                self.run_tool('project_tracker', [action, project])

            else:
                print("\n❌ 无效选项")

            input("\n按回车继续...")


def main():
    """主函数"""
    import sys

    butler = WorkspaceButler()

    # 检查命令行参数
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == 'status':
            butler.show_status()

        elif command == 'interactive':
            butler.interactive_mode()

        else:
            print(f"未知命令: {command}")
            print("\n可用命令:")
            print("  status       - 查看状态")
            print("  interactive  - 交互模式")
    else:
        # 默认显示状态
        print("\n🏠 工作区管家 - 统一入口")
        print("\n使用方法:")
        print("  python workspace_butler_unified.py status       - 查看状态")
        print("  python workspace_butler_unified.py interactive  - 交互模式")
        print("\n快速查看状态...")
        butler.show_status()


if __name__ == "__main__":
    main()
