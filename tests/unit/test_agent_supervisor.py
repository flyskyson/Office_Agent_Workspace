"""
AgentSupervisor 单元测试

测试智能体监督者的各项功能：
- 智能体注册
- 请求路由
- 工作流编排
- 状态管理
"""

import pytest
from datetime import datetime
from typing import Dict, Any

from 00_Agent_Library.agent_supervisor import (
    AgentSupervisor,
    AgentResponse,
    BaseAgent,
    AgentType,
    MarketSupervisionAgent,
    MemoryAgent,
    FileOrganizerAgent
)


# ================================
# Mock 智能体（用于测试）
# ================================

class MockAgent(BaseAgent):
    """模拟智能体"""

    def __init__(self, name: str = "mock_agent"):
        super().__init__(name, AgentType.MEMORY)
        self.call_count = 0

    def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        """执行（增加调用计数）"""
        self.call_count += 1
        return AgentResponse(
            success=True,
            data={"call_count": self.call_count},
            error=None
        )


class FailingAgent(BaseAgent):
    """总是失败的模拟智能体"""

    def __init__(self, name: str = "failing_agent"):
        super().__init__(name, AgentType.MEMORY)

    def execute(self, input_data: Dict[str, Any]) -> AgentResponse:
        """执行（总是失败）"""
        return AgentResponse(
            success=False,
            data=None,
            error="测试失败"
        )


# ================================
# 测试类定义
# ================================

class TestAgentResponse:
    """AgentResponse 测试"""

    @pytest.mark.unit
    def test_create_success_response(self):
        """测试创建成功响应"""
        response = AgentResponse(
            success=True,
            data={"result": 42}
        )

        assert response.success is True
        assert response.data == {"result": 42}
        assert response.error is None
        assert isinstance(response.timestamp, datetime)

    @pytest.mark.unit
    def test_create_error_response(self):
        """测试创建错误响应"""
        response = AgentResponse(
            success=False,
            error="出错了"
        )

        assert response.success is False
        assert response.data is None
        assert response.error == "出错了"


class TestAgentSupervisor:
    """AgentSupervisor 测试"""

    # ------------------------
    # 初始化测试
    # ------------------------

    @pytest.mark.unit
    def test_init(self):
        """测试初始化"""
        supervisor = AgentSupervisor()

        assert supervisor is not None
        assert len(supervisor.agents) > 0
        assert "market_supervision" in supervisor.agents
        assert "memory" in supervisor.agents
        assert "file_organizer" in supervisor.agents

    @pytest.mark.unit
    def test_init_with_custom_agents(self):
        """测试使用自定义智能体初始化"""
        custom_agent = MockAgent()
        supervisor = AgentSupervisor(agents=[custom_agent])

        assert "mock_agent" in supervisor.agents

    # ------------------------
    # 智能体注册测试
    # ------------------------

    @pytest.mark.unit
    def test_register_agent(self):
        """测试注册智能体"""
        supervisor = AgentSupervisor()
        mock_agent = MockAgent()

        initial_count = len(supervisor.agents)
        supervisor.register_agent(mock_agent)

        assert len(supervisor.agents) == initial_count + 1
        assert "mock_agent" in supervisor.agents

    @pytest.mark.unit
    def test_unregister_agent(self):
        """测试注销智能体"""
        supervisor = AgentSupervisor()

        # 验证智能体存在
        assert "memory" in supervisor.agents

        # 注销智能体
        supervisor.unregister_agent("memory")

        # 验证已注销
        assert "memory" not in supervisor.agents

    @pytest.mark.unit
    def test_enable_disable_agent(self):
        """测试启用/禁用智能体"""
        supervisor = AgentSupervisor()

        # 禁用智能体
        supervisor.disable_agent("memory")
        assert supervisor.agents["memory"].enabled is False

        # 启用智能体
        supervisor.enable_agent("memory")
        assert supervisor.agents["memory"].enabled is True

    # ------------------------
    # 请求路由测试
    # ------------------------

    @pytest.mark.unit
    @pytest.mark.parametrize("request_text,expected_agent", [
        ("帮我生成申请书", "market_supervision"),
        ("记住这个信息", "memory"),
        ("整理文件", "file_organizer"),
        ("我要申请个体工商户", "market_supervision"),
        ("添加笔记", "memory"),
    ])
    def test_route_requests(self, request_text: str, expected_agent: str):
        """参数化测试请求路由"""
        supervisor = AgentSupervisor()

        routed_agent = supervisor.route(request_text)

        assert routed_agent == expected_agent

    @pytest.mark.unit
    def test_route_unknown_request(self):
        """测试路由未知请求"""
        supervisor = AgentSupervisor()

        # 未知请求应该返回默认智能体
        routed = supervisor.route("我不知道说什么")
        assert routed is not None

    # ------------------------
    # 智能体执行测试
    # ------------------------

    @pytest.mark.unit
    def test_execute_agent_success(self):
        """测试成功执行智能体"""
        supervisor = AgentSupervisor()
        mock_agent = MockAgent()
        supervisor.register_agent(mock_agent)

        response = supervisor.execute_agent(
            "mock_agent",
            {"action": "test"}
        )

        assert response.success is True
        assert response.data["call_count"] == 1

    @pytest.mark.unit
    def test_execute_agent_failure(self):
        """测试执行失败的智能体"""
        supervisor = AgentSupervisor()
        failing_agent = FailingAgent()
        supervisor.register_agent(failing_agent)

        response = supervisor.execute_agent(
            "failing_agent",
            {"action": "test"}
        )

        assert response.success is False
        assert response.error == "测试失败"

    @pytest.mark.unit
    def test_execute_disabled_agent(self):
        """测试执行已禁用的智能体"""
        supervisor = AgentSupervisor()
        supervisor.disable_agent("memory")

        response = supervisor.execute_agent(
            "memory",
            {"action": "add_note"}
        )

        assert response.success is False
        assert "禁用" in response.error or "disabled" in response.error.lower()

    # ------------------------
    # 工作流编排测试
    # ------------------------

    @pytest.mark.unit
    def test_orchestrate_simple_workflow(self):
        """测试编排简单工作流"""
        supervisor = AgentSupervisor()
        mock_agent = MockAgent()
        supervisor.register_agent(mock_agent)

        workflow = [
            {
                "agent": "mock_agent",
                "action": "test",
                "params": {}
            }
        ]

        result = supervisor.orchestrate(workflow)

        assert result["success"] is True
        assert len(result["results"]) == 1

    @pytest.mark.unit
    def test_orchestrate_multi_step_workflow(self):
        """测试编排多步骤工作流"""
        supervisor = AgentSupervisor()
        mock_agent = MockAgent()
        supervisor.register_agent(mock_agent)

        workflow = [
            {
                "agent": "mock_agent",
                "action": "step1",
                "params": {}
            },
            {
                "agent": "mock_agent",
                "action": "step2",
                "params": {}
            },
            {
                "agent": "mock_agent",
                "action": "step3",
                "params": {}
            }
        ]

        result = supervisor.orchestrate(workflow)

        assert result["success"] is True
        assert len(result["results"]) == 3
        assert mock_agent.call_count == 3

    @pytest.mark.unit
    def test_orchestrate_workflow_with_failure(self):
        """测试编排包含失败的工作流"""
        supervisor = AgentSupervisor()
        failing_agent = FailingAgent()
        supervisor.register_agent(failing_agent)

        workflow = [
            {
                "agent": "failing_agent",
                "action": "step1",
                "params": {}
            },
            {
                "agent": "failing_agent",
                "action": "step2",
                "params": {}
            }
        ]

        result = supervisor.orchestrate(workflow)

        # 应该在第一次失败后停止
        assert result["success"] is False
        assert len(result["results"]) == 1

    # ------------------------
    # 统计测试
    # ------------------------

    @pytest.mark.unit
    def test_get_stats(self):
        """测试获取统计信息"""
        supervisor = AgentSupervisor()

        # 执行一些操作
        supervisor.execute_agent("memory", {"action": "add_note"})
        supervisor.execute_agent("memory", {"action": "search"})

        stats = supervisor.get_stats()

        assert stats["requests"]["total"] == 2
        assert "memory" in stats["agents"]
        assert stats["agents"]["memory"]["calls"] == 2


class TestPredefinedWorkflows:
    """预定义工作流测试"""

    @pytest.mark.unit
    def test_workflow_license_application(self):
        """测试证照申请工作流"""
        supervisor = AgentSupervisor()

        # 这个测试只验证工作流能正确构建
        # 实际执行可能需要更多 mock
        assert hasattr(supervisor, "workflow_license_application_complete")

    @pytest.mark.unit
    def test_workflow_daily_news(self):
        """测试每日新闻工作流"""
        supervisor = AgentSupervisor()

        assert hasattr(supervisor, "workflow_daily_news_summary")


# ================================
# 参数化测试
# ================================

class TestAgentSupervisorParameterized:
    """参数化测试"""

    @pytest.mark.unit
    @pytest.mark.parametrize("agent_name", [
        "market_supervision",
        "memory",
        "file_organizer"
    ])
    def test_default_agents_registered(self, agent_name: str):
        """测试默认智能体都已注册"""
        supervisor = AgentSupervisor()

        assert agent_name in supervisor.agents
        assert supervisor.agents[agent_name].enabled is True
