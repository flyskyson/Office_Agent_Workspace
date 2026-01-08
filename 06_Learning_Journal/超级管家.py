#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
超级管家 - 一键获取工作区所有关键信息
让AI能够立即回答关于你工作区的任何问题
"""

import json
from datetime import datetime
from pathlib import Path


class SuperButler:
    """超级管家 - 收集所有关键信息"""

    def __init__(self, workspace_root=None):
        """初始化"""
        if workspace_root is None:
            workspace_root = Path(__file__).parent
        else:
            workspace_root = Path(workspace_root)

        self.workspace_root = workspace_root
        self.memory_dir = workspace_root / "06_Learning_Journal" / "workspace_memory"
        self.config_dir = workspace_root / ".claude"

    def get_all_info(self):
        """获取所有信息 - 返回完整报告"""
        info = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "workspace_path": str(self.workspace_root),
        }

        # 1. MCP服务器配置
        info["mcp_servers"] = self.get_mcp_servers()

        # 2. 工作区索引
        info["workspace_index"] = self.get_workspace_index()

        # 3. 项目列表
        info["projects"] = self.get_projects_summary()

        # 4. 工具脚本
        info["tools"] = self.get_tools_summary()

        # 5. 最近活动
        info["recent_activity"] = self.get_recent_activity()

        # 6. 笔记和文档
        info["notes"] = self.get_notes_summary()

        # 7. 数据新鲜度
        info["data_freshness"] = self.check_data_freshness()

        return info

    def get_mcp_servers(self):
        """获取MCP服务器配置"""
        mcp_config = self.workspace_root / ".mcp.json"

        if not mcp_config.exists():
            return {"status": "未找到MCP配置文件", "servers": []}

        try:
            with open(mcp_config, 'r', encoding='utf-8') as f:
                config = json.load(f)

            servers = []
            for name, details in config.get('mcpServers', {}).items():
                servers.append({
                    "name": name,
                    "command": details.get('command', ''),
                    "installed": True
                })

            return {
                "status": "已配置",
                "count": len(servers),
                "servers": servers
            }
        except Exception as e:
            return {"status": f"读取失败: {e}", "servers": []}

    def get_workspace_index(self):
        """获取工作区索引"""
        index_file = self.memory_dir / "workspace_index_latest.json"

        if not index_file.exists():
            return {"status": "未找到索引文件", "scan_time": None}

        try:
            with open(index_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            return {
                "status": "已索引",
                "scan_time": data.get('scan_time'),
                "total_projects": len(data.get('projects', [])),
                "total_tools": len(data.get('tools', [])),
                "total_scripts": len(data.get('scripts', []))
            }
        except Exception as e:
            return {"status": f"读取失败: {e}"}

    def get_projects_summary(self):
        """获取项目摘要"""
        index_file = self.memory_dir / "workspace_index_latest.json"

        if not index_file.exists():
            return {"active": [], "archived": []}

        try:
            with open(index_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            projects = data.get('projects', [])

            active = []
            archived = []

            for p in projects:
                summary = {
                    "name": p.get('name'),
                    "path": p.get('path'),
                    "last_modified": p.get('last_modified'),
                    "py_files": p.get('py_files_count', 0),
                    "has_readme": p.get('has_readme', False)
                }

                if p.get('status') == 'active':
                    active.append(summary)
                else:
                    archived.append(summary)

            return {
                "active": active,
                "archived": archived,
                "active_count": len(active),
                "archived_count": len(archived)
            }
        except Exception as e:
            return {"error": str(e)}

    def get_tools_summary(self):
        """获取工具摘要"""
        index_file = self.memory_dir / "workspace_index_latest.json"

        if not index_file.exists():
            return {"python_tools": [], "batch_scripts": []}

        try:
            with open(index_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            tools = [
                {"name": t.get('name'), "modified": t.get('modified')}
                for t in data.get('tools', [])
            ]

            scripts = [
                {"name": s.get('name'), "modified": s.get('modified')}
                for s in data.get('scripts', [])
            ]

            return {
                "python_tools": tools,
                "batch_scripts": scripts,
                "python_tools_count": len(tools),
                "batch_scripts_count": len(scripts)
            }
        except Exception as e:
            return {"error": str(e)}

    def get_recent_activity(self):
        """获取最近活动"""
        # 查找最近生成的报告
        reports = list(self.workspace_root.glob("*报告_*.md"))

        recent_reports = []
        for report in reports[:5]:  # 最近5个
            recent_reports.append({
                "name": report.name,
                "modified": datetime.fromtimestamp(report.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            })

        return {
            "recent_reports": recent_reports,
            "count": len(recent_reports)
        }

    def get_notes_summary(self):
        """获取笔记摘要"""
        notes = []

        # 查找学习日志
        daily_logs_dir = self.workspace_root / "06_Learning_Journal" / "daily_logs"
        if daily_logs_dir.exists():
            log_files = list(daily_logs_dir.rglob("*.md"))
            notes.append({
                "type": "学习日志",
                "location": "06_Learning_Journal/daily_logs/",
                "count": len(log_files)
            })

        # 查找挑战记录
        challenges_dir = self.workspace_root / "06_Learning_Journal" / "challenges_solved"
        if challenges_dir.exists():
            challenge_files = list(challenges_dir.rglob("*.md"))
            notes.append({
                "type": "问题解决记录",
                "location": "06_Learning_Journal/challenges_solved/",
                "count": len(challenge_files)
            })

        # 查找代码模式
        patterns_dir = self.workspace_root / "06_Learning_Journal" / "code_patterns"
        if patterns_dir.exists():
            pattern_files = list(patterns_dir.rglob("*.md"))
            notes.append({
                "type": "代码模式",
                "location": "06_Learning_Journal/code_patterns/",
                "count": len(pattern_files)
            })

        return {
            "total_categories": len(notes),
            "categories": notes
        }

    def check_data_freshness(self):
        """检查数据新鲜度"""
        index_file = self.memory_dir / "workspace_index_latest.json"

        if not index_file.exists():
            return {
                "index_exists": False,
                "recommendation": "请运行: python workspace_scanner.py"
            }

        # 检查索引时间
        mtime = index_file.stat().st_mtime
        scan_time = datetime.fromtimestamp(mtime)
        age_hours = (datetime.now() - scan_time).total_seconds() / 3600

        if age_hours < 1:
            freshness = "非常新鲜"
            recommendation = "数据最新"
        elif age_hours < 24:
            freshness = "较新"
            recommendation = "数据较新,建议每日刷新"
        elif age_hours < 168:  # 7天
            freshness = "一般"
            recommendation = "数据已陈旧,建议运行: python workspace_scanner.py"
        else:
            freshness = "陈旧"
            recommendation = "数据过时,请立即运行: python workspace_scanner.py"

        return {
            "index_exists": True,
            "last_scan": scan_time.strftime("%Y-%m-%d %H:%M:%S"),
            "age_hours": round(age_hours, 1),
            "freshness": freshness,
            "recommendation": recommendation
        }

    def print_report(self):
        """打印可读报告"""
        info = self.get_all_info()

        print("\n" + "="*70)
        print("超级管家报告".center(70))
        print("="*70)
        print(f"\n生成时间: {info['timestamp']}")
        print(f"工作区路径: {info['workspace_path']}")

        # MCP服务器
        print("\n" + "-"*70)
        print("MCP服务器配置:")
        mcp = info['mcp_servers']
        print(f"  状态: {mcp['status']}")
        print(f"  数量: {mcp['count']} 个")
        for server in mcp['servers']:
            print(f"    - {server['name']}")

        # 数据新鲜度
        print("\n" + "-"*70)
        print("数据新鲜度:")
        fresh = info['data_freshness']
        if fresh['index_exists']:
            print(f"  最后扫描: {fresh['last_scan']}")
            print(f"  数据年龄: {fresh['age_hours']} 小时")
            print(f"  新鲜度: {fresh['freshness']}")
            print(f"  建议: {fresh['recommendation']}")
        else:
            print(f"  状态: {fresh['recommendation']}")

        # 项目
        print("\n" + "-"*70)
        print("项目资产:")
        projects = info['projects']
        print(f"  活跃项目: {projects['active_count']} 个")
        for p in projects['active']:
            print(f"    - {p['name']:30s} | {p['last_modified']} | {p['py_files']}个文件")
        print(f"  归档项目: {projects['archived_count']} 个")
        for p in projects['archived']:
            print(f"    - {p['name']}")

        # 工具
        print("\n" + "-"*70)
        print("工具脚本:")
        tools = info['tools']
        if 'error' not in tools:
            print(f"  Python工具: {tools['python_tools_count']} 个")
            for t in tools['python_tools'][:10]:  # 只显示前10个
                print(f"    - {t['name']}")
            print(f"  批处理脚本: {tools['batch_scripts_count']} 个")
            for s in tools['batch_scripts'][:10]:
                print(f"    - {s['name']}")

        # 笔记
        print("\n" + "-"*70)
        print("笔记和文档:")
        notes = info['notes']
        print(f"  分类数量: {notes['total_categories']} 个")
        for cat in notes['categories']:
            print(f"    - {cat['type']}: {cat['count']}个文件 ({cat['location']})")

        # 最近活动
        print("\n" + "-"*70)
        print("最近活动:")
        activity = info['recent_activity']
        print(f"  最近报告: {activity['count']} 个")
        for report in activity['recent_reports']:
            print(f"    - {report['name']} ({report['modified']})")

        print("\n" + "="*70)
        print()

    def export_json(self, output_file=None):
        """导出为JSON文件供AI读取"""
        info = self.get_all_info()

        if output_file is None:
            output_file = self.workspace_root / "06_Learning_Journal" / "workspace_memory" / "super_butler_report.json"

        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(info, f, ensure_ascii=False, indent=2)

        return output_file


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='超级管家 - 一键获取工作区所有信息')
    parser.add_argument('--export', '-e', action='store_true', help='导出为JSON文件')
    parser.add_argument('--json-only', '-j', action='store_true', help='只导出JSON,不打印报告')

    args = parser.parse_args()

    butler = SuperButler()

    if args.export or args.json_only:
        output_file = butler.export_json()
        if not args.json_only:
            print(f"\n已导出报告到: {output_file}")

    if not args.json_only:
        butler.print_report()


if __name__ == '__main__':
    main()
