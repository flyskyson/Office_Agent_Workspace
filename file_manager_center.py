#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
超级文件管理中心
统一入口，集成所有文件管理功能

作者：Office Agent Workspace
创建日期：2026-01-08
版本：v1.0
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

# 设置控制台编码为UTF-8
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


class FileManagerCenter:
    """文件管理中心 - 统一入口"""

    def __init__(self, workspace_root=None):
        """初始化文件管理中心"""
        if workspace_root is None:
            workspace_root = Path(__file__).parent
        self.workspace_root = Path(workspace_root)
        self.today = datetime.now().strftime("%Y%m%d")

        # 工具映射
        self.tools = {
            'scanner': 'workspace_scanner.py',
            'cleaner': 'workspace_cleaner.py',
            'maintenance': 'workspace_maintenance.py',
            'report': 'workspace_report.py',
            'organizer': 'daily_file_organizer.py',
            'snapshot': 'create_snapshot.py',
            'version_tracker': 'code_version_tracker.py',
        }

    def print_banner(self):
        """打印横幅"""
        print("=" * 70)
        print("🏦 超级文件管理中心")
        print("=" * 70)
        print(f"📍 工作区: {self.workspace_root}")
        print(f"📅 日期: {self.today}")
        print()

    def print_menu(self):
        """打印主菜单"""
        print("📋 可用命令:")
        print()
        print("📁 文件管理")
        print("  organize      - 整理文件（智能分类归档）")
        print("  clean         - 清理缓存和临时文件")
        print("  scan          - 扫描工作区全貌")
        print()
        print("📸 快照与备份")
        print("  snapshot      - 创建完整快照")
        print("  restore       - 恢复文件（需要指定文件名）")
        print()
        print("📊 报告与监控")
        print("  report        - 生成健康报告")
        print("  status        - 查看当前状态")
        print()
        print("🔧 维护工具")
        print("  maintenance   - 运行定期维护")
        print("  check-git     - 检查Git状态")
        print()
        print("🤖 智能功能")
        print("  auto          - 智能推荐并执行")
        print("  help          - 显示帮助信息")
        print()
        print("💡 提示: 大部分命令支持 --dry-run 参数预览效果")
        print()

    def run_tool(self, tool_name, args=None):
        """运行指定工具"""
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

        print(f"🔧 运行工具: {self.tools[tool_name]}")
        print()

        try:
            result = subprocess.run(cmd, cwd=self.workspace_root)
            return result.returncode == 0
        except Exception as e:
            print(f"❌ 运行失败: {e}")
            return False

    def organize_files(self, dry_run=False):
        """整理文件"""
        print("📁 开始文件整理...")
        print()

        args = ['--dry-run'] if dry_run else []
        return self.run_tool('organizer', args)

    def clean_workspace(self, dry_run=False):
        """清理工作区"""
        print("🧹 开始清理工作区...")
        print()

        args = ['--dry-run'] if dry_run else []
        return self.run_tool('cleaner', args)

    def scan_workspace(self):
        """扫描工作区"""
        print("🔍 扫描工作区全貌...")
        print()
        return self.run_tool('scanner')

    def create_snapshot(self):
        """创建快照"""
        print("📸 创建工作区快照...")
        print()
        return self.run_tool('snapshot')

    def generate_report(self):
        """生成报告"""
        print("📊 生成健康报告...")
        print()
        return self.run_tool('report')

    def run_maintenance(self):
        """运行维护"""
        print("🔧 运行定期维护...")
        print()
        return self.run_tool('maintenance')

    def check_git_status(self):
        """检查Git状态"""
        print("🔍 检查Git状态...")
        print()

        try:
            result = subprocess.run(
                ['git', 'status', '--short'],
                cwd=self.workspace_root,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) == 1 and not lines[0]:
                    print("✅ 工作区干净，没有未提交的更改")
                else:
                    print(f"📝 未提交的更改: {len(lines)} 个文件")
                    print()
                    for line in lines[:10]:  # 只显示前10个
                        print(f"  {line}")
                    if len(lines) > 10:
                        print(f"  ... 还有 {len(lines) - 10} 个文件")
                return True
            else:
                print("⚠️  Git未初始化或不可用")
                return False
        except Exception as e:
            print(f"❌ 检查失败: {e}")
            return False

    def get_status(self):
        """获取当前状态"""
        print("📊 工作区当前状态")
        print("=" * 70)
        print()

        # 统计文件
        try:
            result = subprocess.run(
                ['git', 'ls-files'],
                cwd=self.workspace_root,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                tracked_files = len([f for f in result.stdout.split('\n') if f])
                print(f"📁 Git追踪文件: {tracked_files} 个")
        except:
            pass

        # 检查磁盘空间
        try:
            import shutil
            total, used, free = shutil.disk_usage(self.workspace_root)
            print(f"💾 磁盘空间:")
            print(f"   总容量: {total // (1024**3):.1f} GB")
            print(f"   已使用: {used // (1024**3):.1f} GB")
            print(f"   可用: {free // (1024**3):.1f} GB")
        except:
            pass

        print()

        # 检查最近报告
        report_dir = self.workspace_root / '05_Outputs' / 'Reports'
        if report_dir.exists():
            reports = sorted(report_dir.glob('*.md'), key=lambda x: x.stat().st_mtime, reverse=True)
            if reports:
                print(f"📄 最新报告: {reports[0].name}")
                print(f"   位置: {reports[0]}")

        print()

    def smart_recommend(self):
        """智能推荐操作"""
        print("🤖 智能分析工作区状态...")
        print()

        recommendations = []

        # 检查根目录文件数量
        root_files = list(self.workspace_root.glob('*'))
        root_files = [f for f in root_files if f.is_file()]

        if len(root_files) > 20:
            recommendations.append({
                'action': 'organize',
                'reason': f'根目录有 {len(root_files)} 个文件，建议整理',
                'priority': '高'
            })

        # 检查Git状态
        try:
            result = subprocess.run(
                ['git', 'status', '--short'],
                cwd=self.workspace_root,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                changed_files = len([l for l in result.stdout.split('\n') if l.strip()])
                if changed_files > 10:
                    recommendations.append({
                        'action': 'check-git',
                        'reason': f'有 {changed_files} 个文件未提交，建议检查',
                        'priority': '中'
                    })
        except:
            pass

        # 检查缓存目录
        cache_dirs = [
            self.workspace_root / '__pycache__',
            self.workspace_root / '.pytest_cache',
        ]

        for cache_dir in cache_dirs:
            if cache_dir.exists():
                recommendations.append({
                    'action': 'clean',
                    'reason': f'发现缓存目录: {cache_dir.name}',
                    'priority': '低'
                })

        # 显示推荐
        if not recommendations:
            print("✅ 工作区状态良好，暂无需要处理的任务")
        else:
            print(f"💡 发现 {len(recommendations)} 个建议操作:")
            print()

            for i, rec in enumerate(recommendations, 1):
                priority_icon = {'高': '🔴', '中': '🟡', '低': '🟢'}.get(rec['priority'], '⚪')
                print(f"{i}. {priority_icon} [{rec['priority']}] {rec['action']}")
                print(f"   原因: {rec['reason']}")
                print()

            # 询问是否执行
            print("是否执行这些操作？(y/n): ", end='')
            # 简化处理，不等待输入
            print()
            print("💡 你可以运行: python file_manager_center.py auto")

    def execute_auto(self):
        """自动执行推荐操作"""
        print("🤖 自动执行智能推荐...")
        print()

        # 简化版：只执行最必要的操作
        self.check_git_status()
        print()

        # 如果需要整理
        root_files = list(self.workspace_root.glob('*'))
        root_files = [f for f in root_files if f.is_file()]

        if len(root_files) > 20:
            print("📁 文件较多，运行整理...")
            self.organize_files(dry_run=False)
            print()

    def main(self):
        """主函数"""
        import argparse

        parser = argparse.ArgumentParser(
            description='超级文件管理中心',
            formatter_class=argparse.RawDescriptionHelpFormatter
        )

        parser.add_argument(
            'command',
            nargs='?',
            help='要执行的命令',
            choices=[
                'organize', 'clean', 'scan', 'snapshot', 'restore',
                'report', 'status', 'maintenance', 'check-git',
                'auto', 'help'
            ]
        )

        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='模拟运行，不实际执行'
        )

        args = parser.parse_args()

        # 打印横幅
        self.print_banner()

        # 如果没有命令，显示菜单
        if not args.command:
            self.print_menu()
            return

        # 执行命令
        command = args.command

        if command == 'help':
            self.print_menu()

        elif command == 'organize':
            self.organize_files(dry_run=args.dry_run)

        elif command == 'clean':
            self.clean_workspace(dry_run=args.dry_run)

        elif command == 'scan':
            self.scan_workspace()

        elif command == 'snapshot':
            self.create_snapshot()

        elif command == 'report':
            self.generate_report()

        elif command == 'status':
            self.get_status()

        elif command == 'maintenance':
            self.run_maintenance()

        elif command == 'check-git':
            self.check_git_status()

        elif command == 'auto':
            self.smart_recommend()

        else:
            print(f"❌ 未知命令: {command}")
            print("运行 'python file_manager_center.py help' 查看帮助")


def main():
    """主函数入口"""
    center = FileManagerCenter()
    center.main()


if __name__ == '__main__':
    main()
