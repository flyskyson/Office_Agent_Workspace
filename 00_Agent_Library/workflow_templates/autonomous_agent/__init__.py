"""
自主代理工作流模板

核心理念: "有多大责任,就有多大的权利"

版本: v1.0
创建日期: 2026-01-15
"""

__version__ = "1.0.0"
__author__ = "总代理 (AI)"

# 暂时注释掉未实现的模块
# from .template import AutonomousAgentWorkflow
# from .chief_agent import ChiefAgent
# from .sub_agent import SubAgent
from .tools_registry import ToolsRegistry
from .config import ProjectConfig
from .checkpoint_manager import WorkflowCheckpointManager
from .workflow_visualizer import AutonomousWorkflowVisualizer

__all__ = [
    # "AutonomousAgentWorkflow",
    # "ChiefAgent",
    # "SubAgent",
    "ToolsRegistry",
    "ProjectConfig",
    "WorkflowCheckpointManager",
    "AutonomousWorkflowVisualizer",
]
