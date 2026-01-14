#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Office Agent 版本管理和演进系统
确保代码的连贯性、向后兼容和渐进式升级

作者: Claude Code
日期: 2026-01-12
"""

import json
import shutil
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import hashlib

# Windows 终端编码修复
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass


class VersionManager:
    """
    版本管理器 - 管理所有工具的版本和兼容性

    核心原则:
    1. 新版本不删除旧代码，而是添加新功能
    2. 保持旧API可用，添加新API
    3. 每次升级记录变更日志
    4. 提供版本切换能力
    """

    def __init__(self, workspace_root=None):
        if workspace_root is None:
            workspace_root = Path(__file__).parent.parent
        self.workspace_root = Path(workspace_root)
        self.version_file = self.workspace_root / "06_Learning_Journal" / "version_registry.json"
        self.backup_dir = self.workspace_root / "02_Project_Archive" / "version_backups"

        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.registry = self._load_registry()

    def _load_registry(self):
        """加载版本注册表"""
        if self.version_file.exists():
            with open(self.version_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "tools": {},
            "last_update": None,
            "current_version": "1.0.0"
        }

    def _save_registry(self):
        """保存版本注册表"""
        self.registry['last_update'] = datetime.now().isoformat()
        with open(self.version_file, 'w', encoding='utf-8') as f:
            json.dump(self.registry, f, ensure_ascii=False, indent=2)

    def register_tool(self, tool_name: str, version: str, file_path: str,
                     api_version: str = "1.0",
                     description: str = "",
                     dependencies: List[str] = None):
        """
        注册工具版本

        参数:
            tool_name: 工具名称
            version: 当前版本 (如 "1.0.0")
            file_path: 主文件路径
            api_version: API版本 (用于向后兼容)
            description: 描述
            dependencies: 依赖的其他工具
        """
        if tool_name not in self.registry['tools']:
            self.registry['tools'][tool_name] = {
                "name": tool_name,
                "versions": [],
                "current_version": version,
                "api_version": api_version,
                "description": description,
                "dependencies": dependencies or []
            }

        tool = self.registry['tools'][tool_name]

        # 检查版本是否已存在
        version_exists = any(v['version'] == version for v in tool['versions'])

        if not version_exists:
            tool['versions'].append({
                "version": version,
                "file_path": file_path,
                "released": datetime.now().isoformat(),
                "api_version": api_version,
                "changelog": []
            })

        tool['current_version'] = version
        self._save_registry()

        print(f"[注册] {tool_name} v{version}")

    def add_changelog(self, tool_name: str, version: str, changes: List[str]):
        """
        添加版本变更日志

        参数:
            tool_name: 工具名称
            version: 版本号
            changes: 变更列表 ["新增功能", "修复bug"]
        """
        if tool_name not in self.registry['tools']:
            return

        tool = self.registry['tools'][tool_name]

        for ver_info in tool['versions']:
            if ver_info['version'] == version:
                ver_info['changelog'].extend(changes)
                break

        self._save_registry()

    def backup_before_upgrade(self, tool_name: str, file_path: Path):
        """
        升级前备份

        创建快照，确保可以回滚
        """
        if not file_path.exists():
            return

        # 计算文件哈希
        with open(file_path, 'rb') as f:
            file_hash = hashlib.md5(f.read()).hexdigest()[:8]

        # 备份文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{tool_name}_{timestamp}_{file_hash}.py"
        backup_path = self.backup_dir / backup_name

        # 复制文件
        shutil.copy2(file_path, backup_path)

        print(f"[备份] {tool_name} -> {backup_name}")

        # 记录备份
        if tool_name not in self.registry['tools']:
            self.registry['tools'][tool_name] = {"versions": []}

        if 'backups' not in self.registry['tools'][tool_name]:
            self.registry['tools'][tool_name]['backups'] = []

        self.registry['tools'][tool_name]['backups'].append({
            "file": backup_name,
            "original": str(file_path),
            "created": timestamp,
            "hash": file_hash
        })

        self._save_registry()

        return backup_path

    def get_tool_info(self, tool_name: str) -> Dict:
        """获取工具完整信息"""
        return self.registry['tools'].get(tool_name, {})

    def list_all_tools(self):
        """列出所有工具及其版本"""
        for tool_name, tool_info in self.registry['tools'].items():
            print(f"\n{tool_name}")
            print(f"  当前版本: {tool_info.get('current_version', '未知')}")
            print(f"  API版本: {tool_info.get('api_version', '未知')}")
            print(f"  所有版本: {', '.join([v['version'] for v in tool_info.get('versions', [])])}")

    def export_report(self, output_file: Path = None):
        """导出版本报告"""
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.workspace_root / "06_Learning_Journal" / f"version_report_{timestamp}.md"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Office Agent 版本报告\n\n")
            f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            for tool_name, tool_info in self.registry['tools'].items():
                f.write(f"## {tool_name}\n\n")
                f.write(f"- **当前版本**: {tool_info.get('current_version', '未知')}\n")
                f.write(f"- **API版本**: {tool_info.get('api_version', '未知')}\n")
                f.write(f"- **描述**: {tool_info.get('description', '无')}\n\n")

                if tool_info.get('versions'):
                    f.write("### 版本历史\n\n")
                    for ver_info in tool_info['versions']:
                        f.write(f"#### {ver_info['version']}\n")
                        f.write(f"- **发布时间**: {ver_info.get('released', '未知')}\n")
                        f.write(f"- **API版本**: {ver_info.get('api_version', '未知')}\n")
                        f.write(f"- **文件**: `{ver_info.get('file_path', '未知')}`\n")

                        if ver_info.get('changelog'):
                            f.write("- **变更**:\n")
                            for change in ver_info['changelog']:
                                f.write(f"  - {change}\n")
                        f.write("\n")

        print(f"[报告] 已导出到: {output_file}")


class APICompatibilityLayer:
    """
    API 兼容层 - 确保旧代码继续工作

    原则:
    1. 新API = 增强功能，不破坏旧API
    2. 旧API调用内部转发到新实现
    3. 提供渐进式迁移路径
    """

    def __init__(self, version_manager: VersionManager):
        self.vm = version_manager

    def wrap_old_api(self, old_func, new_func, deprecation_warning=None):
        """
        包装旧API，使其调用新实现

        使用:
            # 旧函数
            def old_organize():
                pass

            # 新函数
            def new_organize(**kwargs):
                pass

            # 包装
            wrapped = wrap_old_api(old_organize, new_organize, "请使用 new_organize")
        """
        def wrapper(*args, **kwargs):
            if deprecation_warning:
                import warnings
                warnings.warn(deprecation_warning, DeprecationWarning, stacklevel=2)

            # 转发到新实现
            return new_func(**kwargs)

        # 保留原函数的文档字符串
        wrapper.__doc__ = old_func.__doc__
        wrapper.__name__ = old_func.__name__

        return wrapper

    def migrate_config(self, old_config: Dict, migration_map: Dict) -> Dict:
        """
        配置文件迁移

        参数:
            old_config: 旧配置
            migration_map: 迁移映射 {"old_key": "new_key"}

        返回:
            新配置
        """
        new_config = {}

        # 复制旧配置（使用新键名）
        for old_key, new_key in migration_map.items():
            if old_key in old_config:
                new_config[new_key] = old_config[old_key]

        # 保留不在映射中的配置
        for key, value in old_config.items():
            if key not in migration_map:
                new_config[key] = value

        return new_config


class EvolutionTracker:
    """
    演进追踪器 - 记录系统的进化历程

    用途:
    1. 记录每次升级的动机和目标
    2. 记录采用的技术和模式
    3. 评估升级效果
    4. 规划下一步演进
    """

    def __init__(self, workspace_root=None):
        if workspace_root is None:
            workspace_root = Path(__file__).parent.parent
        self.workspace_root = Path(workspace_root)
        self.evolution_file = self.workspace_root / "06_Learning_Journal" / "evolution_log.json"
        self.log = self._load_log()

    def _load_log(self):
        """加载演进日志"""
        if self.evolution_file.exists():
            with open(self.evolution_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "milestones": [],
            "patterns_learned": [],
            "next_steps": []
        }

    def _save_log(self):
        """保存演进日志"""
        with open(self.evolution_file, 'w', encoding='utf-8') as f:
            json.dump(self.log, f, ensure_ascii=False, indent=2)

    def record_upgrade(self, title: str, description: str,
                      tools_affected: List[str],
                      patterns_used: List[str],
                      benefits: List[str]):
        """
        记录一次升级

        参数:
            title: 升级标题
            description: 详细描述
            tools_affected: 受影响的工具列表
            patterns_used: 使用的设计模式
            benefits: 带来的好处
        """
        milestone = {
            "date": datetime.now().isoformat(),
            "title": title,
            "description": description,
            "tools_affected": tools_affected,
            "patterns_used": patterns_used,
            "benefits": benefits
        }

        self.log['milestones'].append(milestone)
        self._save_log()

        print(f"[记录] 演进里程碑: {title}")

    def learn_pattern(self, pattern_name: str, description: str,
                     source: str, use_cases: List[str]):
        """
        记录学到的模式

        参数:
            pattern_name: 模式名称
            description: 描述
            source: 来源 (如 "AutoGen", "LangGraph")
            use_cases: 使用场景
        """
        pattern = {
            "name": pattern_name,
            "description": description,
            "source": source,
            "learned": datetime.now().isoformat(),
            "use_cases": use_cases
        }

        # 避免重复
        if not any(p['name'] == pattern_name for p in self.log['patterns_learned']):
            self.log['patterns_learned'].append(pattern)
            self._save_log()
            print(f"[学习] 模式: {pattern_name}")

    def plan_next_step(self, title: str, priority: str,
                      description: str, dependencies: List[str] = None):
        """
        规划下一步演进

        参数:
            title: 标题
            priority: 优先级 (high/medium/low)
            description: 描述
            dependencies: 依赖的其他任务
        """
        step = {
            "title": title,
            "priority": priority,
            "description": description,
            "dependencies": dependencies or [],
            "status": "planned",
            "created": datetime.now().isoformat()
        }

        self.log['next_steps'].append(step)
        self._save_log()

        print(f"[规划] 下一步: {title} (优先级: {priority})")

    def export_evolution_report(self, output_file: Path = None):
        """导出演进报告"""
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.workspace_root / "06_Learning_Journal" / f"evolution_report_{timestamp}.md"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Office Agent 演进报告\n\n")
            f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            # 里程碑
            f.write("## 演进里程碑\n\n")
            for milestone in reversed(self.log['milestones']):
                f.write(f"### {milestone['title']}\n")
                f.write(f"**时间**: {milestone['date']}\n\n")
                f.write(f"{milestone['description']}\n\n")

                if milestone.get('tools_affected'):
                    f.write("**受影响工具**: ")
                    f.write(", ".join(milestone['tools_affected']))
                    f.write("\n\n")

                if milestone.get('patterns_used'):
                    f.write("**使用模式**: ")
                    f.write(", ".join(milestone['patterns_used']))
                    f.write("\n\n")

                if milestone.get('benefits'):
                    f.write("**带来的好处**:\n")
                    for benefit in milestone['benefits']:
                        f.write(f"- {benefit}\n")
                    f.write("\n")

            # 学到的模式
            f.write("## 学到的设计模式\n\n")
            for pattern in self.log['patterns_learned']:
                f.write(f"### {pattern['name']} (来源: {pattern['source']})\n")
                f.write(f"{pattern['description']}\n\n")
                f.write("**使用场景**:\n")
                for use_case in pattern['use_cases']:
                    f.write(f"- {use_case}\n")
                f.write("\n")

            # 下一步
            f.write("## 下一步计划\n\n")
            for step in self.log['next_steps']:
                if step['status'] == 'planned':
                    priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(step['priority'], "")
                    f.write(f"### {priority_icon} {step['title']}\n")
                    f.write(f"- **优先级**: {step['priority']}\n")
                    f.write(f"- **描述**: {step['description']}\n")
                    if step.get('dependencies'):
                        f.write(f"- **依赖**: {', '.join(step['dependencies'])}\n")
                    f.write("\n")

        print(f"[报告] 已导出到: {output_file}")


# ============ 初始化系统 ============

def initialize_evolution_system():
    """初始化演进系统，记录初始状态"""

    vm = VersionManager()
    et = EvolutionTracker()

    # 注册现有工具
    vm.register_tool(
        "file_organizer",
        version="1.0.0",
        file_path="01_Active_Projects/file_organizer/file_organizer.py",
        api_version="1.0",
        description="证照材料智能整理工具",
        dependencies=[]
    )

    vm.register_tool(
        "market_supervision_agent",
        version="3.0.0",
        file_path="01_Active_Projects/market_supervision_agent/jinja2_filler.py",
        api_version="3.0",
        description="市场监管申请书生成工具 (Jinja2模板版)",
        dependencies=[]
    )

    vm.register_tool(
        "memory_agent",
        version="1.0.0",
        file_path="01_Active_Projects/memory_agent/memory_agent.py",
        api_version="1.0",
        description="学习记忆助手",
        dependencies=[]
    )

    # 记录最新升级 (2026-01-12)
    et.record_upgrade(
        title="基于 zread 调研的全面升级",
        description="""
        基于 zread 对顶级开源项目的调研，实施了三大核心技术:

        1. **AutoGen AgentTool 模式**
           - 创建工具互操作框架
           - 实现工具注册表
           - 支持工具相互调用

        2. **LangGraph 状态管理**
           - 创建工作流引擎
           - 实现节点和边系统
           - 支持条件分支

        3. **AutoGen Studio GUI**
           - 创建统一 Streamlit 界面
           - 实现工具状态监控
           - 提供工作流可视化
        """,
        tools_affected=[
            "file_organizer",
            "market_supervision_agent",
            "memory_agent",
            "agent_toolkit",
            "workflow_engine",
            "office_agent_studio"
        ],
        patterns_used=[
            "AgentTool Pattern",
            "State Management",
            "Graph-based Workflow",
            "Unified GUI",
            "Version Management"
        ],
        benefits=[
            "工具可以相互调用和协作",
            "复杂流程有清晰的状态管理",
            "统一的用户界面",
            "完整的版本控制和回滚能力",
            "向后兼容，旧功能继续可用"
        ]
    )

    # 记录学到的模式
    et.learn_pattern(
        pattern_name="AgentTool Pattern",
        description="工具可以作为其他工具的组件被调用，实现工具间的互操作性",
        source="Microsoft AutoGen",
        use_cases=[
            "file_organizer 可以被 application_generator 调用",
            "memory_agent 可以作为所有工具的共享知识库",
            "工具注册表统一管理所有工具"
        ]
    )

    et.learn_pattern(
        pattern_name="State-based Workflow",
        description="使用状态机和图式架构管理复杂流程，每个节点更新状态",
        source="LangGraph",
        use_cases=[
            "申请书生成: 验证→选择模板→生成→审查",
            "文件整理: 扫描→识别→移动→报告",
            "支持条件分支和循环"
        ]
    )

    et.learn_pattern(
        pattern_name="Version Compatibility",
        description="新版本不删除旧代码，而是添加新功能，保持旧API可用",
        source="Best Practice",
        use_cases=[
            "所有工具保持向后兼容",
            "提供API包装层",
            "配置文件自动迁移",
            "升级前自动备份"
        ]
    )

    # 规划下一步
    et.plan_next_step(
        title="工具间实际通信",
        priority="high",
        description="让 file_organizer、application_generator、memory_agent 真正相互调用",
        dependencies=["agent_toolkit", "workflow_engine"]
    )

    et.plan_next_step(
        title="自定义工作流编辑器",
        priority="medium",
        description="在 GUI 中添加可视化工作流编辑器",
        dependencies=["office_agent_studio"]
    )

    # 导出报告
    print("\n" + "=" * 70)
    print("初始化完成")
    print("=" * 70)

    vm.export_report()
    et.export_evolution_report()

    return vm, et


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════╗
║          Office Agent 演进系统初始化                           ║
║                                                                  ║
║  确保代码的连贯性、向后兼容和渐进式升级                         ║
╚══════════════════════════════════════════════════════════════════╝
    """)

    vm, et = initialize_evolution_system()

    print("\n" + "=" * 70)
    print("已注册工具:")
    print("=" * 70)
    vm.list_all_tools()

    print("\n" + "=" * 70)
    print("演进里程碑:")
    print("=" * 70)
    for milestone in et.log['milestones']:
        print(f"\n{milestone['title']}")
        print(f"  时间: {milestone['date'][:10]}")
        print(f"  工具: {', '.join(milestone['tools_affected'])}")

    print("\n" + "=" * 70)
    print("下一步计划:")
    print("=" * 70)
    for step in et.log['next_steps']:
        if step['status'] == 'planned':
            priority_symbols = {"high": "[高]", "medium": "[中]", "low": "[低]"}
            priority_symbol = priority_symbols.get(step['priority'], "")
            print(f"\n{priority_symbol} {step['title']}")
            print(f"   {step['description']}")
