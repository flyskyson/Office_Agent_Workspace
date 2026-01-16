"""
自主代理工作流启动器

用法：
    python workflow_starter.py <project_config.yaml>
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from workflow_templates.autonomous_agent.config import ProjectConfig
from workflow_templates.autonomous_agent.tools_registry import ToolsRegistry


def create_project_workspace(project_name: str) -> Path:
    """创建项目工作空间"""
    base_dir = Path("05_Outputs/autonomous_agent_projects")
    project_dir = base_dir / project_name
    project_dir.mkdir(parents=True, exist_ok=True)

    # 创建子目录
    (project_dir / "logs").mkdir(exist_ok=True)
    (project_dir / "tools").mkdir(exist_ok=True)
    (project_dir / "outputs").mkdir(exist_ok=True)

    return project_dir


def generate_project_context(config: ProjectConfig, workspace: Path, registry: ToolsRegistry) -> dict:
    """生成项目上下文"""
    return {
        "project": {
            "name": config.name,
            "version": config.version,
            "goal": config.goal,
            "description": config.description,
            "nodes": [
                {
                    "id": node.id,
                    "name": node.name,
                    "role": node.role,
                    "purpose": node.purpose,
                    "tasks": node.tasks,
                    "requirements": node.requirements
                }
                for node in config.nodes
            ]
        },
        "milestones": [
            {
                "point": m.point,
                "description": m.description,
                "require_confirmation": m.require_confirmation,
                "trigger_condition": m.trigger_condition
            }
            for m in config.milestones
        ],
        "budget": {
            "resources": config.budget.resources,
            "limits": config.budget.limits
        },
        "tools_registry": {
            "path": config.tools_registry.path,
            "statistics": registry.get_statistics()
        },
        "workspace": str(workspace),
        "start_time": datetime.now().isoformat(),
        "status": "initialized"
    }


def main():
    if len(sys.argv) < 2:
        print("用法: python workflow_starter.py <project_config.yaml>")
        sys.exit(1)

    config_path = sys.argv[1]

    try:
        # 1. 加载配置
        print(f"📋 加载配置: {config_path}")
        config = ProjectConfig.from_yaml(config_path)
        config.validate()
        print(f"✅ 配置加载成功")
        print(f"   项目: {config.name}")
        print(f"   目标: {config.goal}")
        print(f"   节点数: {len(config.nodes)}")

        # 2. 初始化工具注册表
        print(f"\n🔧 初始化工具注册表...")
        registry_path = Path(config.tools_registry.registry_file)
        registry_path.parent.mkdir(parents=True, exist_ok=True)
        registry = ToolsRegistry(str(registry_path))
        stats = registry.get_statistics()
        print(f"✅ 工具注册表初始化成功")
        print(f"   已有工具: {stats['total_tools']}")

        # 3. 创建工作空间
        print(f"\n📁 创建工作空间...")
        workspace = create_project_workspace(config.name)
        print(f"✅ 工作空间创建成功: {workspace}")

        # 4. 生成项目上下文
        print(f"\n📝 生成项目上下文...")
        context = generate_project_context(config, workspace, registry)
        context_file = workspace / "project_context.json"
        with open(context_file, "w", encoding="utf-8") as f:
            json.dump(context, f, ensure_ascii=False, indent=2)
        print(f"✅ 项目上下文已生成: {context_file}")

        # 5. 生成初始状态
        print(f"\n📊 生成初始状态...")
        initial_state = {
            "project_name": config.name,
            "status": "ready",
            "current_node": None,
            "completed_nodes": [],
            "failed_nodes": [],
            "tools_created": [],
            "start_time": context["start_time"],
            "last_update": datetime.now().isoformat(),
            "budget_usage": {
                "success_rate": 1.0,
                "consecutive_failures": 0,
                "broken_tools": 0
            },
            "milestones_reached": []
        }
        state_file = workspace / "project_state.json"
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(initial_state, f, ensure_ascii=False, indent=2)
        print(f"✅ 初始状态已生成: {state_file}")

        # 6. 输出启动信息
        print(f"""
{'='*60}
        自主代理工作流已启动 🚀
{'='*60}

📋 项目信息
   名称: {config.name}
   版本: {config.version}
   目标: {config.goal}

📊 节点概览
   总节点数: {len(config.nodes)}
   节点列表:
""")
        for i, node in enumerate(config.nodes, 1):
            print(f"      {i}. {node.name} ({node.role})")

        print(f"""
🔧 工具信息
   注册表: {config.tools_registry.registry_file}
   已有工具: {stats['total_tools']}

📁 工作空间
   路径: {workspace}

{'='*60}
🎯 下一步操作
{'='*60}

1️⃣  阅读项目上下文
   cat {context_file}

2️⃣  启动 Claude Code，作为总代理执行项目
   - 阅读 project_context.json
   - 按照节点顺序执行
   - 实时更新 project_state.json

3️⃣  查看实时状态
   cat {state_file}

💡 提示：您现在可以告诉 Claude Code：
   "读取 {context_file}，作为总代理开始执行这个项目"

{'='*60}
        """)

    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
