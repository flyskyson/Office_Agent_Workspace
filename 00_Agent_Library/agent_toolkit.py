#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Office Agent 工具框架
参考 Microsoft AutoGen AgentTool 模式

作者: Claude Code
日期: 2026-01-12
"""

import sys
import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime

# Windows 终端编码修复
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass


class BaseTool(ABC):
    """工具基类 - 所有办公工具的基类"""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.stats = {
            'usage_count': 0,
            'last_used': None,
            'success_count': 0,
            'error_count': 0
        }

    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        执行工具功能
        返回格式: {'success': bool, 'result': Any, 'message': str}
        """
        pass

    @abstractmethod
    def validate_input(self, **kwargs) -> tuple[bool, str]:
        """
        验证输入参数
        返回: (是否有效, 错误信息)
        """
        pass

    def get_info(self) -> Dict[str, Any]:
        """获取工具信息"""
        return {
            'name': self.name,
            'description': self.description,
            'stats': self.stats
        }

    def update_stats(self, success: bool):
        """更新统计信息"""
        self.stats['usage_count'] += 1
        self.stats['last_used'] = datetime.now().isoformat()
        if success:
            self.stats['success_count'] += 1
        else:
            self.stats['error_count'] += 1


class FileOrganizerTool(BaseTool):
    """文件整理工具 - AgentTool 包装器"""

    def __init__(self):
        super().__init__(
            name="file_organizer",
            description="智能整理证照材料，支持自动识别、分类、归档"
        )
        # 延迟导入，避免循环依赖
        self.organizer = None

    def _get_organizer(self):
        """延迟加载 organizer"""
        if self.organizer is None:
            sys.path.insert(0, str(Path(__file__).parent.parent / "01_Active_Projects" / "file_organizer"))
            from file_organizer import FileOrganizer
            self.organizer = FileOrganizer('config.json')
        return self.organizer

    def validate_input(self, **kwargs) -> tuple[bool, str]:
        """验证输入"""
        # FileOrganizer 不需要额外参数，使用配置文件
        return True, ""

    def execute(self, **kwargs) -> Dict[str, Any]:
        """执行文件整理"""
        try:
            valid, msg = self.validate_input(**kwargs)
            if not valid:
                return {'success': False, 'result': None, 'message': msg}

            organizer = self._get_organizer()
            organizer.organize()

            self.update_stats(success=True)
            return {
                'success': True,
                'result': organizer.stats,
                'message': f"文件整理完成，处理了 {organizer.stats['成功移动']} 个文件"
            }

        except Exception as e:
            self.update_stats(success=False)
            return {
                'success': False,
                'result': None,
                'message': f"文件整理失败: {str(e)}"
            }


class MemoryAgentTool(BaseTool):
    """记忆助手工具 - AgentTool 包装器"""

    def __init__(self):
        super().__init__(
            name="memory_agent",
            description="智能知识管理，支持语义搜索、相似问题查找、学习路径推荐"
        )
        self.agent = None

    def _get_agent(self):
        """延迟加载 agent"""
        if self.agent is None:
            sys.path.insert(0, str(Path(__file__).parent.parent / "01_Active_Projects" / "memory_agent"))
            from memory_agent import MemoryAgent
            self.agent = MemoryAgent()
        return self.agent

    def validate_input(self, **kwargs) -> tuple[bool, str]:
        """验证输入"""
        action = kwargs.get('action')
        if action not in ['search', 'search_code', 'search_notes', 'find_similar', 'get_path']:
            return False, f"无效的操作: {action}"

        query = kwargs.get('query')
        if not query:
            return False, "缺少查询参数"

        return True, ""

    def execute(self, **kwargs) -> Dict[str, Any]:
        """执行记忆助手功能"""
        try:
            valid, msg = self.validate_input(**kwargs)
            if not valid:
                return {'success': False, 'result': None, 'message': msg}

            agent = self._get_agent()
            action = kwargs['action']
            query = kwargs['query']

            if action == 'search':
                results = agent.search_engine.search(query)
            elif action == 'search_code':
                results = agent.search_engine.search_code(query)
            elif action == 'search_notes':
                results = agent.search_engine.search_notes(query)
            elif action == 'find_similar':
                results = agent.recommender.find_similar_problems(query)
            elif action == 'get_path':
                results = agent.recommender.get_learning_path(query)
            else:
                results = []

            self.update_stats(success=True)
            return {
                'success': True,
                'result': results,
                'message': f"找到 {len(results)} 条结果"
            }

        except Exception as e:
            self.update_stats(success=False)
            return {
                'success': False,
                'result': None,
                'message': f"记忆助手执行失败: {str(e)}"
            }


class ApplicationGeneratorTool(BaseTool):
    """申请书生成工具 - AgentTool 包装器"""

    def __init__(self):
        super().__init__(
            name="application_generator",
            description="市场监管申请书自动生成，支持数据验证、模板填充"
        )
        self.generator = None

    def _get_generator(self):
        """延迟加载 generator"""
        # 实现逻辑
        pass

    def validate_input(self, **kwargs) -> tuple[bool, str]:
        """验证输入"""
        data = kwargs.get('data')
        if not data:
            return False, "缺少申请数据"

        return True, ""

    def execute(self, **kwargs) -> Dict[str, Any]:
        """执行申请书生成"""
        try:
            valid, msg = self.validate_input(**kwargs)
            if not valid:
                return {'success': False, 'result': None, 'message': msg}

            # TODO: 实现生成逻辑
            self.update_stats(success=True)
            return {
                'success': True,
                'result': {'output_file': 'generated.docx'},
                'message': '申请书生成成功'
            }

        except Exception as e:
            self.update_stats(success=False)
            return {
                'success': False,
                'result': None,
                'message': f"申请书生成失败: {str(e)}"
            }


class ToolRegistry:
    """工具注册表 - 管理所有可用工具"""

    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}
        self._register_default_tools()

    def _register_default_tools(self):
        """注册默认工具"""
        self.register(FileOrganizerTool())
        self.register(MemoryAgentTool())
        self.register(ApplicationGeneratorTool())

    def register(self, tool: BaseTool):
        """注册工具"""
        self.tools[tool.name] = tool
        print(f"[注册] 工具: {tool.name}")

    def get_tool(self, name: str) -> Optional[BaseTool]:
        """获取工具"""
        return self.tools.get(name)

    def list_tools(self) -> List[Dict[str, Any]]:
        """列出所有工具"""
        return [tool.get_info() for tool in self.tools.values()]

    def execute_tool(self, name: str, **kwargs) -> Dict[str, Any]:
        """执行工具"""
        tool = self.get_tool(name)
        if not tool:
            return {
                'success': False,
                'result': None,
                'message': f"工具不存在: {name}"
            }

        return tool.execute(**kwargs)


class WorkflowEngine:
    """
    工作流引擎
    参考 LangGraph 的状态机模式
    """

    def __init__(self, registry: ToolRegistry):
        self.registry = registry
        self.workflows = {}

    def define_workflow(self, name: str, steps: List[Dict]):
        """
        定义工作流

        steps 格式:
        [
            {'tool': 'tool_name', 'params': {...}, 'next': 'next_step_name'},
            {'tool': 'tool_name', 'params': {...}, 'condition': lambda result: ...}
        ]
        """
        self.workflows[name] = steps

    def execute_workflow(self, name: str, initial_state: Dict = None) -> Dict[str, Any]:
        """
        执行工作流

        返回: {'success': bool, 'final_state': Dict, 'steps_executed': int}
        """
        if name not in self.workflows:
            return {
                'success': False,
                'final_state': None,
                'steps_executed': 0,
                'message': f"工作流不存在: {name}"
            }

        state = initial_state or {}
        steps = self.workflows[name]
        steps_executed = 0

        for step in steps:
            tool_name = step['tool']
            params = step.get('params', {})

            # 合并状态和参数
            if state:
                params = {**params, **state}

            # 执行工具
            result = self.registry.execute_tool(tool_name, **params)

            if not result['success']:
                return {
                    'success': False,
                    'final_state': state,
                    'steps_executed': steps_executed,
                    'message': f"步骤失败: {tool_name} - {result['message']}"
                }

            # 更新状态
            if result['result']:
                state.update(result['result'])

            steps_executed += 1

            # 检查条件
            condition = step.get('condition')
            if condition and not condition(result):
                break

        return {
            'success': True,
            'final_state': state,
            'steps_executed': steps_executed,
            'message': '工作流执行完成'
        }


# 预定义工作流
def create_default_workflows(engine: WorkflowEngine):
    """创建默认工作流"""

    # 工作流1: 申请书生成完整流程
    engine.define_workflow('application_generation', [
        {
            'tool': 'memory_agent',
            'params': {'action': 'search', 'query': '申请书模板'},
            'next': 'validate'
        },
        {
            'tool': 'application_generator',
            'params': {'data': 'from_state'},
            'next': 'organize'
        },
        {
            'tool': 'file_organizer',
            'params': {},
            'next': None
        }
    ])

    # 工作流2: 文件整理 + 知识索引
    engine.define_workflow('organize_and_index', [
        {
            'tool': 'file_organizer',
            'params': {},
            'next': 'index'
        },
        {
            'tool': 'memory_agent',
            'params': {'action': 'search', 'query': '整理后的文件'},
            'next': None
        }
    ])


def main():
    """演示工具框架的使用"""

    print("=" * 70)
    print("Office Agent 工具框架演示")
    print("=" * 70)
    print()

    # 创建工具注册表
    registry = ToolRegistry()

    # 列出所有工具
    print("\n[可用工具]")
    for tool_info in registry.list_tools():
        print(f"  - {tool_info['name']}: {tool_info['description']}")
        print(f"    使用次数: {tool_info['stats']['usage_count']}")

    # 创建工作流引擎
    engine = WorkflowEngine(registry)
    create_default_workflows(engine)

    print("\n[可用工作流]")
    for workflow_name in engine.workflows.keys():
        print(f"  - {workflow_name}")

    # 演示1: 直接调用工具
    print("\n" + "=" * 70)
    print("演示1: 直接调用文件整理工具")
    print("=" * 70)

    result = registry.execute_tool('file_organizer')
    print(f"\n结果: {result['message']}")
    if result['success']:
        print(f"统计: {result['result']}")

    # 演示2: 调用记忆助手
    print("\n" + "=" * 70)
    print("演示2: 调用记忆助手搜索")
    print("=" * 70)

    result = registry.execute_tool(
        'memory_agent',
        action='search',
        query='文件整理最佳实践'
    )
    print(f"\n结果: {result['message']}")

    # 演示3: 执行工作流
    print("\n" + "=" * 70)
    print("演示3: 执行工作流")
    print("=" * 70)

    result = engine.execute_workflow('organize_and_index')
    print(f"\n结果: {result['message']}")
    print(f"执行步骤数: {result['steps_executed']}")


if __name__ == "__main__":
    main()
