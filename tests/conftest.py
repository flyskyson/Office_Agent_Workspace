"""
pytest 配置和共享夹具

提供全局测试配置和可复用的测试夹具
"""

import os
import sys
import tempfile
from pathlib import Path
from typing import Generator

import pytest
import yaml


# ================================
# 路径配置
# ================================

# 添加项目根目录到 Python 路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "00_Agent_Library"))


# ================================
# 测试数据路径
# ================================

@pytest.fixture
def test_data_dir() -> Path:
    """测试数据目录"""
    return PROJECT_ROOT / "tests" / "fixtures"


@pytest.fixture
def test_configs_dir() -> Path:
    """测试配置目录"""
    return test_data_dir(None) / "configs"


@pytest.fixture
def test_db_path() -> Path:
    """测试数据库路径"""
    return test_data_dir(None) / "test_databases"


# ================================
# 临时目录和文件
# ================================

@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """临时目录（自动清理）"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def temp_config_file(temp_dir: Path) -> Generator[Path, None, None]:
    """临时配置文件"""
    config_file = temp_dir / "test_config.yaml"
    yield config_file
    # 自动清理


@pytest.fixture
def temp_db_file(temp_dir: Path) -> Generator[Path, None, None]:
    """临时数据库文件"""
    db_file = temp_dir / "test.db"
    yield db_file
    # 自动清理


# ================================
# 配置夹具
# ================================

@pytest.fixture
def sample_config() -> dict:
    """示例配置"""
    return {
        "version": "2.0.0",
        "workspace": {
            "name": "Test Workspace",
            "root": "/tmp/test_workspace"
        },
        "database": {
            "default_type": "sqlite",
            "sqlite_path": "test_databases"
        },
        "features": {
            "mcp_servers": {
                "enabled": True
            }
        }
    }


@pytest.fixture
def sample_project_config() -> dict:
    """示例项目配置"""
    return {
        "name": "测试项目",
        "enabled": True,
        "database": {
            "type": "sqlite",
            "path": "test.db"
        }
    }


# ================================
# 智能体测试夹具
# ================================

@pytest.fixture
def mock_agent_response():
    """模拟智能体响应"""
    from datetime import datetime
    from 00_Agent_Library.agent_supervisor import AgentResponse

    return AgentResponse(
        success=True,
        data={"message": "测试成功", "result": 42},
        error=None
    )


@pytest.fixture
def sample_workflow():
    """示例工作流"""
    return [
        {
            "agent": "memory",
            "action": "add_note",
            "params": {
                "title": "测试笔记",
                "content": "这是测试内容"
            }
        },
        {
            "agent": "file_organizer",
            "action": "scan",
            "params": {
                "path": "/tmp/test"
            }
        }
    ]


# ================================
# 数据库测试夹具
# ================================

@pytest.fixture
def sample_operator_data():
    """示例经营户数据"""
    return {
        "operator_name": "张三",
        "id_card": "123456789012345678",
        "phone": "13800138000",
        "business_name": "张三商铺",
        "business_address": "北京市朝阳区xxx"
    }


@pytest.fixture
def sample_note_data():
    """示例笔记数据"""
    return {
        "title": "测试笔记",
        "content": "这是测试笔记的内容",
        "tags": "测试,笔记",
        "category": "测试"
    }


# ================================
# MCP 测试夹具
# ================================

@pytest.fixture
def mcp_request_template():
    """MCP 请求模板"""
    return {
        "jsonrpc": "2.0",
        "id": 1,
        "method": None,
        "params": None
    }


@pytest.fixture
def sample_mcp_tools():
    """示例 MCP 工具列表"""
    return [
        {
            "name": "execute_query",
            "description": "执行 SQL 查询",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "params": {"type": "array"}
                }
            }
        },
        {
            "name": "list_tables",
            "description": "列出所有表",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "db_name": {"type": "string"}
                }
            }
        }
    ]


# ================================
# 环境变量夹具
# ================================

@pytest.fixture
def mock_env_vars():
    """模拟环境变量"""
    original_env = os.environ.copy()

    # 设置测试环境变量
    os.environ.update({
        "TEST_MODE": "true",
        "WORKSPACE_ROOT": str(PROJECT_ROOT),
        "LOG_LEVEL": "DEBUG"
    })

    yield os.environ

    # 恢复原始环境变量
    os.environ.clear()
    os.environ.update(original_env)


# ================================
# 标记定义
# ================================

def pytest_configure(config):
    """配置 pytest 标记"""
    config.addinivalue_line(
        "markers", "unit: 单元测试标记"
    )
    config.addinivalue_line(
        "markers", "integration: 集成测试标记"
    )
    config.addinivalue_line(
        "markers", "e2e: 端到端测试标记"
    )
    config.addinivalue_line(
        "markers", "slow: 慢速测试标记"
    )
    config.addinivalue_line(
        "markers", "requires_network: 需要网络连接"
    )


# ================================
# 跳过条件
# ================================

def pytest_collection_modifyitems(config, items):
    """根据条件跳过测试"""

    # 跳过需要网络的测试（如果没有网络）
    if not config.getoption("--run-network", default=False):
        skip_network = pytest.mark.skip(reason="需要 --run-network 选项")
        for item in items:
            if "requires_network" in item.keywords:
                item.add_marker(skip_network)
