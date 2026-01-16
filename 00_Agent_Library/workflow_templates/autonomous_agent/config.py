"""
项目配置管理

加载、验证和管理项目配置
"""

import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class MilestoneConfig:
    """暂停点配置"""
    point: str
    description: str
    require_confirmation: bool
    trigger_condition: str


@dataclass
class BudgetConfig:
    """预算配置"""
    resources: Dict[str, Any] = field(default_factory=dict)
    limits: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NodeConfig:
    """节点配置"""
    id: str
    name: str
    agent: str
    role: str
    purpose: str
    tasks: List[str] = field(default_factory=list)
    steps: List[str] = field(default_factory=list)
    requirements: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)


@dataclass
class ToolsRegistryConfig:
    """工具注册表配置"""
    path: str
    registry_file: str


@dataclass
class LoggingConfig:
    """日志配置"""
    level: str = "INFO"
    output: str = "project/logs/"


@dataclass
class ProjectConfig:
    """项目配置"""
    name: str
    version: str
    goal: str
    description: str = ""
    milestones: List[MilestoneConfig] = field(default_factory=list)
    budget: BudgetConfig = field(default_factory=BudgetConfig)
    nodes: List[NodeConfig] = field(default_factory=list)
    tools_registry: Optional[ToolsRegistryConfig] = None
    logging: LoggingConfig = field(default_factory=LoggingConfig)

    @classmethod
    def from_yaml(cls, config_path: str) -> "ProjectConfig":
        """从YAML文件加载配置"""
        config_file = Path(config_path)
        if not config_file.exists():
            raise FileNotFoundError(f"配置文件不存在: {config_path}")

        with open(config_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        # 解析项目基本信息
        project_data = data.get("project", {})
        milestones_data = data.get("milestones", [])
        budget_data = data.get("budget", {})
        nodes_data = data.get("nodes", [])
        tools_registry_data = data.get("tools_registry", {})
        logging_data = data.get("logging", {})

        # 解析暂停点
        milestones = [
            MilestoneConfig(
                point=m.get("point", ""),
                description=m.get("description", ""),
                require_confirmation=m.get("require_confirmation", False),
                trigger_condition=m.get("trigger_condition", "")
            )
            for m in milestones_data
        ]

        # 解析预算
        budget = BudgetConfig(
            resources=budget_data.get("resources", {}),
            limits=budget_data.get("limits", {})
        )

        # 解析节点
        nodes = [
            NodeConfig(
                id=n.get("id", ""),
                name=n.get("name", ""),
                agent=n.get("agent", ""),
                role=n.get("role", ""),
                purpose=n.get("purpose", ""),
                tasks=n.get("tasks", []),
                steps=n.get("steps", []),
                requirements=n.get("requirements", []),
                constraints=n.get("constraints", [])
            )
            for n in nodes_data
        ]

        # 解析工具注册表
        tools_registry = None
        if tools_registry_data:
            tools_registry = ToolsRegistryConfig(
                path=tools_registry_data.get("path", ""),
                registry_file=tools_registry_data.get("registry_file", "")
            )

        # 解析日志配置
        logging = LoggingConfig(
            level=logging_data.get("level", "INFO"),
            output=logging_data.get("output", "project/logs/")
        )

        return cls(
            name=project_data.get("name", ""),
            version=project_data.get("version", "1.0"),
            goal=project_data.get("goal", ""),
            description=project_data.get("description", ""),
            milestones=milestones,
            budget=budget,
            nodes=nodes,
            tools_registry=tools_registry,
            logging=logging
        )

    def validate(self) -> bool:
        """验证配置的有效性"""
        # 验证项目基本信息
        if not self.name:
            raise ValueError("项目名称不能为空")
        if not self.goal:
            raise ValueError("项目目标不能为空")

        # 验证节点
        if not self.nodes:
            raise ValueError("至少需要一个节点")

        node_ids = [node.id for node in self.nodes]
        if len(node_ids) != len(set(node_ids)):
            raise ValueError("节点ID必须唯一")

        # 验证暂停点
        valid_milestones = ["start", "30%", "70%", "pre_final"]
        for milestone in self.milestones:
            if milestone.point not in valid_milestones:
                raise ValueError(f"无效的暂停点: {milestone.point}")

        # 验证工具注册表配置
        if self.tools_registry:
            if not self.tools_registry.path:
                raise ValueError("工具路径不能为空")
            if not self.tools_registry.registry_file:
                raise ValueError("工具注册表文件不能为空")

        return True

    def get_node_by_id(self, node_id: str) -> Optional[NodeConfig]:
        """根据ID获取节点配置"""
        for node in self.nodes:
            if node.id == node_id:
                return node
        return None

    def get_milestone_by_point(self, point: str) -> Optional[MilestoneConfig]:
        """根据暂停点获取配置"""
        for milestone in self.milestones:
            if milestone.point == point:
                return milestone
        return None
