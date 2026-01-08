#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
今日启动器 - 每天打开工作区的第一站

这是你的"晨间助手"，帮助你：
1. 快速了解工作区状态
2. 回顾昨天的工作
3. 确定今天的任务
4. 直接开始工作

作者: 工作区智能管家
版本: v1.0
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
import sys

# Windows UTF-8 修复
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


class DailyLauncher:
    """今日启动器 - 你的晨间工作区助手"""

    def __init__(self, workspace_root=None):
        """初始化启动器

        Args:
            workspace_root: 工作区根目录
        """
        if workspace_root is None:
            workspace_root = Path(__file__).parent
        else:
            workspace_root = Path(workspace_root)

        self.workspace_root = workspace_root
        self.memory_dir = workspace_root / "06_Learning_Journal" / "workspace_memory"

        # 颜色代码（Windows终端兼容）
        self.colors = {
            'header': '\033[96m',    # 青色
            'success': '\033[92m',   # 绿色
            'warning': '\033[93m',   # 黄色
            'error': '\033[91m',     # 红色
            'info': '\033[94m',      # 蓝色
            'reset': '\033[0m',      # 重置
            'bold': '\033[1m'        # 粗体
        }

    def color_print(self, text, color='reset'):
        """带颜色的打印"""
        if sys.platform == 'win32':
            # Windows可能不支持ANSI颜色，直接打印
            print(text)
        else:
            color_code = self.colors.get(color, self.colors['reset'])
            print(f"{color_code}{text}{self.colors['reset']}")

    def print_header(self, title):
        """打印标题"""
        print("\n" + "=" * 70)
        self.color_print(f"  {title}", 'header')
        print("=" * 70 + "\n")

    def load_workspace_index(self):
        """加载工作区索引

        Returns:
            dict: 工作区索引数据，如果不存在返回None
        """
        index_file = self.memory_dir / "workspace_index_latest.json"

        if not index_file.exists():
            return None

        try:
            with open(index_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.color_print(f"⚠️  无法加载工作区索引: {e}", 'warning')
            return None

    def get_recent_files(self, hours=24, limit=10):
        """获取最近修改的文件

        Args:
            hours: 查找最近多少小时内修改的文件
            limit: 最多返回多少个文件

        Returns:
            list: 最近修改的文件列表
        """
        try:
            index_data = self.load_workspace_index()
            if not index_data:
                return []

            # 收集所有最近修改的文件
            recent_files = []

            # 从项目中收集
            for project in index_data.get('projects', []):
                project_name = project.get('name', 'Unknown')
                project_status = project.get('status', 'unknown')

                for script in project.get('main_scripts', []):
                    try:
                        modified_time = datetime.strptime(
                            script.get('modified', ''),
                            '%Y-%m-%d %H:%M:%S'
                        )

                        # 检查是否在指定时间内
                        time_diff = datetime.now() - modified_time
                        if time_diff.total_seconds() <= hours * 3600:
                            recent_files.append({
                                'name': script.get('name', 'Unknown'),
                                'path': script.get('path', ''),
                                'project': project_name,
                                'project_status': project_status,
                                'modified': modified_time,
                                'size': script.get('size', 0)
                            })
                    except:
                        continue

            # 从工具中收集
            for tool in index_data.get('tools', []):
                try:
                    modified_time = datetime.strptime(
                        tool.get('modified', ''),
                        '%Y-%m-%d %H:%M:%S'
                    )

                    time_diff = datetime.now() - modified_time
                    if time_diff.total_seconds() <= hours * 3600:
                        recent_files.append({
                            'name': tool.get('name', 'Unknown'),
                            'path': tool.get('path', ''),
                            'project': '工作区工具',
                            'project_status': 'tool',
                            'modified': modified_time,
                            'size': tool.get('size', 0)
                        })
                except:
                    continue

            # 按修改时间排序（最新的在前）
            recent_files.sort(key=lambda x: x['modified'], reverse=True)

            return recent_files[:limit]

        except Exception as e:
            self.color_print(f"⚠️  获取最近文件时出错: {e}", 'warning')
            return []

    def check_workspace_health(self):
        """检查工作区健康状况

        Returns:
            dict: 健康状态信息
        """
        health_status = {
            'status': 'unknown',
            'issues': [],
            'warnings': [],
            'info': []
        }

        index_data = self.load_workspace_index()

        if not index_data:
            health_status['status'] = 'error'
            health_status['issues'].append("无法找到工作区索引，请运行 workspace_scanner.py")
            return health_status

        # 检查索引新鲜度
        try:
            scan_time = datetime.strptime(
                index_data.get('scan_time', ''),
                '%Y-%m-%d %H:%M:%S'
            )
            age_hours = (datetime.now() - scan_time).total_seconds() / 3600

            if age_hours > 24:
                health_status['warnings'].append(
                    f"工作区索引已过期 {age_hours:.1f} 小时，建议重新扫描"
                )
            else:
                health_status['info'].append(
                    f"工作区索引较新 ({age_hours:.1f} 小时前更新)"
                )
        except:
            pass

        # 检查项目状态
        active_projects = [p for p in index_data.get('projects', []) if p.get('status') == 'active']
        for project in active_projects:
            if not project.get('has_readme'):
                health_status['warnings'].append(
                    f"项目 {project.get('name')} 缺少README文档"
                )

        # 检查Git状态
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.workspace_root,
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                changed_files = [line for line in result.stdout.strip().split('\n') if line]
                if changed_files:
                    health_status['info'].append(
                        f"有 {len(changed_files)} 个文件未提交到Git"
                    )
        except:
            pass

        # 确定总体状态
        if health_status['issues']:
            health_status['status'] = 'error'
        elif health_status['warnings']:
            health_status['status'] = 'warning'
        else:
            health_status['status'] = 'good'

        return health_status

    def generate_daily_recommendations(self):
        """生成今日任务推荐

        Returns:
            list: 推荐任务列表
        """
        recommendations = []

        index_data = self.load_workspace_index()
        if not index_data:
            return []

        # 获取最近修改的文件
        recent_files = self.get_recent_files(hours=48, limit=5)

        if recent_files:
            latest_file = recent_files[0]
            project = latest_file.get('project', 'Unknown')

            recommendations.append({
                'type': 'continue',
                'priority': 'high',
                'title': f'继续昨天的工作: {project}',
                'description': f"你最后修改了 {latest_file.get('name')}",
                'action': f'打开项目文件夹',
                'path': f"{self.workspace_root / '01_Active_Projects' / project}"
            })

        # 检查缺少README的项目
        active_projects = [p for p in index_data.get('projects', []) if p.get('status') == 'active']
        projects_without_readme = [
            p for p in active_projects
            if not p.get('has_readme')
        ]

        if projects_without_readme:
            project = projects_without_readme[0]
            recommendations.append({
                'type': 'documentation',
                'priority': 'medium',
                'title': f'为项目添加README: {project.get("name")}',
                'description': '好的文档让项目更专业',
                'action': '创建README.md',
                'path': f"{self.workspace_root / project.get('path')}"
            })

        # 推荐整理工作区
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.workspace_root,
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0 and result.stdout.strip():
                recommendations.append({
                    'type': 'maintenance',
                    'priority': 'low',
                    'title': '提交代码变更',
                    'description': '有文件未提交到Git',
                    'action': '运行 git add & git commit',
                    'path': str(self.workspace_root)
                })
        except:
            pass

        return recommendations

    def display_welcome_message(self):
        """显示欢迎信息"""
        now = datetime.now()
        hour = now.hour

        if hour < 12:
            greeting = "早安"
        elif hour < 18:
            greeting = "午安"
        else:
            greeting = "晚上好"

        self.print_header(f"{greeting}！☀️  工作区今日启动器")
        self.color_print(f"  当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")
        self.color_print(f"  工作区: {self.workspace_root.name}\n")

    def display_health_status(self):
        """显示工作区健康状态"""
        print("📊 工作区健康检查")
        print("-" * 70)

        health = self.check_workspace_health()

        # 总体状态
        status_icons = {
            'good': '✅',
            'warning': '⚠️ ',
            'error': '❌',
            'unknown': '❓'
        }

        icon = status_icons.get(health['status'], '❓')
        status_text = {
            'good': '良好',
            'warning': '需要注意',
            'error': '存在问题',
            'unknown': '未知'
        }.get(health['status'], '未知')

        self.color_print(f"  总体状态: {icon} {status_text}\n")

        # 显示问题
        if health['issues']:
            self.color_print("  🔴 问题:", 'error')
            for issue in health['issues']:
                print(f"     • {issue}")
            print()

        if health['warnings']:
            self.color_print("  🟡 警告:", 'warning')
            for warning in health['warnings']:
                print(f"     • {warning}")
            print()

        if health['info']:
            self.color_print("  🔵 信息:", 'info')
            for info in health['info']:
                print(f"     • {info}")
            print()

    def display_recent_activity(self):
        """显示最近活动"""
        print("\n📝 最近24小时活动")
        print("-" * 70)

        recent_files = self.get_recent_files(hours=24, limit=8)

        if not recent_files:
            print("  最近24小时没有修改任何文件")
            print("  💡 这是新的一天，开始创建吧！")
            return

        for i, file_info in enumerate(recent_files[:8], 1):
            # 时间差显示
            time_diff = datetime.now() - file_info['modified']
            if time_diff.total_seconds() < 3600:
                time_str = f"{int(time_diff.total_seconds() / 60)} 分钟前"
            elif time_diff.total_seconds() < 86400:
                time_str = f"{int(time_diff.total_seconds() / 3600)} 小时前"
            else:
                time_str = "昨天"

            # 文件大小
            size = file_info['size']
            if size < 1024:
                size_str = f"{size} B"
            elif size < 1024 * 1024:
                size_str = f"{size // 1024} KB"
            else:
                size_str = f"{size // (1024 * 1024)} MB"

            # 项目状态图标
            if file_info['project_status'] == 'active':
                status_icon = '🚀'
            elif file_info['project_status'] == 'archived':
                status_icon = '📦'
            else:
                status_icon = '🛠️ '

            print(f"  {i}. {status_icon} [{file_info['project']}] {file_info['name']}")
            print(f"     📁 {file_info['path']}")
            print(f"     ⏰ {time_str}  |  📊 {size_str}")
            print()

    def display_recommendations(self):
        """显示今日推荐任务"""
        print("\n🎯 今日推荐任务")
        print("-" * 70)

        recommendations = self.generate_daily_recommendations()

        if not recommendations:
            print("  没有特别的推荐任务")
            print("  💡 你可以自由选择今天要做什么！")
            return

        for i, rec in enumerate(recommendations, 1):
            priority_icon = {
                'high': '🔴',
                'medium': '🟡',
                'low': '🟢'
            }.get(rec['priority'], '⚪')

            print(f"\n  {i}. {priority_icon} {rec['title']}")
            print(f"     📝 {rec['description']}")
            print(f"     ⚡ {rec['action']}")

    def display_quick_actions(self):
        """显示快速操作菜单"""
        print("\n\n⚡ 快速操作")
        print("-" * 70)
        print("\n  你想现在做什么？")
        print()
        print("  1. 🔄 刷新工作区索引（运行 workspace_scanner.py）")
        print("  2. 📊 生成详细工作区报告（运行 workspace_report.py）")
        print("  3. 🧹 清理工作区缓存（运行 workspace_cleaner.py）")
        print("  4. 📝 打开学习日志记录")
        print("  5. 🔍 查看所有活跃项目")
        print("  6. 💻 打开VSCode到工作区")
        print("  0. 🚪 退出")
        print()

    def run_quick_action(self, choice):
        """执行快速操作

        Args:
            choice: 用户选择

        Returns:
            bool: 是否应该退出程序
        """
        if choice == '1':
            print("\n正在刷新工作区索引...")
            try:
                scanner_path = self.workspace_root / 'workspace_scanner.py'
                subprocess.run([sys.executable, str(scanner_path)], check=True)
                self.color_print("\n✅ 索引刷新完成！", 'success')
            except Exception as e:
                self.color_print(f"\n❌ 刷新失败: {e}", 'error')
            input("\n按回车键继续...")
            return False

        elif choice == '2':
            print("\n正在生成工作区报告...")
            try:
                report_path = self.workspace_root / 'workspace_report.py'
                subprocess.run([sys.executable, str(report_path)], check=True)
                self.color_print("\n✅ 报告生成完成！", 'success')
            except Exception as e:
                self.color_print(f"\n❌ 生成失败: {e}", 'error')
            input("\n按回车键继续...")
            return False

        elif choice == '3':
            print("\n正在清理工作区...")
            try:
                cleaner_path = self.workspace_root / 'workspace_cleaner.py'
                subprocess.run([sys.executable, str(cleaner_path)], check=True)
                self.color_print("\n✅ 清理完成！", 'success')
            except Exception as e:
                self.color_print(f"\n❌ 清理失败: {e}", 'error')
            input("\n按回车键继续...")
            return False

        elif choice == '4':
            print("\n正在打开学习日志记录工具...")
            try:
                logger_path = self.workspace_root / '06_Learning_Journal' / 'learning_logger.py'
                if logger_path.exists():
                    subprocess.run([sys.executable, str(logger_path)], check=True)
                else:
                    self.color_print("⚠️  learning_logger.py 不存在", 'warning')
            except Exception as e:
                self.color_print(f"\n❌ 启动失败: {e}", 'error')
            input("\n按回车键继续...")
            return False

        elif choice == '5':
            self.display_all_projects()
            input("\n按回车键继续...")
            return False

        elif choice == '6':
            print("\n正在打开VSCode...")
            try:
                subprocess.run(['code', str(self.workspace_root)], check=True)
                self.color_print("\n✅ VSCode已打开！", 'success')
            except Exception as e:
                self.color_print(f"\n❌ 打开VSCode失败: {e}", 'error')
                print("💡 请确保已安装VSCode并在PATH中")
            input("\n按回车键继续...")
            return False

        elif choice == '0':
            return True

        else:
            print("\n⚠️  无效选项，请重试")
            input("\n按回车键继续...")
            return False

    def display_all_projects(self):
        """显示所有活跃项目"""
        print("\n🚀 所有活跃项目")
        print("-" * 70)

        index_data = self.load_workspace_index()
        if not index_data:
            print("  无法加载项目信息")
            return

        active_projects = [p for p in index_data.get('projects', []) if p.get('status') == 'active']

        if not active_projects:
            print("  没有活跃项目")
            return

        for i, project in enumerate(active_projects, 1):
            print(f"\n  {i}. {project.get('name')}")
            print(f"     📁 路径: {project.get('path')}")
            print(f"     📄 Python文件: {project.get('py_files_count', 0)} 个")
            print(f"     📝 README: {'✅' if project.get('has_readme') else '❌'}")
            print(f"     ⏰ 最后修改: {project.get('last_modified', 'Unknown')}")

    def run(self):
        """运行今日启动器主循环"""
        while True:
            # 清屏
            os.system('cls' if os.name == 'nt' else 'clear')

            # 显示欢迎信息
            self.display_welcome_message()

            # 显示健康状态
            self.display_health_status()

            # 显示最近活动
            self.display_recent_activity()

            # 显示推荐任务
            self.display_recommendations()

            # 显示快速操作
            self.display_quick_actions()

            # 获取用户输入
            choice = input("  请输入选项 (0-6): ").strip()

            # 执行操作
            should_exit = self.run_quick_action(choice)

            if should_exit:
                print("\n👋 祝你今天工作愉快！")
                break


def main():
    """主函数"""
    launcher = DailyLauncher()
    try:
        launcher.run()
    except KeyboardInterrupt:
        print("\n\n👋 已取消。祝你今天工作愉快！")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        input("\n按回车键退出...")


if __name__ == '__main__':
    main()
