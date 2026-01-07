#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日工作区快照工具 - 智能管家的"日记本"
每天自动记录工作区的状态、变更、活动
形成完整的工作区演进历史
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path


class DailySnapshot:
    """每日快照工具"""

    def __init__(self, workspace_root=None):
        """初始化快照工具

        Args:
            workspace_root: 工作区根目录
        """
        if workspace_root is None:
            workspace_root = Path(__file__).parent
        else:
            workspace_root = Path(workspace_root)

        self.workspace_root = workspace_root
        self.snapshots_dir = workspace_root / "06_Learning_Journal" / "workspace_memory" / "daily_snapshots"
        self.snapshots_dir.mkdir(parents=True, exist_ok=True)

    def create_snapshot(self):
        """创建今日快照"""
        today = datetime.now().strftime('%Y-%m-%d')
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        snapshot_file = self.snapshots_dir / f"snapshot_{today.replace('-', '')}.md"

        print(f"正在创建 {today} 的工作区快照...")

        snapshot_content = f"""# 工作区每日快照

**日期**: {today}
**快照时间**: {now}
**快照版本**: v1.0

---

## 📊 今日统计

### 项目概览
"""

        # 统计项目
        active_projects = self._scan_projects("01_Active_Projects")
        archived_projects = self._scan_projects("02_Project_Archive", count_only=True)

        snapshot_content += f"""
- **活跃项目**: {len(active_projects)} 个
- **归档项目**: {archived_projects} 个
"""

        # 活跃项目详情
        snapshot_content += "\n### 活跃项目列表\n\n"
        for project in active_projects:
            snapshot_content += f"#### {project['name']}\n\n"
            snapshot_content += f"- **路径**: `{project['path']}`\n"
            snapshot_content += f"- **文件数**: {project['file_count']}\n"
            snapshot_content += f"- **主要文件**: {', '.join(project['main_files'][:5])}\n"
            snapshot_content += f"- **最后修改**: {project['last_modified']}\n\n"

        # 工具脚本
        snapshot_content += "\n## 🛠️ 工具脚本状态\n\n"

        tools = self._scan_tools()
        for tool in tools:
            snapshot_content += f"- **{tool['name']}** - {tool['size']} bytes - {tool['modified']}\n"

        # 学习日志
        snapshot_content += "\n## 📓 学习日志\n\n"

        learning_summary = self._scan_learning_journal()
        snapshot_content += f"- **每日日志**: {learning_summary['daily_logs']} 篇\n"
        snapshot_content += f"- **解决的问题**: {learning_summary['challenges']} 个\n"
        snapshot_content += f"- **代码模式**: {learning_summary['patterns']} 个\n\n"

        # 今日变更
        snapshot_content += "## 🔄 今日变更\n\n"
        snapshot_content += self._detect_changes()

        # 明日计划
        snapshot_content += "\n## 📅 明日计划\n\n"
        snapshot_content += "- [ ] 待添加项目\n"
        snapshot_content += "- [ ] 待学习内容\n"
        snapshot_content += "- [ ] 待解决问题\n\n"

        # 备注
        snapshot_content += "---\n\n"
        snapshot_content += "## 📝 备注\n\n"
        snapshot_content += "在此记录今日的重要事件、想法、决策等\n\n"
        snapshot_content += "---\n\n"
        snapshot_content += f"**快照生成**: {now}\n"
        snapshot_content += f"**生成工具**: daily_snapshot.py\n"

        # 保存快照
        with open(snapshot_file, 'w', encoding='utf-8') as f:
            f.write(snapshot_content)

        print(f"[OK] 快照已保存: {snapshot_file}")

        # 复制为最新快照
        latest_snapshot = self.snapshots_dir / "snapshot_latest.md"
        shutil.copy(snapshot_file, latest_snapshot)
        print(f"[OK] 最新快照已更新: {latest_snapshot}")

        return snapshot_file

    def _scan_projects(self, projects_dir_name, count_only=False):
        """扫描项目目录"""
        projects_dir = self.workspace_root / projects_dir_name

        if not projects_dir.exists():
            if count_only:
                return 0
            return []

        projects = []

        for project_dir in projects_dir.iterdir():
            if not project_dir.is_dir() or project_dir.name.startswith('.'):
                continue

            if count_only:
                continue

            # 统计文件
            files = list(project_dir.rglob('*'))
            file_count = len([f for f in files if f.is_file()])

            # 主要文件
            py_files = [f.name for f in project_dir.rglob('*.py')
                       if 'venv' not in str(f) and '__pycache__' not in str(f)]
            md_files = [f.name for f in project_dir.rglob('*.md')]

            main_files = py_files[:3] + md_files[:2]

            # 最后修改时间
            last_modified = datetime.fromtimestamp(
                project_dir.stat().st_mtime
            ).strftime('%Y-%m-%d %H:%M')

            projects.append({
                'name': project_dir.name,
                'path': f"{projects_dir_name}/{project_dir.name}",
                'file_count': file_count,
                'main_files': main_files,
                'last_modified': last_modified
            })

        if count_only:
            return len(projects)

        return projects

    def _scan_tools(self):
        """扫描工具脚本"""
        tools = []

        for pattern in ['*.py', '*.bat']:
            for tool_file in self.workspace_root.glob(pattern):
                if tool_file.name.startswith(('workspace_', 'check_', 'setup_',
                                             'run_', 'create_', 'generate_',
                                             'start_new_session', 'butler_mode')):
                    stat = tool_file.stat()
                    tools.append({
                        'name': tool_file.name,
                        'size': stat.st_size,
                        'modified': datetime.fromtimestamp(
                            stat.st_mtime
                        ).strftime('%Y-%m-%d %H:%M')
                    })

        return sorted(tools, key=lambda x: x['modified'], reverse=True)

    def _scan_learning_journal(self):
        """扫描学习日志"""
        journal_dir = self.workspace_root / "06_Learning_Journal"

        summary = {
            'daily_logs': 0,
            'challenges': 0,
            'patterns': 0
        }

        # 统计每日日志
        if (journal_dir / "daily_logs").exists():
            summary['daily_logs'] = len(list((journal_dir / "daily_logs").rglob('*.md')))

        # 统计解决的问题
        if (journal_dir / "challenges_solved").exists():
            for file in (journal_dir / "challenges_solved").glob('*.md'):
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    summary['challenges'] += content.count('## ')

        # 统计代码模式
        if (journal_dir / "code_patterns").exists():
            summary['patterns'] = len(list((journal_dir / "code_patterns").rglob('*.md')))

        return summary

    def _detect_changes(self):
        """检测今日变更（简单版本）"""
        # 这里可以与之前的版本对比
        # 目前只提供简单的检测

        changes = []

        # 检查最近修改的文件
        recent_files = []
        for pattern in ['*.py', '*.md', '*.bat']:
            for file in self.workspace_root.glob(pattern):
                if 'venv' in str(file) or '__pycache__' in str(file):
                    continue

                stat = file.stat()
                modified_time = datetime.fromtimestamp(stat.st_mtime)
                hours_ago = (datetime.now() - modified_time).total_seconds() / 3600

                if hours_ago < 24:
                    recent_files.append({
                        'path': str(file.relative_to(self.workspace_root)),
                        'modified': modified_time.strftime('%H:%M')
                    })

        if recent_files:
            changes.append("### 最近24小时修改的文件\n\n")
            for file in sorted(recent_files, key=lambda x: x['modified'], reverse=True)[:10]:
                changes.append(f"- `{file['path']}` - {file['modified']}\n")

        if not changes:
            changes.append("未检测到明显的变更\n")

        return ''.join(changes)

    def generate_weekly_report(self):
        """生成周报"""
        # 找到本周的所有快照
        snapshots = sorted(self.snapshots_dir.glob("snapshot_*.md"))

        if len(snapshots) < 2:
            print("快照数量不足，无法生成周报")
            return

        weekly_report = f"""# 工作区周报

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**报告周期**: 本周

---

## 📊 本周概览

本周共生成 {len(snapshots)} 个快照

详细内容请查看各日快照文件。

---

**生成工具**: daily_snapshot.py
"""

        report_file = self.snapshots_dir / f"weekly_report_{datetime.now().strftime('%Y%m%d')}.md"

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(weekly_report)

        print(f"[OK] 周报已生成: {report_file}")


def main():
    """主程序"""
    import sys
    import io

    if sys.platform == "win32":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    print("="*70)
    print("每日工作区快照工具")
    print("="*70)

    snapshot = DailySnapshot()

    # 创建今日快照
    snapshot.create_snapshot()

    print("\n" + "="*70)
    print("快照创建完成!")
    print("工作区的今天已被记录")
    print("="*70)


if __name__ == "__main__":
    main()
