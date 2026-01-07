"""
工作区清理工具
安全清理和整理 Office_Agent_Workspace
"""

import sys
import io
from pathlib import Path
from datetime import datetime, timedelta
import shutil
import re

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


class WorkspaceCleaner:
    """工作区清理器"""

    def __init__(self, workspace_path=None, dry_run=True):
        self.workspace_path = Path(workspace_path) if workspace_path else Path.cwd()
        self.dry_run = dry_run  # 默认为演习模式，不实际删除
        self.today = datetime.now()

        # 统计数据
        self.pycache_removed = 0
        self.pyc_removed = 0
        self.space_freed = 0
        self.files_moved = []
        self.old_reports_archived = 0
        self.old_reports_deleted = 0

        # 目标目录结构
        self.scripts_dir = self.workspace_path / "00_Agent_Library" / "99_Scripts_Tools"
        self.docs_dir = self.workspace_path / "00_Agent_Library" / "01_Documentation"
        self.archive_dir = self.workspace_path / "06_Learning_Journal" / "workspace_memory" / "old_reports"

        # 旧报告保留天数（默认30天）
        self.report_retention_days = 30

    def get_size(self, path):
        """获取文件或目录大小"""
        if path.is_file():
            return path.stat().st_size
        elif path.is_dir():
            total = 0
            try:
                for item in path.rglob('*'):
                    if item.is_file():
                        total += item.stat().st_size
            except (OSError, PermissionError):
                pass
            return total
        return 0

    def format_size(self, size_bytes):
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"

    def clean_pycache(self):
        """清理所有 __pycache__ 目录"""
        print("\n" + "="*60)
        print("🗑️  清理 Python 缓存")
        print("="*60)

        pycache_dirs = list(self.workspace_path.rglob('__pycache__'))
        total_size = 0

        print(f"\n找到 {len(pycache_dirs)} 个 __pycache__ 目录")

        if not pycache_dirs:
            print("✅ 没有需要清理的缓存")
            return

        # 计算总大小
        for pycache in pycache_dirs:
            if pycache.is_dir():
                size = self.get_size(pycache)
                total_size += size

        print(f"预计释放空间: {self.format_size(total_size)}")

        if self.dry_run:
            print("\n🔍 [演习模式] 将删除以下目录:")
            for pycache in pycache_dirs[:10]:
                rel_path = pycache.relative_to(self.workspace_path)
                print(f"  • {rel_path}")
            if len(pycache_dirs) > 10:
                print(f"  *... 还有 {len(pycache_dirs) - 10} 个*")
        else:
            # 实际删除
            print("\n⚠️  正在删除...")
            for pycache in pycache_dirs:
                try:
                    if pycache.is_dir():
                        size = self.get_size(pycache)
                        shutil.rmtree(pycache)
                        self.pycache_removed += 1
                        self.space_freed += size
                except (OSError, PermissionError) as e:
                    print(f"  ⚠️  无法删除 {pycache}: {e}")

            print(f"✅ 已删除 {self.pycache_removed} 个目录")

    def clean_pyc_files(self):
        """清理所有 .pyc 文件"""
        print("\n" + "="*60)
        print("🗑️  清理 .pyc 文件")
        print("="*60)

        pyc_files = list(self.workspace_path.rglob('*.pyc'))
        total_size = sum(f.stat().st_size for f in pyc_files if f.is_file())

        print(f"\n找到 {len(pyc_files)} 个 .pyc 文件")
        print(f"预计释放空间: {self.format_size(total_size)}")

        if self.dry_run:
            print("\n🔍 [演习模式] 将删除这些文件")
            if len(pyc_files) > 0:
                print(f"  示例: {pyc_files[0].relative_to(self.workspace_path)}")
                if len(pyc_files) > 1:
                    print(f"  示例: {pyc_files[1].relative_to(self.workspace_path)}")
                print(f"  *... 还有 {len(pyc_files) - 2} 个*")
        else:
            # 实际删除
            print("\n⚠️  正在删除...")
            for pyc_file in pyc_files:
                try:
                    if pyc_file.is_file():
                        size = pyc_file.stat().st_size
                        pyc_file.unlink()
                        self.pyc_removed += 1
                        self.space_freed += size
                except (OSError, PermissionError) as e:
                    print(f"  ⚠️  无法删除 {pyc_file}: {e}")

            print(f"✅ 已删除 {self.pyc_removed} 个文件")

    def organize_root_scripts(self):
        """整理根目录的脚本文件"""
        print("\n" + "="*60)
        print("📁 整理根目录脚本")
        print("="*60)

        # 需要移动的脚本文件
        scripts_to_move = [
            'add_poppler_path.ps1',
            'add_tesseract_path.ps1',
            'check-deepseek.ps1',
            'fix-deepseek.ps1',
            'init-vscode.ps1',
            'start-vscode-with-deepseek.bat',
            'switch-model.bat',
            'switch-model.ps1',
        ]

        # 检查哪些文件存在
        existing_scripts = []
        for script in scripts_to_move:
            script_path = self.workspace_path / script
            if script_path.exists():
                existing_scripts.append(script_path)

        if not existing_scripts:
            print("\n✅ 根目录没有需要整理的脚本")
            return

        print(f"\n找到 {len(existing_scripts)} 个脚本文件")

        # 创建目标目录
        if not self.scripts_dir.exists():
            if self.dry_run:
                print(f"🔍 [演习模式] 将创建目录: {self.scripts_dir.relative_to(self.workspace_path)}")
            else:
                self.scripts_dir.mkdir(parents=True, exist_ok=True)
                print(f"✅ 已创建目录: {self.scripts_dir.relative_to(self.workspace_path)}")

        # 移动文件
        print(f"\n目标目录: {self.scripts_dir.relative_to(self.workspace_path)}")
        print("\n将移动以下文件:")

        for script_path in existing_scripts:
            target_path = self.scripts_dir / script_path.name
            rel_path = script_path.relative_to(self.workspace_path)

            if self.dry_run:
                print(f"  🔍 {rel_path} -> {self.scripts_dir.relative_to(self.workspace_path)}/")
            else:
                try:
                    shutil.move(str(script_path), str(target_path))
                    self.files_moved.append({
                        'from': str(script_path),
                        'to': str(target_path)
                    })
                    print(f"  ✅ {script_path.name} 已移动")
                except Exception as e:
                    print(f"  ⚠️  移动失败 {script_path.name}: {e}")

    def organize_root_docs(self):
        """整理根目录的文档文件"""
        print("\n" + "="*60)
        print("📁 整理根目录文档")
        print("="*60)

        # 需要移动的文档文件
        docs_to_move = [
            'copilot-ai-models-guide.md',
            'copilot-usage-guide.md',
            'README_DeepSeek接入.md',
            'README_VSCode重启问题解决.md',
            'README_模型切换.md',
        ]

        # 检查哪些文件存在
        existing_docs = []
        for doc in docs_to_move:
            doc_path = self.workspace_path / doc
            if doc_path.exists():
                existing_docs.append(doc_path)

        if not existing_docs:
            print("\n✅ 根目录没有需要整理的文档")
            return

        print(f"\n找到 {len(existing_docs)} 个文档文件")

        # 创建目标目录
        if not self.docs_dir.exists():
            if self.dry_run:
                print(f"🔍 [演习模式] 将创建目录: {self.docs_dir.relative_to(self.workspace_path)}")
            else:
                self.docs_dir.mkdir(parents=True, exist_ok=True)
                print(f"✅ 已创建目录: {self.docs_dir.relative_to(self.workspace_path)}")

        # 移动文件
        print(f"\n目标目录: {self.docs_dir.relative_to(self.workspace_path)}")
        print("\n将移动以下文件:")

        for doc_path in existing_docs:
            target_path = self.docs_dir / doc_path.name
            rel_path = doc_path.relative_to(self.workspace_path)

            if self.dry_run:
                print(f"  🔍 {rel_path} -> {self.docs_dir.relative_to(self.workspace_path)}/")
            else:
                try:
                    shutil.move(str(doc_path), str(target_path))
                    self.files_moved.append({
                        'from': str(doc_path),
                        'to': str(target_path)
                    })
                    print(f"  ✅ {doc_path.name} 已移动")
                except Exception as e:
                    print(f"  ⚠️  移动失败 {doc_path.name}: {e}")

    def remove_nul_file(self):
        """删除可能误创建的 nul 文件"""
        print("\n" + "="*60)
        print("🗑️  检查并删除临时文件")
        print("="*60)

        nul_file = self.workspace_path / "nul"

        if not nul_file.exists():
            print("\n✅ 没有找到 nul 文件")
            return

        size = nul_file.stat().st_size
        print(f"\n找到 nul 文件 ({self.format_size(size)})")

        if self.dry_run:
            print(f"🔍 [演习模式] 将删除: nul")
        else:
            try:
                nul_file.unlink()
                self.space_freed += size
                print("✅ 已删除 nul 文件")
            except Exception as e:
                print(f"⚠️  删除失败: {e}")

    def cleanup_old_reports(self):
        """清理超过指定天数的旧报告"""
        print("\n" + "="*60)
        print(f"📋 清理旧报告 (超过 {self.report_retention_days} 天)")
        print("="*60)

        # 查找所有报告文件（清理报告、维护报告、健康报告）
        report_patterns = [
            "清理报告_*.md",
            "维护报告_*.md",
            "工作区健康报告_*.md"
        ]

        old_reports = []
        cutoff_date = self.today - timedelta(days=self.report_retention_days)

        # 查找所有报告文件
        for pattern in report_patterns:
            for report_file in self.workspace_path.glob(pattern):
                if report_file.is_file():
                    try:
                        # 从文件名提取日期
                        match = re.search(r'(\d{8})_', report_file.name)
                        if match:
                            file_date_str = match.group(1)
                            file_date = datetime.strptime(file_date_str, '%Y%m%d')

                            # 如果文件超过保留天数
                            if file_date < cutoff_date:
                                old_reports.append({
                                    'path': report_file,
                                    'date': file_date,
                                    'age_days': (self.today - file_date).days
                                })
                    except (ValueError, AttributeError):
                        # 如果无法解析日期，跳过
                        continue

        if not old_reports:
            print(f"\n✅ 没有超过 {self.report_retention_days} 天的报告")
            return

        # 按日期排序
        old_reports.sort(key=lambda x: x['date'])

        print(f"\n找到 {len(old_reports)} 个旧报告:")
        total_size = 0
        for report in old_reports[:5]:  # 只显示前5个
            size = report['path'].stat().st_size
            total_size += size
            print(f"  • {report['path'].name} ({report['age_days']} 天前, {self.format_size(size)})")
        if len(old_reports) > 5:
            print(f"  *... 还有 {len(old_reports) - 5} 个*")
            # 计算剩余文件大小
            for report in old_reports[5:]:
                total_size += report['path'].stat().st_size

        print(f"\n总大小: {self.format_size(total_size)}")

        # 创建归档目录
        if not self.archive_dir.exists():
            if self.dry_run:
                print(f"\n🔍 [演习模式] 将创建归档目录: {self.archive_dir.relative_to(self.workspace_path)}")
            else:
                self.archive_dir.mkdir(parents=True, exist_ok=True)
                print(f"✅ 已创建归档目录: {self.archive_dir.relative_to(self.workspace_path)}")

        # 移动或删除旧报告
        if self.dry_run:
            print(f"\n🔍 [演习模式] 将归档/删除 {len(old_reports)} 个旧报告:")
            print(f"  → 移动到归档目录: {self.archive_dir.relative_to(self.workspace_path)}")
        else:
            print(f"\n⚠️  正在归档旧报告...")
            for report in old_reports:
                try:
                    target_path = self.archive_dir / report['path'].name
                    shutil.move(str(report['path']), str(target_path))
                    self.old_reports_archived += 1
                except Exception as e:
                    print(f"  ⚠️  归档失败 {report['path'].name}: {e}")

            print(f"✅ 已归档 {self.old_reports_archived} 个旧报告")

    def generate_report(self):
        """生成清理报告"""
        print("\n" + "="*60)
        print("📊 清理报告")
        print("="*60)

        print(f"\n📅 时间: {self.today.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📂 工作区: {self.workspace_path}")
        print(f"🔍 模式: {'演习模式 (未实际删除)' if self.dry_run else '实际执行模式'}")

        print(f"\n🗑️  删除的缓存目录: {self.pycache_removed}")
        print(f"🗑️  删除的 .pyc 文件: {self.pyc_removed}")
        print(f"💾 释放的空间: {self.format_size(self.space_freed)}")
        print(f"📁 移动的文件: {len(self.files_moved)}")
        print(f"📋 归档的旧报告: {self.old_reports_archived}")

        if self.files_moved:
            print("\n移动的文件列表:")
            for file_move in self.files_moved:
                print(f"  • {Path(file_move['from']).name}")

        # 保存到文件
        report_filename = f"清理报告_{self.today.strftime('%Y%m%d_%H%M%S')}.md"
        report_path = self.workspace_path / report_filename

        report_content = f"""# 工作区清理报告

**生成时间**: {self.today.strftime('%Y-%m-%d %H:%M:%S')}
**工作区路径**: `{self.workspace_path}`
**执行模式**: {'演习模式 (未实际删除)' if self.dry_run else '实际执行模式'}

---

## 📊 清理统计

- **删除的缓存目录**: {self.pycache_removed}
- **删除的 .pyc 文件**: {self.pyc_removed}
- **释放的空间**: {self.format_size(self.space_freed)}
- **移动的文件**: {len(self.files_moved)}
- **归档的旧报告**: {self.old_reports_archived} (超过 {self.report_retention_days} 天)

---

## 📁 文件整理

{self._format_file_moves() if self.files_moved else '*无文件移动*'}

---

## ✅ 完成状态

清理任务已完成！工作区现在更加整洁了。

*本报告由 workspace_cleaner.py 自动生成*
"""

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)

        print(f"\n✅ 报告已保存: {report_filename}")
        return report_path

    def _format_file_moves(self):
        """格式化文件移动列表"""
        lines = []
        for file_move in self.files_moved:
            from_path = Path(file_move['from'])
            to_path = Path(file_move['to'])
            lines.append(f"- `{from_path.name}` → `{to_path.relative_to(self.workspace_path)}`")
        return "\n".join(lines)

    def run_cleanup(self):
        """执行完整的清理流程"""
        print("\n" + "="*60)
        print("🧹 工作区清理工具")
        print("="*60)

        mode_str = "🔍 演习模式" if self.dry_run else "⚡ 实际执行模式"
        print(f"\n{mode_str}")
        print(f"工作区: {self.workspace_path}")

        if self.dry_run:
            print("\n💡 提示: 这是演习模式，不会实际删除任何文件")
            print("   如需实际执行，请使用: python workspace_cleaner.py --execute")
        else:
            print("\n⚠️  警告: 将实际删除文件和移动文件！")
            print("   建议先运行演习模式查看效果")

        # 执行清理步骤
        self.clean_pycache()
        self.clean_pyc_files()
        self.organize_root_scripts()
        self.organize_root_docs()
        self.remove_nul_file()
        self.cleanup_old_reports()  # 清理旧报告

        # 生成报告
        return self.generate_report()


def main():
    """主函数"""
    import sys

    # 检查命令行参数
    dry_run = "--execute" not in sys.argv

    # 检查是否指定了自定义保留天数
    retention_days = 30  # 默认30天
    if "--retention" in sys.argv:
        try:
            idx = sys.argv.index("--retention")
            if idx + 1 < len(sys.argv):
                retention_days = int(sys.argv[idx + 1])
        except (ValueError, IndexError):
            print("⚠️  无效的保留天数参数，使用默认值 30 天")

    # 创建清理器
    cleaner = WorkspaceCleaner(dry_run=dry_run)
    cleaner.report_retention_days = retention_days

    try:
        # 运行清理
        report_path = cleaner.run_cleanup()
        print(f"\n✅ 清理完成！")
        return 0
    except Exception as e:
        print(f"\n❌ 清理过程出错: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
