#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能管家项目查询工具
让工作区管家能够回答项目相关问题
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# 设置控制台编码为UTF-8
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


class SmartButlerProjectQuery:
    """智能管家项目查询系统"""

    def __init__(self, workspace_root=None):
        if workspace_root is None:
            workspace_root = Path(__file__).parent
        self.workspace_root = Path(workspace_root)

        # 数据源
        self.progress_file = self.workspace_root / "06_Learning_Journal" / "workspace_memory" / "project_progress_enhanced.json"
        self.workspace_index = self.workspace_root / "06_Learning_Journal" / "workspace_memory" / "workspace_index_latest.json"

    def load_project_data(self):
        """加载项目数据"""
        # 优先加载增强版进度数据
        if self.progress_file.exists():
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                return json.load(f)

        # 退而求其次，加载普通进度数据
        tracker_file = self.workspace_root / "06_Learning_Journal" / "workspace_memory" / "project_progress.json"
        if tracker_file.exists():
            with open(tracker_file, 'r', encoding='utf-8') as f:
                return {"projects": json.load(f)}

        # 最后加载工作区索引
        if self.workspace_index.exists():
            with open(self.workspace_index, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 转换格式
                return {"projects": {p['name']: p for p in data.get('projects', [])}}

        return {"projects": {}}

    def get_project_status(self, project_name=None):
        """获取项目状态

        Args:
            project_name: 项目名，None表示查询所有项目

        Returns:
            str: 格式化的项目状态信息
        """
        data = self.load_project_data()
        projects = data.get('projects', {})

        if project_name:
            # 查询特定项目
            if project_name not in projects:
                return f"❌ 项目 '{project_name}' 不存在"

            project = projects[project_name]

            # 判断数据格式
            if 'progress' in project:
                # 增强版格式
                return self._format_enhanced_project(project_name, project)
            else:
                # 基础格式
                return self._format_basic_project(project_name, project)
        else:
            # 查询所有项目
            if not projects:
                return "📋 暂无项目记录"

            result = ["\n" + "=" * 70]
            result.append("📋 所有项目状态")
            result.append("=" * 70)

            for name, proj in projects.items():
                if 'progress' in proj:
                    status_icon = {
                        'active': '🟢',
                        'paused': '⏸️ ',
                        'completed': '✅',
                        'archived': '📦'
                    }.get(proj['basic_info']['status'], '❓')

                    progress = proj['progress']['percentage']
                    progress_bar = '█' * (progress // 10) + '░' * (10 - progress // 10)

                    result.append(f"\n{status_icon} {name}")
                    result.append(f"   进度: [{progress_bar}] {progress}%")
                    result.append(f"   当前: {proj['progress']['current_task']}")
                    result.append(f"   更新: {proj['progress']['last_updated']}")
                else:
                    result.append(f"\n🟢 {name}")
                    result.append(f"   状态: {proj.get('status', 'unknown')}")
                    result.append(f"   最后修改: {proj.get('last_modified', 'Unknown')}")

            return '\n'.join(result)

    def _format_enhanced_project(self, name, project):
        """格式化增强版项目信息"""
        basic = project.get('basic_info', {})
        progress = project.get('progress', {})
        milestones = project.get('milestones', {})

        result = [f"\n📊 项目: {name}"]
        result.append("-" * 70)

        # 基本信息
        result.append(f"📍 位置: {basic.get('path', 'N/A')}")
        result.append(f"📄 文件: {basic.get('py_files_count', 0)} 个Python文件")

        # 进度信息
        pct = progress.get('percentage', 0)
        progress_bar = '█' * (pct // 10) + '░' * (10 - pct // 10)
        result.append(f"\n📈 进度: [{progress_bar}] {pct}%")
        result.append(f"🎯 当前任务: {progress.get('current_task', 'N/A')}")
        result.append(f"📝 备注: {progress.get('notes', '无')}")
        result.append(f"⏰ 最后更新: {progress.get('last_updated', 'N/A')}")

        # 里程碑
        if milestones:
            result.append(f"\n✅ 已完成:")
            for item in milestones.get('completed', [])[:3]:
                result.append(f"   • {item}")

            if milestones.get('in_progress'):
                result.append(f"\n🚧 进行中:")
                for item in milestones.get('in_progress', []):
                    result.append(f"   • {item}")

            if milestones.get('todo'):
                result.append(f"\n📋 待办:")
                for item in milestones.get('todo', [])[:3]:
                    result.append(f"   • {item}")

        return '\n'.join(result)

    def _format_basic_project(self, name, project):
        """格式化基础项目信息"""
        result = [f"\n📊 项目: {name}"]
        result.append("-" * 70)
        result.append(f"📍 位置: {project.get('path', 'N/A')}")
        result.append(f"📄 状态: {project.get('status', 'unknown')}")
        result.append(f"⏰ 最后修改: {project.get('last_modified', 'N/A')}")
        return '\n'.join(result)

    def get_recommendation(self):
        """获取智能推荐

        Returns:
            str: 推荐建议
        """
        data = self.load_project_data()
        projects = data.get('projects', {})

        if not projects:
            return "💡 建议: 开始使用 project_tracker.py 记录你的第一个项目!"

        recommendations = []

        for name, proj in projects.items():
            if 'progress' in proj:
                progress = proj['progress']
                pct = progress.get('percentage', 0)

                if pct < 30:
                    recommendations.append(f"🌱 {name}: 项目刚起步,建议先完成基础功能")
                elif 30 <= pct < 80:
                    recommendations.append(f"🔥 {name}: 项目进展良好,当前任务: {progress.get('current_task', 'N/A')}")
                elif 80 <= pct < 100:
                    recommendations.append(f"🏁 {name}: 即将完成!冲刺阶段: {progress.get('current_task', 'N/A')}")
                else:
                    recommendations.append(f"✅ {name}: 已完成,可以考虑归档或开始新项目")

        if not recommendations:
            return "💡 建议: 继续保持良好的开发节奏!"

        result = ["\n" + "=" * 70]
        result.append("🎯 智能推荐")
        result.append("=" * 70)
        result.extend(recommendations)

        return '\n'.join(result)


def main():
    """命令行界面"""
    import sys

    query = SmartButlerProjectQuery()

    if len(sys.argv) < 2:
        print("""
🤖 智能管家项目查询系统

使用方法:

1. 查看所有项目:
   python 智能管家项目查询.py list

2. 查看特定项目:
   python 智能管家项目查询.py status <项目名>

3. 获取智能推荐:
   python 智能管家项目查询.py recommend

示例:
  python 智能管家项目查询.py list
  python 智能管家项目查询.py status file_organizer
  python 智能管家项目查询.py recommend
        """)
        return

    command = sys.argv[1]

    if command == "list":
        print(query.get_project_status())

    elif command == "status":
        if len(sys.argv) < 3:
            print("❌ 请提供项目名")
            print("   示例: python 智能管家项目查询.py status file_organizer")
            return
        print(query.get_project_status(sys.argv[2]))

    elif command == "recommend":
        print(query.get_recommendation())

    else:
        print(f"❌ 未知命令: {command}")


if __name__ == "__main__":
    main()
