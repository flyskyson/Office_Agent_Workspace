#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目进度追踪器
帮助你管理多个项目,不用担心忘记进度
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# 设置控制台编码为UTF-8
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

class ProjectTracker:
    """项目进度追踪器"""

    def __init__(self, workspace_root=None):
        if workspace_root is None:
            workspace_root = Path(__file__).parent
        self.workspace_root = Path(workspace_root)
        self.tracker_file = self.workspace_root / "06_Learning_Journal" / "workspace_memory" / "project_progress.json"

    def load_progress(self):
        """加载项目进度"""
        if not self.tracker_file.exists():
            return {}

        with open(self.tracker_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_progress(self, data):
        """保存项目进度"""
        self.tracker_file.parent.mkdir(parents=True, exist_ok=True)

        with open(self.tracker_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def update_project(self, project_name, status, progress_pct, current_task, notes=""):
        """更新项目进度"""
        data = self.load_progress()

        data[project_name] = {
            "status": status,  # active, paused, completed, archived
            "progress": progress_pct,
            "current_task": current_task,
            "notes": notes,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        self.save_progress(data)
        print(f"✅ 项目 {project_name} 进度已更新")

    def get_project_status(self, project_name):
        """获取项目状态"""
        data = self.load_progress()

        if project_name not in data:
            print(f"⚠️  项目 {project_name} 尚未记录")
            return None

        project = data[project_name]
        print(f"\n📊 项目: {project_name}")
        print(f"   状态: {project['status']}")
        print(f"   进度: {project['progress']}%")
        print(f"   当前任务: {project['current_task']}")
        print(f"   最后更新: {project['last_updated']}")
        if project['notes']:
            print(f"   备注: {project['notes']}")

        return project

    def list_all_projects(self):
        """列出所有项目"""
        data = self.load_progress()

        if not data:
            print("📋 尚未记录任何项目")
            return

        print("\n" + "=" * 70)
        print("📋 所有项目进度")
        print("=" * 70)

        for name, info in data.items():
            status_icon = {
                "active": "🟢",
                "paused": "⏸️ ",
                "completed": "✅",
                "archived": "📦"
            }.get(info['status'], "❓")

            progress_bar = "█" * (info['progress'] // 10) + "░" * (10 - info['progress'] // 10)

            print(f"\n{status_icon} {name}")
            print(f"   进度: [{progress_bar}] {info['progress']}%")
            print(f"   当前: {info['current_task']}")
            print(f"   更新: {info['last_updated']}")

    def pause_project(self, project_name, notes=""):
        """暂停项目"""
        self.update_project(
            project_name,
            status="paused",
            progress_pct=self.load_progress().get(project_name, {}).get('progress', 0),
            current_task="已暂停",
            notes=notes
        )
        print(f"⏸️  项目 {project_name} 已暂停")

    def resume_project(self, project_name, new_task=""):
        """恢复项目"""
        data = self.load_progress()

        if project_name not in data:
            print(f"⚠️  项目 {project_name} 尚未记录")
            return

        project = data[project_name]
        notes = f"上次任务: {project['current_task']}" if not new_task else new_task

        self.update_project(
            project_name,
            status="active",
            progress_pct=project['progress'],
            current_task=notes,
            notes=f"从 {project['last_updated']} 恢复"
        )
        print(f"▶️  项目 {project_name} 已恢复")

    def start_new_project(self, project_name, description=""):
        """开始新项目"""
        data = self.load_progress()

        # 如果有活跃项目,先暂停
        for name, info in data.items():
            if info['status'] == 'active':
                print(f"⚠️  检测到活跃项目: {name}")
                choice = input(f"是否暂停 {name} 并开始新项目? (y/n): ").strip().lower()
                if choice == 'y':
                    self.pause_project(name, f"转而开发 {project_name}")

        self.update_project(
            project_name,
            status="active",
            progress_pct=0,
            current_task="项目初始化",
            notes=description
        )
        print(f"🚀 新项目 {project_name} 已开始")


def main():
    """命令行界面"""
    import sys

    tracker = ProjectTracker()

    if len(sys.argv) < 2:
        print("""
📋 项目进度追踪器 - 使用方法

1. 查看所有项目:
   python project_tracker.py list

2. 开始新项目:
   python project_tracker.py start <项目名>

3. 更新项目进度:
   python project_tracker.py update <项目名> <进度%> <当前任务>

4. 查看项目状态:
   python project_tracker.py status <项目名>

5. 暂停项目:
   python project_tracker.py pause <项目名> [备注]

6. 恢复项目:
   python project_tracker.py resume <项目名> [新任务]

示例:
  python project_tracker.py start backup_tool
  python project_tracker.py update file_organizer 85 "添加进度提示"
  python project_tracker.py pause file_organizer "临时开发备份工具"
  python project_tracker.py resume file_organizer
        """)
        return

    command = sys.argv[1]

    if command == "list":
        tracker.list_all_projects()

    elif command == "start":
        if len(sys.argv) < 3:
            print("❌ 请提供项目名")
            return
        project_name = sys.argv[2]
        description = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else ""
        tracker.start_new_project(project_name, description)

    elif command == "update":
        if len(sys.argv) < 5:
            print("❌ 用法: update <项目名> <进度%> <当前任务>")
            return
        project_name = sys.argv[2]
        progress = int(sys.argv[3])
        current_task = " ".join(sys.argv[4:])
        tracker.update_project(project_name, "active", progress, current_task)

    elif command == "status":
        if len(sys.argv) < 3:
            print("❌ 请提供项目名")
            return
        tracker.get_project_status(sys.argv[2])

    elif command == "pause":
        if len(sys.argv) < 3:
            print("❌ 请提供项目名")
            return
        project_name = sys.argv[2]
        notes = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else ""
        tracker.pause_project(project_name, notes)

    elif command == "resume":
        if len(sys.argv) < 3:
            print("❌ 请提供项目名")
            return
        project_name = sys.argv[2]
        new_task = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else ""
        tracker.resume_project(project_name, new_task)

    else:
        print(f"❌ 未知命令: {command}")


if __name__ == "__main__":
    main()
