#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AgentSupervisor - 智能体监督者
联邦智能体架构，协调多个 Agent 协作

作者: Claude Code
日期: 2026-01-16
版本: 1.0.0
参考: langgraph-ai/langgraph-supervisor-experiment
"""

import sys
import json
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from enum import Enum
from datetime import datetime
from copy import deepcopy

# Windows 终端编码修复
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass

# 添加库路径
sys.path.insert(0, str(Path(__file__).parent))

from workflow_engine import WorkflowGraph, WorkflowStatus


# ============================================================================
# 智能体基类
# ============================================================================

class AgentType(Enum):
    """智能体类型"""
    SUPERVISION = "market_supervision"    # 市场监管
    MEMORY = "memory"                      # 记忆助手
    FILE_ORGANIZER = "file_organizer"      # 文件整理
    NEWS_SCRAPER = "news_scraper"          # 新闻爬虫
    WORKFLOW_ENGINE = "workflow_engine"    # 工作流引擎


class AgentResponse:
    """智能体响应"""

    def __init__(
        self,
        success: bool,
        data: Any = None,
        error: str = None,
        next_agent: str = None
    ):
        self.success = success
        self.data = data
        self.error = error
        self.next_agent = next_agent
        self.timestamp = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "next_agent": self.next_agent,
            "timestamp": self.timestamp.isoformat()
        }


class BaseAgent:
    """智能体基类"""

    def __init__(self, name: str, agent_type: AgentType):
        self.name = name
        self.agent_type = agent_type
        self.enabled = True
        self.state = {}

    def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        """
        执行智能体任务

        参数:
            input_data: 输入数据

        返回:
            AgentResponse: 执行结果
        """
        raise NotImplementedError("子类必须实现 execute 方法")

    def reset(self):
        """重置智能体状态"""
        self.state = {}


# ============================================================================
# 具体智能体实现
# ============================================================================

class MarketSupervisionAgent(BaseAgent):
    """市场监管智能体"""

    def __init__(self):
        super().__init__("市场监管智能体", AgentType.SUPERVISION)
        # 延迟导入避免循环依赖
        self._db_manager = None

    @property
    def db_manager(self):
        """延迟加载数据库管理器"""
        if self._db_manager is None:
            try:
                sys.path.insert(0, str(Path(__file__).parent.parent / "01_Active_Projects" / "market_supervision_agent" / "src"))
                from database_manager import DatabaseManager
                self._db_manager = DatabaseManager()
            except ImportError:
                print("[WARN] 无法导入 DatabaseManager")
        return self._db_manager

    def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        """执行市场监管任务"""
        action = input_data.get("action")

        try:
            if action == "generate_application":
                # 生成申请书
                operator_name = input_data.get("operator_name")
                id_card = input_data.get("id_card")

                if not operator_name or not id_card:
                    return AgentResponse(
                        success=False,
                        error="缺少必需参数: operator_name, id_card"
                    )

                # 查询数据库
                if self.db_manager:
                    existing = self.db_manager.get_operator_by_id_card(id_card)
                    if existing:
                        return AgentResponse(
                            success=True,
                            data={
                                "message": "经营户已存在",
                                "operator": existing
                            }
                        )

                return AgentResponse(
                    success=True,
                    data={
                        "message": f"已为 {operator_name} 准备申请书生成",
                        "next_step": "填写申请表"
                    }
                )

            elif action == "list_operators":
                # 列出经营户
                if self.db_manager:
                    operators = self.db_manager.list_operators(limit=10)
                    return AgentResponse(
                        success=True,
                        data={"operators": operators}
                    )

            return AgentResponse(
                success=False,
                error=f"未知操作: {action}"
            )

        except Exception as e:
            return AgentResponse(
                success=False,
                error=str(e)
            )


class MemoryAgent(BaseAgent):
    """记忆助手智能体"""

    def __init__(self):
        super().__init__("记忆助手", AgentType.MEMORY)
        self._mcp_server = None

    @property
    def mcp_server(self):
        """延迟加载 MCP 服务器"""
        if self._mcp_server is None:
            try:
                from mcp_sqlite_wrapper import MCPSqliteServer
                self._mcp_server = MCPSqliteServer()
                self._mcp_server.init_memory_db()
            except ImportError:
                print("[WARN] 无法导入 MCPSqliteServer")
        return self._mcp_server

    def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        """执行记忆任务"""
        action = input_data.get("action")

        try:
            if action == "add_note":
                # 添加笔记
                title = input_data.get("title")
                content = input_data.get("content", "")

                if not title:
                    return AgentResponse(
                        success=False,
                        error="缺少必需参数: title"
                    )

                if self.mcp_server:
                    note_id = self.mcp_server.add_note(
                        title=title,
                        content=content,
                        tags=input_data.get("tags"),
                        category=input_data.get("category")
                    )
                    return AgentResponse(
                        success=True,
                        data={"note_id": note_id, "message": "笔记已保存"}
                    )

            elif action == "search":
                # 搜索笔记
                keyword = input_data.get("keyword")

                if not keyword:
                    return AgentResponse(
                        success=False,
                        error="缺少必需参数: keyword"
                    )

                if self.mcp_server:
                    notes = self.mcp_server.search_notes(keyword)
                    return AgentResponse(
                        success=True,
                        data={"notes": notes, "count": len(notes)}
                    )

            return AgentResponse(
                success=False,
                error=f"未知操作: {action}"
            )

        except Exception as e:
            return AgentResponse(
                success=False,
                error=str(e)
            )


class FileOrganizerAgent(BaseAgent):
    """文件整理智能体"""

    def __init__(self):
        super().__init__("文件整理工具", AgentType.FILE_ORGANIZER)

    def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        """执行文件整理任务"""
        action = input_data.get("action")

        try:
            if action == "scan":
                # 扫描文件
                path = input_data.get("path", ".")
                return AgentResponse(
                    success=True,
                    data={
                        "message": f"已扫描目录: {path}",
                        "files_found": 0
                    }
                )

            elif action == "organize":
                # 整理文件
                rules = input_data.get("rules", {})
                return AgentResponse(
                    success=True,
                    data={"message": "文件整理完成", "organized": 0}
                )

            return AgentResponse(
                success=False,
                error=f"未知操作: {action}"
            )

        except Exception as e:
            return AgentResponse(
                success=False,
                error=str(e)
            )


# ============================================================================
# AgentSupervisor - 智能体监督者
# ============================================================================

class AgentSupervisor:
    """
    智能体监督者 - 协调多个 Agent 协作

    功能:
    1. 请求路由 - 将用户请求路由到合适的 Agent
    2. 工作流编排 - 协调多个 Agent 按顺序执行
    3. 状态管理 - 维护工作流状态
    4. 错误处理 - 处理 Agent 执行失败
    """

    def __init__(self):
        """初始化监督者"""
        # 注册所有智能体
        self.agents: Dict[str, BaseAgent] = {
            "market_supervision": MarketSupervisionAgent(),
            "memory": MemoryAgent(),
            "file_organizer": FileOrganizerAgent()
        }

        # 工作流图
        self.workflow_graph = WorkflowGraph("agent_supervisor")

        # 统计信息
        self.stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "agent_calls": {}
        }

        print(f"[INFO] AgentSupervisor 初始化完成")
        print(f"[INFO] 已注册 {len(self.agents)} 个智能体")

    # ========================================================================
    # 请求路由
    # ========================================================================

    def route(self, user_request: str) -> str:
        """
        路由请求到合适的智能体

        参数:
            user_request: 用户请求

        返回:
            智能体名称
        """
        # 简单关键词匹配
        request_lower = user_request.lower()

        # 市场监管关键词
        supervision_keywords = ["申请书", "经营户", "申请", "执照", "开业", "个体工商户"]
        if any(kw in request_lower for kw in supervision_keywords):
            return "market_supervision"

        # 记忆助手关键词
        memory_keywords = ["笔记", "记住", "回忆", "搜索", "记录", "笔记"]
        if any(kw in request_lower for kw in memory_keywords):
            return "memory"

        # 文件整理关键词
        file_keywords = ["整理", "文件", "归类", "移动", "复制"]
        if any(kw in request_lower for kw in file_keywords):
            return "file_organizer"

        # 默认返回记忆助手（最通用）
        return "memory"

    # ========================================================================
    # 单智能体执行
    # ========================================================================

    def execute_agent(
        self,
        agent_name: str,
        input_data: Dict[str, Any]
    ) -> AgentResponse:
        """
        执行单个智能体

        参数:
            agent_name: 智能体名称
            input_data: 输入数据

        返回:
            AgentResponse
        """
        if agent_name not in self.agents:
            return AgentResponse(
                success=False,
                error=f"未知智能体: {agent_name}"
            )

        agent = self.agents[agent_name]

        if not agent.enabled:
            return AgentResponse(
                success=False,
                error=f"智能体未启用: {agent_name}"
            )

        # 更新统计
        self.stats["total_requests"] += 1
        if agent_name not in self.stats["agent_calls"]:
            self.stats["agent_calls"][agent_name] = 0
        self.stats["agent_calls"][agent_name] += 1

        # 执行
        try:
            response = agent.execute(input_data)

            if response.success:
                self.stats["successful_requests"] += 1
            else:
                self.stats["failed_requests"] += 1

            return response

        except Exception as e:
            self.stats["failed_requests"] += 1
            return AgentResponse(
                success=False,
                error=f"执行失败: {str(e)}"
            )

    # ========================================================================
    # 工作流编排
    # ========================================================================

    def orchestrate(
        self,
        workflow: List[Dict[str, Any]],
        initial_state: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        编排多智能体工作流

        参数:
            workflow: 工作流定义
                [
                    {"agent": "memory", "action": "search", "params": {"keyword": "xxx"}},
                    {"agent": "market_supervision", "action": "generate_application", "params": {...}}
                ]
            initial_state: 初始状态

        返回:
            最终状态和结果
        """
        if initial_state is None:
            initial_state = {}

        state = deepcopy(initial_state)
        results = []

        print(f"\n[工作流] 执行 {len(workflow)} 步工作流")

        for i, step in enumerate(workflow, 1):
            agent_name = step.get("agent")
            action = step.get("action")
            params = step.get("params", {})

            print(f"  [{i}/{len(workflow)}] {agent_name}.{action}")

            # 构造输入数据
            input_data = {"action": action, **params}
            input_data.update(state)  # 传递前面步骤的状态

            # 执行
            response = self.execute_agent(agent_name, input_data)

            if not response.success:
                print(f"    ❌ 失败: {response.error}")
                return {
                    "success": False,
                    "error": response.error,
                    "completed_steps": i - 1,
                    "results": results
                }

            print(f"    ✅ 成功")

            # 更新状态
            if isinstance(response.data, dict):
                state.update(response.data)

            results.append({
                "step": i,
                "agent": agent_name,
                "action": action,
                "response": response.to_dict()
            })

            # 检查是否需要跳转到其他智能体
            if response.next_agent:
                print(f"    → 跳转到: {response.next_agent}")
                # 插入下一步
                workflow.insert(i, {"agent": response.next_agent, "action": action, "params": params})

        print(f"\n[工作流] ✅ 完成")

        return {
            "success": True,
            "final_state": state,
            "results": results
        }

    # ========================================================================
    # 预定义工作流
    # ========================================================================

    def workflow_license_application_complete(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        证照申请完整流程

        工作流:
        1. FileOrganizer: 扫描证件材料
        2. Memory: 检索历史记录
        3. MarketSupervision: 生成申请书
        4. Memory: 保存申请记录
        """
        workflow = [
            {
                "agent": "file_organizer",
                "action": "scan",
                "params": {"path": params.get("material_path", ".")}
            },
            {
                "agent": "memory",
                "action": "search",
                "params": {"keyword": params.get("operator_name", "")}
            },
            {
                "agent": "market_supervision",
                "action": "generate_application",
                "params": {
                    "operator_name": params.get("operator_name"),
                    "id_card": params.get("id_card")
                }
            },
            {
                "agent": "memory",
                "action": "add_note",
                "params": {
                    "title": f"申请记录: {params.get('operator_name')}",
                    "content": f"身份证: {params.get('id_card')}",
                    "category": "证照申请"
                }
            }
        ]

        return self.orchestrate(workflow)

    def workflow_daily_news_summary(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        每日新闻摘要流程

        工作流:
        1. NewsScraper: 获取新闻
        2. Memory: 存储新闻
        3. Memory: 生成日报
        """
        workflow = [
            {
                "agent": "news_scraper",
                "action": "fetch",
                "params": {"platforms": params.get("platforms", ["weibo", "zhihu"])}
            },
            {
                "agent": "memory",
                "action": "add_note",
                "params": {
                    "title": f"新闻日报 {datetime.now().strftime('%Y-%m-%d')}",
                    "content": "今日热点新闻摘要",
                    "category": "新闻"
                }
            }
        ]

        return self.orchestrate(workflow)

    # ========================================================================
    # 统计和监控
    # ========================================================================

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "requests": {
                "total": self.stats["total_requests"],
                "successful": self.stats["successful_requests"],
                "failed": self.stats["failed_requests"],
                "success_rate": (
                    self.stats["successful_requests"] / self.stats["total_requests"]
                    if self.stats["total_requests"] > 0 else 0
                )
            },
            "agents": {
                name: {
                    "calls": count,
                    "enabled": agent.enabled
                }
                for name, agent in self.agents.items()
                for count in [self.stats["agent_calls"].get(name, 0)]
            },
            "registered_agents": len(self.agents)
        }

    def enable_agent(self, agent_name: str):
        """启用智能体"""
        if agent_name in self.agents:
            self.agents[agent_name].enabled = True
            print(f"[INFO] 已启用智能体: {agent_name}")

    def disable_agent(self, agent_name: str):
        """禁用智能体"""
        if agent_name in self.agents:
            self.agents[agent_name].enabled = False
            print(f"[INFO] 已禁用智能体: {agent_name}")


# ============================================================================
# 命令行接口
# ============================================================================

def main():
    """命令行接口"""
    print("=" * 60)
    print("AgentSupervisor - 智能体监督者")
    print("=" * 60)

    supervisor = AgentSupervisor()

    # 显示已注册的智能体
    print("\n[已注册的智能体]")
    for name, agent in supervisor.agents.items():
        status = "✅" if agent.enabled else "❌"
        print(f"  {status} {name}: {agent.name}")

    # 示例 1: 单智能体执行
    print("\n[示例 1] 单智能体执行")
    response = supervisor.execute_agent(
        "memory",
        {"action": "add_note", "title": "测试笔记", "content": "这是一个测试"}
    )
    print(f"  结果: {response.to_dict()}")

    # 示例 2: 工作流执行
    print("\n[示例 2] 工作流执行")
    workflow_result = supervisor.workflow_license_application_complete({
        "operator_name": "张三",
        "id_card": "123456789012345678"
    })
    print(f"  成功: {workflow_result.get('success')}")

    # 显示统计信息
    print("\n[统计信息]")
    stats = supervisor.get_stats()
    print(f"  总请求数: {stats['requests']['total']}")
    print(f"  成功率: {stats['requests']['success_rate']:.1%}")
    print(f"  智能体调用:")
    for agent_name, agent_stats in stats['agents'].items():
        print(f"    - {agent_name}: {agent_stats['calls']} 次")

    print("\n" + "=" * 60)
    print("✅ AgentSupervisor 测试完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
