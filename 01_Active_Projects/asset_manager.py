#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工作区资产盘点命令中心
让你随时了解自己的"家底" - 项目、工具、文档、代码
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
import sys


class AssetCommandCenter:
    """资产盘点命令中心"""

    def __init__(self, workspace_root=None):
        """初始化命令中心"""
        if workspace_root is None:
            workspace_root = Path(__file__).parent
        else:
            workspace_root = Path(workspace_root)

        self.workspace_root = workspace_root
        self.index_file = workspace_root / "06_Learning_Journal" / "workspace_memory" / "workspace_index_latest.json"

    def load_index(self):
        """加载工作区索引"""
        if not self.index_file.exists():
            print("❌ 工作区索引不存在!")
            print(f"   请先运行: python workspace_scanner.py")
            return None

        with open(self.index_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def show_dashboard(self):
        """显示资产总览仪表盘"""
        print("\n" + "="*70)
        print("工作区资产总览".center(70))
        print("="*70)

        data = self.load_index()
        if not data:
            return

        scan_time = data.get('scan_time', '未知')
        print(f"\n最后扫描: {scan_time}\n")

        # 项目统计
        projects = data.get('projects', [])
        active_projects = [p for p in projects if p.get('status') == 'active']
        archived_projects = [p for p in projects if p.get('status') == 'archived']

        print("项目资产:")
        print(f"   - 活跃项目: {len(active_projects)} 个")
        print(f"   - 归档项目: {len(archived_projects)} 个")
        print(f"   - 总计: {len(projects)} 个")

        # 文件统计
        total_py = sum(p.get('py_files_count', 0) for p in projects)
        total_js = sum(p.get('js_files_count', 0) for p in projects)
        total_doc = sum(p.get('doc_files_count', 0) for p in projects)

        print(f"\n代码资产:")
        print(f"   - Python文件: {total_py} 个")
        print(f"   - JavaScript文件: {total_js} 个")
        print(f"   - 文档文件: {total_doc} 个")

        # 工具统计
        tools = data.get('tools', [])
        scripts = data.get('scripts', [])

        print(f"\n工具资产:")
        print(f"   - 工具脚本: {len(tools)} 个")
        print(f"   - 批处理脚本: {len(scripts)} 个")

        # 提示信息
        print(f"\n输入 'help' 查看可用命令\n")

    def show_projects(self, status='active'):
        """显示项目列表"""
        data = self.load_index()
        if not data:
            return

        projects = data.get('projects', [])

        if status == 'active':
            projects = [p for p in projects if p.get('status') == 'active']
            title = "🚀 活跃项目"
        elif status == 'archived':
            projects = [p for p in projects if p.get('status') == 'archived']
            title = "📦 归档项目"
        else:
            title = "📁 所有项目"

        print(f"\n{title} ({len(projects)}个)")
        print("-" * 70)

        for i, project in enumerate(projects, 1):
            name = project.get('name', '未知')
            path = project.get('path', '')
            py_count = project.get('py_files_count', 0)
            last_modified = project.get('last_modified', '未知')

            # 计算闲置天数
            try:
                modified_time = datetime.strptime(last_modified, '%Y-%m-%d %H:%M:%S')
                days_idle = (datetime.now() - modified_time).days
                idle_info = f"({days_idle}天前更新)"
            except:
                idle_info = ""

            has_readme = "✅" if project.get('has_readme') else "❌"

            print(f"\n{i}. {name}")
            print(f"   路径: {path}")
            print(f"   文件: {py_count}个Python文件 | {has_readme} README")
            print(f"   更新: {last_modified} {idle_info}")

            # 显示主要脚本
            main_scripts = project.get('main_scripts', [])[:3]
            if main_scripts:
                print(f"   主要脚本:")
                for script in main_scripts:
                    script_name = script.get('name', '')
                    script_size = script.get('size', 0)
                    print(f"      • {script_name} ({script_size:,} bytes)")

        print()

    def show_tools(self):
        """显示工具脚本"""
        data = self.load_index()
        if not data:
            return

        tools = data.get('tools', [])
        scripts = data.get('scripts', [])

        print("\n🛠️  工具脚本资产")
        print("-" * 70)

        if tools:
            print(f"\n📌 Python工具 ({len(tools)}个):")
            for tool in tools:
                name = tool.get('name', '')
                modified = tool.get('modified', '')
                print(f"   • {name:30s} | {modified}")

        if scripts:
            print(f"\n📌 批处理脚本 ({len(scripts)}个):")
            for script in scripts:
                name = script.get('name', '')
                modified = script.get('modified', '')
                print(f"   • {name:30s} | {modified}")

        print()

    def show_recent_updates(self, days=7):
        """显示最近更新"""
        data = self.load_index()
        if not data:
            return

        print(f"\n🕒 最近{days}天的更新")
        print("-" * 70)

        cutoff_date = datetime.now() - timedelta(days=days)
        recent_projects = []

        projects = data.get('projects', [])
        for project in projects:
            last_modified = project.get('last_modified', '')
            try:
                modified_time = datetime.strptime(last_modified, '%Y-%m-%d %H:%M:%S')
                if modified_time >= cutoff_date:
                    recent_projects.append({
                        'name': project.get('name'),
                        'modified': last_modified,
                        'time': modified_time
                    })
            except:
                pass

        if recent_projects:
            # 按时间排序
            recent_projects.sort(key=lambda x: x['time'], reverse=True)

            for proj in recent_projects:
                print(f"   • {proj['name']:30s} | {proj['modified']}")
        else:
            print(f"   最近{days}天没有项目更新")

        print()

    def show_health_check(self):
        """健康检查"""
        data = self.load_index()
        if not data:
            return

        print("\n🏥 工作区健康检查")
        print("-" * 70)

        issues = []

        # 检查项目是否有README
        projects = data.get('projects', [])
        active_projects = [p for p in projects if p.get('status') == 'active']

        for project in active_projects:
            if not project.get('has_readme'):
                issues.append(f"⚠️  项目 '{project['name']}' 缺少README文档")

            # 检查长时间未更新
            last_modified = project.get('last_modified', '')
            try:
                modified_time = datetime.strptime(last_modified, '%Y-%m-%d %H:%M:%S')
                days_idle = (datetime.now() - modified_time).days
                if days_idle > 30:
                    issues.append(f"⚠️  项目 '{project['name']}' 已{days_idle}天未更新")
            except:
                pass

        if issues:
            print("\n发现以下问题:")
            for issue in issues:
                print(f"   {issue}")
            print(f"\n共 {len(issues)} 个问题需要关注")
        else:
            print("✅ 工作区状态良好,没有发现问题")

        print()

    def refresh_index(self):
        """刷新工作区索引"""
        print("\n🔄 正在扫描工作区...")
        print("-" * 70)

        try:
            # 运行workspace_scanner.py
            scanner_path = self.workspace_root / "workspace_scanner.py"
            result = subprocess.run(
                [sys.executable, str(scanner_path)],
                capture_output=True,
                text=True,
                cwd=str(self.workspace_root)
            )

            if result.returncode == 0:
                print("✅ 扫描完成!")
                print(result.stdout)
            else:
                print("❌ 扫描失败!")
                print(result.stderr)
        except Exception as e:
            print(f"❌ 执行错误: {e}")

        print()

    def show_help(self):
        """显示帮助信息"""
        print("\n📖 命令帮助")
        print("-" * 70)
        print("""
可用命令:

  基础命令:
  • dashboard 或 dash      - 显示资产总览仪表盘
  • projects 或 proj       - 显示活跃项目
  • archived 或 arch       - 显示归档项目
  • tools                  - 显示工具脚本
  • recent [天数]          - 显示最近更新(默认7天)
  • health                 - 健康检查
  • refresh                - 刷新工作区索引

  其他:
  • help 或 ?              - 显示此帮助
  • quit 或 exit           - 退出

使用示例:
  > dashboard        # 查看总览
  > projects         # 查看活跃项目
  > recent 30        # 查看30天内的更新
  > health           # 健康检查
  > refresh          # 刷新索引
        """)
        print()

    def run_interactive(self):
        """交互式命令行"""
        print("\n" + "="*70)
        print("🎯 工作区资产盘点命令中心".center(70))
        print("="*70)
        print("\n随时掌握你的'家底' - 项目、工具、文档、代码")
        print("输入 'help' 查看可用命令\n")

        # 先显示仪表盘
        self.show_dashboard()

        while True:
            try:
                command = input("💬 请输入命令> ").strip().lower()

                if not command:
                    continue

                if command in ['quit', 'exit', 'q']:
                    print("\n👋 再见!\n")
                    break

                elif command in ['help', '?']:
                    self.show_help()

                elif command in ['dashboard', 'dash', 'd']:
                    self.show_dashboard()

                elif command in ['projects', 'proj', 'p']:
                    self.show_projects('active')

                elif command in ['archived', 'arch', 'a']:
                    self.show_projects('archived')

                elif command == 'tools':
                    self.show_tools()

                elif command.startswith('recent'):
                    parts = command.split()
                    days = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 7
                    self.show_recent_updates(days)

                elif command == 'health':
                    self.show_health_check()

                elif command == 'refresh':
                    self.refresh_index()

                else:
                    print(f"❌ 未知命令: {command}")
                    print("   输入 'help' 查看可用命令\n")

            except KeyboardInterrupt:
                print("\n\n👋 再见!\n")
                break
            except Exception as e:
                print(f"❌ 错误: {e}\n")


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='工作区资产盘点命令中心')
    parser.add_argument('--workspace', '-w', help='工作区路径')
    parser.add_argument('--dashboard', '-d', action='store_true', help='显示仪表盘')
    parser.add_argument('--projects', '-p', action='store_true', help='显示项目')
    parser.add_argument('--tools', '-t', action='store_true', help='显示工具')
    parser.add_argument('--health', action='store_true', help='健康检查')
    parser.add_argument('--refresh', '-r', action='store_true', help='刷新索引')

    args = parser.parse_args()

    center = AssetCommandCenter(args.workspace)

    # 如果有命令行参数,执行后退出
    if args.dashboard:
        center.show_dashboard()
    elif args.projects:
        center.show_projects()
    elif args.tools:
        center.show_tools()
    elif args.health:
        center.show_health_check()
    elif args.refresh:
        center.refresh_index()
    else:
        # 否则进入交互模式
        center.run_interactive()


if __name__ == '__main__':
    main()
