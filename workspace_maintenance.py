"""
工作区定期维护脚本
自动化执行日常维护任务
"""

import sys
import io
from pathlib import Path
from datetime import datetime
import subprocess

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


class WorkspaceMaintenance:
    """工作区维护管理器"""

    def __init__(self, workspace_path=None):
        self.workspace_path = Path(workspace_path) if workspace_path else Path.cwd()
        self.today = datetime.now()
        self.tasks_completed = []
        self.tasks_failed = []

    def log_task(self, task_name, success, details=""):
        """记录任务执行结果"""
        if success:
            self.tasks_completed.append({'task': task_name, 'details': details})
            print(f"  ✅ {task_name}")
        else:
            self.tasks_failed.append({'task': task_name, 'details': details})
            print(f"  ❌ {task_name}: {details}")

    def clean_python_cache(self):
        """清理 Python 缓存"""
        print("\n🗑️  清理 Python 缓存...")

        try:
            # 删除 __pycache__ 目录
            pycache_count = 0
            for pycache in self.workspace_path.rglob('__pycache__'):
                if pycache.is_dir():
                    try:
                        import shutil
                        shutil.rmtree(pycache)
                        pycache_count += 1
                    except Exception:
                        pass

            # 删除 .pyc 文件
            pyc_count = 0
            for pyc_file in self.workspace_path.rglob('*.pyc'):
                if pyc_file.is_file():
                    try:
                        pyc_file.unlink()
                        pyc_count += 1
                    except Exception:
                        pass

            self.log_task(
                "清理 Python 缓存",
                True,
                f"删除了 {pycache_count} 个 __pycache__ 目录和 {pyc_count} 个 .pyc 文件"
            )
        except Exception as e:
            self.log_task("清理 Python 缓存", False, str(e))

    def check_inactive_projects(self, days_threshold=30):
        """检查不活跃的项目"""
        print(f"\n📦 检查超过 {days_threshold} 天未修改的项目...")

        try:
            from datetime import timedelta

            active_projects_path = self.workspace_path / "01_Active_Projects"
            if not active_projects_path.exists():
                self.log_task("检查不活跃项目", False, "01_Active_Projects 目录不存在")
                return

            threshold_date = self.today - timedelta(days=days_threshold)
            inactive_projects = []

            for item in active_projects_path.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    try:
                        mtime = datetime.fromtimestamp(item.stat().st_mtime)
                        if mtime < threshold_date:
                            days_inactive = (self.today - mtime).days
                            inactive_projects.append({
                                'name': item.name,
                                'days': days_inactive,
                                'last_modified': mtime.strftime('%Y-%m-%d')
                            })
                    except Exception:
                        pass

            if inactive_projects:
                projects_info = ", ".join([f"{p['name']} ({p['days']}天)" for p in inactive_projects])
                self.log_task(
                    "检查不活跃项目",
                    True,
                    f"找到 {len(inactive_projects)} 个项目: {projects_info}"
                )
            else:
                self.log_task("检查不活跃项目", True, "所有项目都是活跃的")

        except Exception as e:
            self.log_task("检查不活跃项目", False, str(e))

    def check_disk_space(self):
        """检查磁盘空间"""
        print("\n💾 检查磁盘空间...")

        try:
            import shutil
            total, used, free = shutil.disk_usage(self.workspace_path)

            def format_size(bytes_size):
                for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
                    if bytes_size < 1024.0:
                        return f"{bytes_size:.2f} {unit}"
                    bytes_size /= 1024.0
                return f"{bytes_size:.2f} PB"

            total_gb = total / (1024**3)
            used_gb = used / (1024**3)
            free_gb = free / (1024**3)
            usage_percent = (used / total) * 100

            space_info = f"总空间 {format_size(total)}, 已用 {format_size(total)} ({usage_percent:.1f}%), 剩余 {format_size(free)}"

            if usage_percent > 90:
                self.log_task("检查磁盘空间", False, f"空间不足! {space_info}")
            elif usage_percent > 80:
                self.log_task("检查磁盘空间", True, f"空间紧张. {space_info}")
            else:
                self.log_task("检查磁盘空间", True, space_info)

        except Exception as e:
            self.log_task("检查磁盘空间", False, str(e))

    def find_large_files(self, size_threshold_mb=10):
        """查找大文件"""
        print(f"\n🔍 查找大于 {size_threshold_mb} MB 的文件...")

        try:
            size_threshold_bytes = size_threshold_mb * 1024 * 1024
            large_files = []

            # 只检查主要文件夹，排除虚拟环境
            exclude_dirs = {'venv', '.venv', 'env', '.env', '__pycache__', 'node_modules'}

            for file_path in self.workspace_path.rglob('*'):
                if file_path.is_file():
                    # 跳过虚拟环境和缓存目录
                    if any(excluded in file_path.parts for excluded in exclude_dirs):
                        continue

                    try:
                        size = file_path.stat().st_size
                        if size > size_threshold_bytes:
                            large_files.append({
                                'path': file_path.relative_to(self.workspace_path),
                                'size_mb': size / (1024 * 1024)
                            })
                    except Exception:
                        pass

            if large_files:
                # 按大小排序，只显示前10个
                large_files.sort(key=lambda x: x['size_mb'], reverse=True)
                top_files = large_files[:10]

                files_info = ", ".join([f"{f['path']} ({f['size_mb']:.1f}MB)" for f in top_files])
                self.log_task(
                    "查找大文件",
                    True,
                    f"找到 {len(large_files)} 个大文件。最大的: {files_info}"
                )
            else:
                self.log_task("查找大文件", True, f"没有找到大于 {size_threshold_mb} MB 的文件")

        except Exception as e:
            self.log_task("查找大文件", False, str(e))

    def check_workspace_structure(self):
        """检查工作区结构"""
        print("\n🏗️  检查工作区结构...")

        try:
            expected_folders = [
                "00_Agent_Library",
                "01_Active_Projects",
                "02_Project_Archive",
                "03_Code_Templates",
                "04_Data_&_Resources",
                "05_Outputs"
            ]

            missing_folders = []
            for folder in expected_folders:
                folder_path = self.workspace_path / folder
                if not folder_path.exists():
                    missing_folders.append(folder)

            if missing_folders:
                self.log_task(
                    "检查工作区结构",
                    False,
                    f"缺失文件夹: {', '.join(missing_folders)}"
                )
            else:
                self.log_task("检查工作区结构", True, "所有预期文件夹都存在")

        except Exception as e:
            self.log_task("检查工作区结构", False, str(e))

    def generate_health_report(self):
        """生成健康报告"""
        print("\n📊 生成健康报告...")

        try:
            report_script = self.workspace_path / "workspace_report.py"
            if not report_script.exists():
                self.log_task("生成健康报告", False, "workspace_report.py 不存在")
                return

            result = subprocess.run(
                [sys.executable, str(report_script)],
                cwd=str(self.workspace_path),
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                self.log_task("生成健康报告", True, "报告已生成")
            else:
                self.log_task("生成健康报告", False, "生成失败")

        except Exception as e:
            self.log_task("生成健康报告", False, str(e))

    def generate_maintenance_report(self):
        """生成维护报告"""
        print("\n" + "="*60)
        print("📋 维护报告")
        print("="*60)

        print(f"\n📅 时间: {self.today.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📂 工作区: {self.workspace_path}")

        print(f"\n✅ 已完成任务 ({len(self.tasks_completed)}):")
        for task in self.tasks_completed:
            print(f"  • {task['task']}")
            if task['details']:
                print(f"    {task['details']}")

        if self.tasks_failed:
            print(f"\n❌ 失败任务 ({len(self.tasks_failed)}):")
            for task in self.tasks_failed:
                print(f"  • {task['task']}")
                if task['details']:
                    print(f"    {task['details']}")

        # 保存报告
        report_filename = f"维护报告_{self.today.strftime('%Y%m%d_%H%M%S')}.md"
        report_path = self.workspace_path / report_filename

        report_content = f"""# 工作区维护报告

**生成时间**: {self.today.strftime('%Y-%m-%d %H:%M:%S')}
**工作区路径**: `{self.workspace_path}`

---

## ✅ 已完成任务 ({len(self.tasks_completed)})

{self._format_tasks(self.tasks_completed)}

{self._format_failed_tasks()}

---

## 📊 总结

- **成功**: {len(self.tasks_completed)} 个任务
- **失败**: {len(self.tasks_failed)} 个任务
- **成功率**: {len(self.tasks_completed) / (len(self.tasks_completed) + len(self.tasks_failed)) * 100:.1f}%

---

*本报告由 workspace_maintenance.py 自动生成*
"""

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)

        print(f"\n📄 报告已保存: {report_filename}")
        print("="*60)

        return report_path

    def _format_tasks(self, tasks):
        """格式化任务列表"""
        lines = []
        for task in tasks:
            lines.append(f"- **{task['task']}**")
            if task['details']:
                lines.append(f"  - {task['details']}")
        return "\n".join(lines) if lines else "*无任务*"

    def _format_failed_tasks(self):
        """格式化失败任务列表"""
        if not self.tasks_failed:
            return "## ❌ 失败任务 (0)\n\n✅ 所有任务都成功完成！"

        lines = [f"## ❌ 失败任务 ({len(self.tasks_failed)})\n"]
        lines.append(self._format_tasks(self.tasks_failed))
        return "\n".join(lines)

    def run_maintenance(self, generate_health_report=False):
        """执行完整维护流程"""
        print("\n" + "="*60)
        print("🔧 工作区定期维护")
        print("="*60)

        print(f"\n📅 时间: {self.today.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📂 工作区: {self.workspace_path}")

        # 执行维护任务
        self.clean_python_cache()
        self.check_inactive_projects(days_threshold=30)
        self.check_disk_space()
        self.find_large_files(size_threshold_mb=10)
        self.check_workspace_structure()

        if generate_health_report:
            self.generate_health_report()

        # 生成报告
        return self.generate_maintenance_report()


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='工作区定期维护')
    parser.add_argument(
        '--health-report',
        action='store_true',
        help='同时生成详细健康报告'
    )

    args = parser.parse_args()

    # 创建维护器
    maintenance = WorkspaceMaintenance()

    try:
        # 运行维护
        report_path = maintenance.run_maintenance(
            generate_health_report=args.health_report
        )
        print(f"\n✅ 维护完成！")
        return 0
    except Exception as e:
        print(f"\n❌ 维护过程出错: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
