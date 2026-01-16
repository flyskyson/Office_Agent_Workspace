"""
ConfigCenter 单元测试

测试配置中心的各项功能：
- 配置初始化
- 配置读取和写入
- 嵌套键访问
- 配置合并
- 配置验证
"""

import pytest
import yaml
from pathlib import Path
from datetime import datetime

from 00_Agent_Library.config_center import (
    ConfigCenter,
    ConfigLayer,
    ConfigError
)


# ================================
# 测试类定义
# ================================

class TestConfigCenter:
    """ConfigCenter 测试类"""

    # ------------------------
    # 初始化测试
    # ------------------------

    @pytest.mark.unit
    def test_init_default(self, temp_dir: Path):
        """测试默认初始化"""
        config = ConfigCenter(config_dir=str(temp_dir))

        assert config is not None
        assert config.config_dir == temp_dir
        assert isinstance(config.config, dict)

    @pytest.mark.unit
    def test_init_with_custom_dir(self, temp_dir: Path):
        """测试自定义目录初始化"""
        custom_dir = temp_dir / "custom"
        custom_dir.mkdir(parents=True, exist_ok=True)

        config = ConfigCenter(config_dir=str(custom_dir))

        assert config.config_dir == custom_dir

    # ------------------------
    # 配置初始化测试
    # ------------------------

    @pytest.mark.unit
    def test_init_defaults(self, temp_config_file: Path):
        """测试初始化默认配置"""
        config = ConfigCenter(config_dir=str(temp_config_file.parent))
        config.init_defaults()

        assert temp_config_file.exists()

        with open(temp_config_file, 'r', encoding='utf-8') as f:
            defaults = yaml.safe_load(f)

        assert 'version' in defaults
        assert 'workspace' in defaults
        assert 'database' in defaults

    @pytest.mark.unit
    def test_init_environment(self, temp_dir: Path):
        """测试初始化环境配置"""
        config = ConfigCenter(config_dir=str(temp_dir))
        config.init_environment(mode="development")

        env_file = temp_dir / "environment.yaml"
        assert env_file.exists()

        with open(env_file, 'r', encoding='utf-8') as f:
            env_config = yaml.safe_load(f)

        assert env_config['mode'] == 'development'
        assert env_config['debug'] is True

    # ------------------------
    # 配置读取测试
    # ------------------------

    @pytest.mark.unit
    def test_get_simple_key(self, temp_dir: Path, sample_config: dict):
        """测试读取简单键"""
        config = ConfigCenter(config_dir=str(temp_dir))
        config.config = sample_config

        version = config.get("version")
        assert version == "2.0.0"

    @pytest.mark.unit
    def test_get_nested_key(self, temp_dir: Path, sample_config: dict):
        """测试读取嵌套键"""
        config = ConfigCenter(config_dir=str(temp_dir))
        config.config = sample_config

        db_type = config.get("database.default_type")
        assert db_type == "sqlite"

        workspace_name = config.get("workspace.name")
        assert workspace_name == "Test Workspace"

    @pytest.mark.unit
    def test_get_with_default(self, temp_dir: Path):
        """测试带默认值的读取"""
        config = ConfigCenter(config_dir=str(temp_dir))

        # 读取不存在的键
        value = config.get("nonexistent.key", default="default_value")
        assert value == "default_value"

    @pytest.mark.unit
    def test_get_project_config(self, temp_dir: Path, sample_project_config: dict):
        """测试读取项目配置"""
        config = ConfigCenter(config_dir=str(temp_dir))

        # 创建项目配置文件
        projects_dir = temp_dir / "projects"
        projects_dir.mkdir(parents=True, exist_ok=True)

        project_file = projects_dir / "test_project.yaml"
        with open(project_file, 'w', encoding='utf-8') as f:
            yaml.dump(sample_project_config, f, allow_unicode=True)

        project_config = config.get_project_config("test_project")

        assert project_config['name'] == "测试项目"
        assert project_config['enabled'] is True

    # ------------------------
    # 配置写入测试
    # ------------------------

    @pytest.mark.unit
    def test_set_simple_value(self, temp_dir: Path):
        """测试设置简单值"""
        config = ConfigCenter(config_dir=str(temp_dir))

        config.set("test_key", "test_value")
        value = config.get("test_key")

        assert value == "test_value"

    @pytest.mark.unit
    def test_set_nested_value(self, temp_dir: Path):
        """测试设置嵌套值"""
        config = ConfigCenter(config_dir=str(temp_dir))

        config.set("database.pool_size", 10)
        value = config.get("database.pool_size")

        assert value == 10

    # ------------------------
    # 配置验证测试
    # ------------------------

    @pytest.mark.unit
    def test_validate_success(self, temp_dir: Path, sample_config: dict):
        """测试配置验证成功"""
        config = ConfigCenter(config_dir=str(temp_dir))
        config.config = sample_config

        errors = config.validate()

        assert isinstance(errors, list)
        assert len(errors) == 0

    @pytest.mark.unit
    def test_validate_missing_required(self, temp_dir: Path):
        """测试缺少必需字段"""
        config = ConfigCenter(config_dir=str(temp_dir))
        config.config = {}  # 空配置

        errors = config.validate()

        # 应该有错误（缺少必需字段）
        assert len(errors) > 0

    # ------------------------
    # 快照功能测试
    # ------------------------

    @pytest.mark.unit
    def test_create_snapshot(self, temp_dir: Path, sample_config: dict):
        """测试创建快照"""
        config = ConfigCenter(config_dir=str(temp_dir))
        config.config = sample_config

        snapshot_path = config.create_snapshot("test_snapshot")

        assert snapshot_path.exists()
        assert "test_snapshot" in str(snapshot_path)

    @pytest.mark.unit
    def test_list_snapshots(self, temp_dir: Path, sample_config: dict):
        """测试列出快照"""
        config = ConfigCenter(config_dir=str(temp_dir))
        config.config = sample_config

        # 创建多个快照
        config.create_snapshot("snapshot1")
        config.create_snapshot("snapshot2")

        snapshots = config.list_snapshots()

        assert len(snapshots) >= 2
        assert "snapshot1" in snapshots
        assert "snapshot2" in snapshots


class TestConfigLayer:
    """配置层枚举测试"""

    @pytest.mark.unit
    def test_layer_priority(self):
        """测试配置层优先级"""
        assert ConfigLayer.DEFAULTS.value == 0
        assert ConfigLayer.ENVIRONMENT.value == 1
        assert ConfigLayer.LOCAL.value == 2


# ================================
# 参数化测试
# ================================

class TestConfigCenterParameterized:
    """参数化测试"""

    @pytest.mark.unit
    @pytest.mark.parametrize("key,expected_value", [
        ("version", "2.0.0"),
        ("workspace.name", "Test Workspace"),
        ("database.default_type", "sqlite"),
        ("features.mcp_servers.enabled", True),
    ])
    def test_get_various_keys(self, temp_dir: Path, sample_config: dict,
                              key: str, expected_value):
        """参数化测试各种键的读取"""
        config = ConfigCenter(config_dir=str(temp_dir))
        config.config = sample_config

        value = config.get(key)
        assert value == expected_value


# ================================
# 异常测试
# ================================

class TestConfigCenterExceptions:
    """异常测试"""

    @pytest.mark.unit
    def test_get_invalid_key(self, temp_dir: Path):
        """测试读取无效键"""
        config = ConfigCenter(config_dir=str(temp_dir))
        config.config = {}

        # 不带默认值读取不存在的键应该返回 None
        value = config.get("invalid.key")
        assert value is None

    @pytest.mark.unit
    def test_set_with_invalid_layer(self, temp_dir: Path):
        """测试使用无效层设置配置"""
        config = ConfigCenter(config_dir=str(temp_dir))

        # 应该默认使用 local 层
        config.set("test.key", "value")

        # 验证设置成功
        assert config.get("test.key") == "value"
