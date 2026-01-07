"""
工作区健康报告工具
用于分析 Office_Agent_Workspace 的结构和状态
"""

import sys
import io
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
import os

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


class WorkspaceHealthChecker:
    """工作区健康检查器"""

    def __init__(self, workspace_path=None):
        self.workspace_path = Path(workspace_path) if workspace_path else Path.cwd()
        self.today = datetime.now()

        # 预设的主要文件夹结构
        self.main_folders = [
            "00_Agent_Library",
            "01_Active_Projects",
            "02_Project_Archive",
            "03_Code_Templates",
            "04_Data_&_Resources",
            "05_Outputs",
        ]

        # 统计数据
        self.folder_stats = {}
        self.venv_dirs = []
        self.pycache_dirs = []
        self.temp_files = []
        self.archive_candidates = []

    def get_folder_size(self, path):
        """递归计算文件夹大小（字节）"""
        total_size = 0
        try:
            for item in path.rglob('*'):
                if item.is_file():
                    try:
                        total_size += item.stat().st_size
                    except (OSError, PermissionError):
                        pass
        except (OSError, PermissionError):
            pass
        return total_size

    def format_size(self, size_bytes):
        """格式化文件大小显示"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"

    def count_projects(self, folder_path):
        """统计文件夹中的项目数量"""
        if not folder_path.exists():
            return 0

        # 统计直接子文件夹（排除隐藏文件夹）
        count = 0
        for item in folder_path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                count += 1
        return count

    def analyze_main_folders(self):
        """分析主要文件夹的结构和大小"""
        print("\n📊 正在分析主要文件夹...")

        for folder_name in self.main_folders:
            folder_path = self.workspace_path / folder_name

            if folder_path.exists() and folder_path.is_dir():
                size = self.get_folder_size(folder_path)
                project_count = self.count_projects(folder_path)

                self.folder_stats[folder_name] = {
                    'path': folder_path,
                    'size': size,
                    'size_formatted': self.format_size(size),
                    'project_count': project_count,
                    'exists': True
                }
            else:
                self.folder_stats[folder_name] = {
                    'path': folder_path,
                    'size': 0,
                    'size_formatted': 'N/A',
                    'project_count': 0,
                    'exists': False
                }

    def find_venv_directories(self):
        """找出所有虚拟环境 venv 文件夹"""
        print("🔍 正在扫描虚拟环境...")

        for venv_dir in self.workspace_path.rglob('venv'):
            if venv_dir.is_dir():
                size = self.get_folder_size(venv_dir)
                self.venv_dirs.append({
                    'path': venv_dir,
                    'relative_path': venv_dir.relative_to(self.workspace_path),
                    'size': size,
                    'size_formatted': self.format_size(size)
                })

        # 查找 .venv, env, .env 等常见命名
        for pattern in ['.venv', 'env', '.env', 'virtualenv']:
            for venv_dir in self.workspace_path.rglob(pattern):
                if venv_dir.is_dir():
                    # 避免重复添加
                    rel_path = str(venv_dir.relative_to(self.workspace_path))
                    if not any(d['relative_path'] == rel_path for d in self.venv_dirs):
                        size = self.get_folder_size(venv_dir)
                        self.venv_dirs.append({
                            'path': venv_dir,
                            'relative_path': venv_dir.relative_to(self.workspace_path),
                            'size': size,
                            'size_formatted': self.format_size(size)
                        })

    def find_cache_and_temp_files(self):
        """识别缓存目录和临时文件"""
        print("🗑️  正在扫描缓存和临时文件...")

        # 查找所有 __pycache__ 目录
        for pycache in self.workspace_path.rglob('__pycache__'):
            if pycache.is_dir():
                self.pycache_dirs.append({
                    'path': pycache,
                    'relative_path': pycache.relative_to(self.workspace_path)
                })

        # 查找常见临时文件
        temp_patterns = ['*.log', 'temp_*', '*.tmp', '*.cache', '*.pyc']

        for pattern in temp_patterns:
            for temp_file in self.workspace_path.rglob(pattern):
                if temp_file.is_file():
                    self.temp_files.append({
                        'path': temp_file,
                        'relative_path': temp_file.relative_to(self.workspace_path),
                        'size': temp_file.stat().st_size,
                        'size_formatted': self.format_size(temp_file.stat().st_size)
                    })

    def check_archive_candidates(self):
        """检查 01_Active_Projects/ 下的项目，找出待归档的项目"""
        print("📦 正在检查待归档项目...")

        active_projects_path = self.workspace_path / "01_Active_Projects"

        if not active_projects_path.exists():
            return

        threshold_date = self.today - timedelta(days=30)

        for item in active_projects_path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                # 获取最后修改时间
                try:
                    mtime = datetime.fromtimestamp(item.stat().st_mtime)

                    if mtime < threshold_date:
                        days_inactive = (self.today - mtime).days
                        self.archive_candidates.append({
                            'name': item.name,
                            'path': item,
                            'last_modified': mtime.strftime('%Y-%m-%d %H:%M:%S'),
                            'days_inactive': days_inactive
                        })
                except (OSError, PermissionError):
                    pass

    def generate_report(self):
        """生成完整的健康报告"""
        print("\n" + "="*60)
        print("🏥 工作区健康报告")
        print("="*60)
        print(f"📅 生成时间: {self.today.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📂 工作区路径: {self.workspace_path}")
        print("="*60)

        # 执行所有检查
        self.analyze_main_folders()
        self.find_venv_directories()
        self.find_cache_and_temp_files()
        self.check_archive_candidates()

        # 生成 Markdown 报告内容
        report_lines = []

        # 报告头部
        report_lines.append("# 工作区健康报告\n")
        report_lines.append(f"**生成时间**: {self.today.strftime('%Y-%m-%d %H:%M:%S')}\n")
        report_lines.append(f"**工作区路径**: `{self.workspace_path}`\n")
        report_lines.append("---\n")

        # 1. 主要文件夹统计
        report_lines.append("## 📊 主要文件夹统计\n")
        report_lines.append("| 文件夹 | 状态 | 大小 | 项目数 |")
        report_lines.append("|--------|------|------|--------|")

        total_workspace_size = 0
        for folder_name in self.main_folders:
            stats = self.folder_stats.get(folder_name, {})
            status = "✅ 存在" if stats.get('exists', False) else "❌ 缺失"
            size = stats.get('size_formatted', 'N/A')
            count = stats.get('project_count', 0)
            report_lines.append(f"| {folder_name} | {status} | {size} | {count} |")
            total_workspace_size += stats.get('size', 0)

        report_lines.append(f"\n**总大小**: {self.format_size(total_workspace_size)}\n")

        # 2. 虚拟环境目录
        report_lines.append("## 🐍 虚拟环境目录\n")

        if self.venv_dirs:
            total_venv_size = sum(d['size'] for d in self.venv_dirs)
            report_lines.append(f"**找到 {len(self.venv_dirs)} 个虚拟环境，总大小**: {self.format_size(total_venv_size)}\n\n")
            report_lines.append("| 路径 | 大小 |")
            report_lines.append("|------|------|")

            for venv in sorted(self.venv_dirs, key=lambda x: x['size'], reverse=True):
                report_lines.append(f"| `{venv['relative_path']}` | {venv['size_formatted']} |")
        else:
            report_lines.append("✅ 未找到虚拟环境目录\n")

        # 3. 缓存和临时文件
        report_lines.append("\n## 🗑️  缓存和临时文件\n")

        # __pycache__ 目录
        if self.pycache_dirs:
            report_lines.append(f"### Python 缓存目录\n")
            report_lines.append(f"**找到 {len(self.pycache_dirs)} 个 `__pycache__` 目录**\n\n")

            # 显示前10个
            for pycache in sorted(self.pycache_dirs, key=lambda x: str(x['relative_path']))[:10]:
                report_lines.append(f"- `{pycache['relative_path']}`")

            if len(self.pycache_dirs) > 10:
                report_lines.append(f"\n*... 还有 {len(self.pycache_dirs) - 10} 个*")
            report_lines.append("")

        # 临时文件
        if self.temp_files:
            total_temp_size = sum(f['size'] for f in self.temp_files)
            report_lines.append(f"### 临时文件\n")
            report_lines.append(f"**找到 {len(self.temp_files)} 个临时文件，总大小**: {self.format_size(total_temp_size)}\n\n")

            # 按类型分组
            temp_by_type = defaultdict(list)
            for temp_file in self.temp_files:
                ext = temp_file['path'].suffix or 'no_extension'
                temp_by_type[ext].append(temp_file)

            report_lines.append("| 文件类型 | 数量 | 总大小 |")
            report_lines.append("|----------|------|--------|")

            for ext, files in sorted(temp_by_type.items(), key=lambda x: sum(f['size'] for f in x[1]), reverse=True):
                count = len(files)
                size = self.format_size(sum(f['size'] for f in files))
                report_lines.append(f"| {ext or '(无扩展名)'} | {count} | {size} |")
        else:
            report_lines.append("✅ 未找到临时文件\n")

        # 4. 待归档项目
        report_lines.append("\n## 📦 待归档项目\n")

        if self.archive_candidates:
            report_lines.append(f"**找到 {len(self.archive_candidates)} 个超过30天未修改的项目**\n\n")
            report_lines.append("| 项目名称 | 最后修改时间 | 未活跃天数 |")
            report_lines.append("|----------|--------------|-----------|")

            for project in sorted(self.archive_candidates, key=lambda x: x['days_inactive'], reverse=True):
                report_lines.append(
                    f"| {project['name']} | {project['last_modified']} | {project['days_inactive']} 天 |"
                )

            report_lines.append("\n💡 **建议**: 将这些项目移动到 `02_Project_Archive/` 目录")
        else:
            report_lines.append("✅ 所有活跃项目都在最近30天内有更新\n")

        # 报告尾部
        report_lines.append("\n---\n")
        report_lines.append("*本报告由 workspace_report.py 自动生成*")

        # 保存到文件
        report_content = "\n".join(report_lines)
        report_filename = f"工作区健康报告_{self.today.strftime('%Y%m%d_%H%M%S')}.md"
        report_path = self.workspace_path / report_filename

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)

        # 输出摘要到控制台
        self.print_summary()

        print(f"\n✅ 完整报告已保存到: {report_filename}")
        print(f"📄 文件路径: {report_path}")

        return report_path

    def print_summary(self):
        """在控制台输出摘要信息"""
        print("\n" + "="*60)
        print("📋 报告摘要")
        print("="*60)

        # 文件夹统计摘要
        print("\n📁 主要文件夹:")
        for folder_name in self.main_folders:
            stats = self.folder_stats.get(folder_name, {})
            if stats.get('exists', False):
                print(f"  • {folder_name}: {stats['size_formatted']}, {stats['project_count']} 个项目")
            else:
                print(f"  • {folder_name}: ❌ 不存在")

        # 虚拟环境摘要
        if self.venv_dirs:
            total_venv_size = sum(d['size'] for d in self.venv_dirs)
            print(f"\n🐍 虚拟环境: 找到 {len(self.venv_dirs)} 个，总大小 {self.format_size(total_venv_size)}")
        else:
            print("\n🐍 虚拟环境: 未找到")

        # 缓存和临时文件摘要
        if self.pycache_dirs:
            print(f"\n🗑️  __pycache__: {len(self.pycache_dirs)} 个目录")
        else:
            print(f"\n🗑️  __pycache__: 未找到")

        if self.temp_files:
            total_temp_size = sum(f['size'] for f in self.temp_files)
            print(f"   临时文件: {len(self.temp_files)} 个，总大小 {self.format_size(total_temp_size)}")
        else:
            print(f"   临时文件: 未找到")

        # 待归档项目摘要
        if self.archive_candidates:
            print(f"\n📦 待归档项目: {len(self.archive_candidates)} 个（超过30天未修改）")
            for project in self.archive_candidates[:5]:
                print(f"   • {project['name']} - {project['days_inactive']} 天未活跃")
            if len(self.archive_candidates) > 5:
                print(f"   *... 还有 {len(self.archive_candidates) - 5} 个*")
        else:
            print("\n📦 待归档项目: 无")

        print("="*60)


def main():
    """主函数"""
    print("🏥 工作区健康检查工具")
    print("="*60)

    # 创建检查器实例
    checker = WorkspaceHealthChecker()

    # 生成报告
    try:
        report_path = checker.generate_report()
        print(f"\n✅ 报告生成完成！")
        return 0
    except Exception as e:
        print(f"\n❌ 生成报告时出错: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
