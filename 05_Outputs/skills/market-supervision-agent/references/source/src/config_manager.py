#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理器

统一管理所有配置文件：
- portal_config.yaml: 政务服务网配置
- workflow_config.yaml: 工作流配置
- industry_scope.yaml: 行业经营范围映射

支持：
- 配置加载和验证
- 热更新
- 环境切换（开发/生产）
- 配置合并和覆盖

作者: Claude Code
日期: 2026-01-14
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from loguru import logger


@dataclass
class ConfigManager:
    """配置管理器"""

    # 配置文件路径
    config_dir: Path = field(default_factory=lambda: Path("config"))

    # 当前环境
    environment: str = "development"  # development | production

    # 配置缓存
    _cache: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """初始化后处理"""
        # 加载环境变量
        self.environment = os.getenv("ENVIRONMENT", "development")
        logger.info(f"配置管理器初始化，环境: {self.environment}")

    def load_config(
        self,
        config_name: str,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        加载配置文件

        Args:
            config_name: 配置名称（不含.yaml后缀）
            use_cache: 是否使用缓存

        Returns:
            配置字典
        """
        # 检查缓存
        if use_cache and config_name in self._cache:
            logger.debug(f"从缓存加载配置: {config_name}")
            return self._cache[config_name]

        # 构建文件路径
        config_file = self.config_dir / f"{config_name}.yaml"

        if not config_file.exists():
            logger.error(f"配置文件不存在: {config_file}")
            return {}

        # 加载配置
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)

            # 加载环境特定配置
            env_config_file = self.config_dir / f"{config_name}.{self.environment}.yaml"
            if env_config_file.exists():
                with open(env_config_file, 'r', encoding='utf-8') as f:
                    env_config = yaml.safe_load(f)
                # 合并配置（环境配置覆盖基础配置）
                config = self._merge_config(config, env_config)

            # 缓存配置
            if use_cache:
                self._cache[config_name] = config

            logger.info(f"加载配置: {config_name}")
            return config

        except Exception as e:
            logger.error(f"加载配置失败: {config_name}, {e}")
            return {}

    def save_config(
        self,
        config_name: str,
        config: Dict[str, Any]
    ) -> bool:
        """
        保存配置文件

        Args:
            config_name: 配置名称
            config: 配置字典

        Returns:
            是否成功
        """
        config_file = self.config_dir / f"{config_name}.yaml"

        try:
            # 确保目录存在
            config_file.parent.mkdir(parents=True, exist_ok=True)

            # 保存配置
            with open(config_file, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

            # 更新缓存
            self._cache[config_name] = config

            logger.info(f"保存配置: {config_name}")
            return True

        except Exception as e:
            logger.error(f"保存配置失败: {config_name}, {e}")
            return False

    def reload_config(self, config_name: str) -> Dict[str, Any]:
        """
        重新加载配置（清除缓存）

        Args:
            config_name: 配置名称

        Returns:
            配置字典
        """
        # 清除缓存
        if config_name in self._cache:
            del self._cache[config_name]

        # 重新加载
        return self.load_config(config_name, use_cache=False)

    def get_portal_config(self) -> Dict[str, Any]:
        """获取政务服务网配置"""
        return self.load_config("portal_config")

    def get_workflow_config(self) -> Dict[str, Any]:
        """获取工作流配置"""
        return self.load_config("workflow_config")

    def get_industry_scope_config(self) -> Dict[str, Any]:
        """获取行业经营范围配置"""
        return self.load_config("industry_scope")

    def get_scenarios(self) -> Dict[str, Any]:
        """获取所有场景配置"""
        workflow_config = self.get_workflow_config()
        return workflow_config.get("scenarios", {})

    def get_scenario(self, scenario_name: str) -> Optional[Dict[str, Any]]:
        """
        获取特定场景配置

        Args:
            scenario_name: 场景名称（registration, change, cancellation, annual_report）

        Returns:
            场景配置
        """
        scenarios = self.get_scenarios()
        return scenarios.get(scenario_name)

    def get_material_requirements(
        self,
        scenario: str
    ) -> List[Dict[str, Any]]:
        """
        获取场景的材料清单

        Args:
            scenario: 场景名称

        Returns:
            材料列表
        """
        scenario_config = self.get_scenario(scenario)
        if not scenario_config:
            return []

        return scenario_config.get("materials", [])

    def get_industry_scopes(self, industry: str) -> List[Dict[str, Any]]:
        """
        获取行业的标准经营范围

        Args:
            industry: 行业名称

        Returns:
            经营范围列表
        """
        industry_config = self.get_industry_scope_config()
        industries = industry_config.get("industries", {})
        industry_data = industries.get(industry, {})

        return industry_data.get("standard_scopes", [])

    def get_all_industries(self) -> List[str]:
        """
        获取所有支持的行业

        Returns:
            行业名称列表
        """
        industry_config = self.get_industry_scope_config()
        return list(industry_config.get("industries", {}).keys())

    def _merge_config(
        self,
        base: Dict[str, Any],
        override: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        递归合并配置

        Args:
            base: 基础配置
            override: 覆盖配置

        Returns:
            合并后的配置
        """
        result = base.copy()

        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_config(result[key], value)
            else:
                result[key] = value

        return result

    def validate_config(self, config_name: str) -> bool:
        """
        验证配置文件

        Args:
            config_name: 配置名称

        Returns:
            是否有效
        """
        config = self.load_config(config_name)

        if not config:
            logger.error(f"配置为空: {config_name}")
            return False

        # 根据不同配置类型验证
        if config_name == "portal_config":
            return self._validate_portal_config(config)
        elif config_name == "workflow_config":
            return self._validate_workflow_config(config)
        elif config_name == "industry_scope":
            return self._validate_industry_scope_config(config)
        else:
            logger.warning(f"未知的配置类型: {config_name}")
            return True

    def _validate_portal_config(self, config: Dict[str, Any]) -> bool:
        """验证政务服务网配置"""
        required_fields = ["portal", "selectors"]

        for field in required_fields:
            if field not in config:
                logger.error(f"配置缺少必需字段: {field}")
                return False

        # 检查登录凭证
        credentials = config.get("portal", {}).get("credentials", {})
        if not credentials.get("username") or not credentials.get("password"):
            logger.warning("政务服务网账号或密码未配置")

        return True

    def _validate_workflow_config(self, config: Dict[str, Any]) -> bool:
        """验证工作流配置"""
        required_fields = ["scenarios", "stages", "input_sources"]

        for field in required_fields:
            if field not in config:
                logger.error(f"配置缺少必需字段: {field}")
                return False

        # 检查场景配置
        scenarios = config.get("scenarios", {})
        for scenario_name, scenario_config in scenarios.items():
            if "required_fields" not in scenario_config:
                logger.warning(f"场景 {scenario_name} 缺少 required_fields")
            if "materials" not in scenario_config:
                logger.warning(f"场景 {scenario_name} 缺少 materials")

        return True

    def _validate_industry_scope_config(self, config: Dict[str, Any]) -> bool:
        """验证行业经营范围配置"""
        required_fields = ["industries"]

        for field in required_fields:
            if field not in config:
                logger.error(f"配置缺少必需字段: {field}")
                return False

        # 检查行业配置
        industries = config.get("industries", {})
        for industry_name, industry_config in industries.items():
            if "standard_scopes" not in industry_config:
                logger.warning(f"行业 {industry_name} 缺少 standard_scopes")

        return True


# ==================== 全局配置实例 ====================

# 创建全局配置管理器实例
_config_manager = None


def get_config_manager() -> ConfigManager:
    """
    获取全局配置管理器实例

    Returns:
        配置管理器
    """
    global _config_manager

    if _config_manager is None:
        _config_manager = ConfigManager()

    return _config_manager


def load_config(config_name: str) -> Dict[str, Any]:
    """便捷函数：加载配置"""
    return get_config_manager().load_config(config_name)


def get_portal_config() -> Dict[str, Any]:
    """便捷函数：获取政务服务网配置"""
    return get_config_manager().get_portal_config()


def get_workflow_config() -> Dict[str, Any]:
    """便捷函数：获取工作流配置"""
    return get_config_manager().get_workflow_config()


def get_industry_scope_config() -> Dict[str, Any]:
    """便捷函数：获取行业经营范围配置"""
    return get_config_manager().get_industry_scope_config()


if __name__ == "__main__":
    # 测试配置管理器
    logger.info("=" * 60)
    logger.info("配置管理器测试")
    logger.info("=" * 60)

    config_manager = ConfigManager()

    # 加载所有配置
    configs = ["portal_config", "workflow_config", "industry_scope"]

    for config_name in configs:
        logger.info(f"\n加载配置: {config_name}")
        config = config_manager.load_config(config_name)

        if config:
            logger.success(f"配置加载成功: {config_name}")
            logger.info(f"配置项数量: {len(config)}")
        else:
            logger.error(f"配置加载失败: {config_name}")

        # 验证配置
        valid = config_manager.validate_config(config_name)
        logger.info(f"配置验证: {'通过' if valid else '失败'}")

    # 测试场景配置
    logger.info("\n场景配置:")
    scenarios = config_manager.get_scenarios()
    for scenario_name in scenarios.keys():
        logger.info(f"  - {scenario_name}")

    # 测试行业配置
    logger.info("\n支持的行业:")
    industries = config_manager.get_all_industries()
    for industry in industries:
        logger.info(f"  - {industry}")
