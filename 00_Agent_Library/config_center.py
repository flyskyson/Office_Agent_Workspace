#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一配置中心 - ConfigCenter
为 Office Agent Workspace 提供单一数据源的配置管理

作者: Claude Code
日期: 2026-01-16
版本: 1.0.0
"""

import sys
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from copy import deepcopy
from datetime import datetime

# Windows 终端编码修复
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass


# ============================================================================
# 配置中心核心类
# ============================================================================

class ConfigCenter:
    """
    统一配置中心 - 单一数据源原则

    功能:
    1. 分层配置系统（默认 < 环境 < 项目 < 本地）
    2. 配置合并和覆盖
    3. 配置验证
    4. 热重载
    5. 配置导出和导入
    """

    def __init__(self, workspace_root: Path = None):
        """
        初始化配置中心

        参数:
            workspace_root: 工作区根目录
        """
        if workspace_root is None:
            workspace_root = Path(__file__).parent.parent

        self.workspace_root = Path(workspace_root)

        # 配置目录结构
        self.config_dir = self.workspace_root / "04_Data_&_Resources" / "config"
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # 配置层级（从低到高优先级）
        self.layers = [
            "defaults.yaml",      # 默认配置（提交到 git）
            "environment.yaml",   # 环境配置（dev/prod/test）
            "local.yaml"          # 本地覆盖（不提交 git）
        ]

        # 项目配置目录
        self.projects_dir = self.config_dir / "projects"
        self.projects_dir.mkdir(exist_ok=True)

        # 缓存
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._last_load: Dict[str, datetime] = {}

        print(f"[INFO] 配置中心初始化完成")
        print(f"[INFO] 配置目录: {self.config_dir}")

    # ========================================================================
    # 核心配置方法
    # ========================================================================

    def get(self, key: str, default: Any = None, layer: str = None) -> Any:
        """
        获取配置值（支持嵌套访问）

        参数:
            key: 配置键，支持点号分隔的嵌套访问（如 "database.host"）
            default: 默认值
            layer: 指定配置层（可选）

        返回:
            配置值

        示例:
            >>> config.get("database.host")
            'localhost'
            >>> config.get("market_supervision.ocr.engine")
            'baidu'
        """
        config = self._load_config(layer=layer)

        # 支持点号分隔的嵌套访问
        keys = key.split('.')
        value = config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default

        return value if value is not None else default

    def set(self, key: str, value: Any, layer: str = "local") -> None:
        """
        设置配置值（只修改 local 层）

        参数:
            key: 配置键
            value: 配置值
            layer: 配置层（默认 local）
        """
        config = self._load_layer(layer)

        # 支持嵌套设置
        keys = key.split('.')
        current = config

        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]

        current[keys[-1]] = value

        # 保存到文件
        self._save_layer(layer, config)

        # 清除缓存
        self._clear_cache()

        print(f"[INFO] 配置已更新: {key} = {value}")

    def get_all(self, layer: str = None) -> Dict[str, Any]:
        """
        获取所有配置

        参数:
            layer: 指定配置层（可选）

        返回:
            完整配置字典
        """
        return deepcopy(self._load_config(layer=layer))

    # ========================================================================
    # 项目配置
    # ========================================================================

    def get_project_config(self, project_name: str) -> Dict[str, Any]:
        """
        获取项目配置

        参数:
            project_name: 项目名称（如 "market_supervision"）

        返回:
            项目配置字典
        """
        project_file = self.projects_dir / f"{project_name}.yaml"

        if not project_file.exists():
            # 创建默认项目配置
            return self._create_default_project_config(project_name)

        with open(project_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}

    def set_project_config(self, project_name: str, config: Dict[str, Any]) -> None:
        """
        设置项目配置

        参数:
            project_name: 项目名称
            config: 配置字典
        """
        project_file = self.projects_dir / f"{project_name}.yaml"

        with open(project_file, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True, default_flow_style=False)

        print(f"[INFO] 项目配置已保存: {project_name}")

    def list_projects(self) -> List[str]:
        """列出所有项目"""
        projects = []
        for file in self.projects_dir.glob("*.yaml"):
            projects.append(file.stem)
        return sorted(projects)

    # ========================================================================
    # 配置层管理
    # ========================================================================

    def _load_layer(self, layer: str) -> Dict[str, Any]:
        """加载单个配置层"""
        layer_file = self.config_dir / layer

        if not layer_file.exists():
            return {}

        with open(layer_file, 'r', encoding='utf-8') as f:
            if layer.endswith('.yaml'):
                return yaml.safe_load(f) or {}
            elif layer.endswith('.json'):
                return json.load(f)
            else:
                raise ValueError(f"不支持的配置文件格式: {layer}")

    def _save_layer(self, layer: str, config: Dict[str, Any]) -> None:
        """保存配置层"""
        layer_file = self.config_dir / layer

        with open(layer_file, 'w', encoding='utf-8') as f:
            if layer.endswith('.yaml'):
                yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
            elif layer.endswith('.json'):
                json.dump(config, f, ensure_ascii=False, indent=2)

    def _load_config(self, layer: str = None) -> Dict[str, Any]:
        """
        加载并合并配置

        参数:
            layer: 如果指定，只加载该层

        返回:
            合并后的配置
        """
        cache_key = f"all_{layer}" if layer else "all"

        # 检查缓存
        if cache_key in self._cache:
            return self._cache[cache_key]

        # 加载并合并
        merged = {}

        if layer:
            # 只加载指定层
            merged = self._load_layer(layer)
        else:
            # 按优先级合并所有层
            for layer_name in self.layers:
                layer_config = self._load_layer(layer_name)
                merged = self._deep_merge(merged, layer_config)

        # 缓存
        self._cache[cache_key] = merged
        self._last_load[cache_key] = datetime.now()

        return merged

    def _deep_merge(self, base: Dict, update: Dict) -> Dict:
        """深度合并字典"""
        result = deepcopy(base)

        for key, value in update.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = deepcopy(value)

        return result

    def _clear_cache(self) -> None:
        """清除缓存"""
        self._cache.clear()
        self._last_load.clear()

    # ========================================================================
    # 默认配置生成
    # ========================================================================

    def _create_default_project_config(self, project_name: str) -> Dict[str, Any]:
        """创建默认项目配置"""
        default_config = {
            "name": project_name,
            "version": "1.0.0",
            "enabled": True,
            "database": {
                "type": "sqlite",
                "path": f"04_Data_&_Resources/{project_name}.db"
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        }

        # 保存默认配置
        self.set_project_config(project_name, default_config)

        return default_config

    def init_defaults(self) -> None:
        """初始化默认配置文件"""
        print("\n[初始化默认配置]")

        # 1. defaults.yaml
        defaults = {
            "version": "1.0.0",
            "workspace": {
                "name": "Office Agent Workspace",
                "root": str(self.workspace_root)
            },
            "database": {
                "default_type": "sqlite",
                "sqlite_path": "04_Data_&_Resources/databases",
                "pool_size": 5
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "file": "06_Learning_Journal/workspace.log"
            },
            "paths": {
                "data": "04_Data_&_Resources",
                "output": "05_Outputs",
                "logs": "06_Learning_Journal",
                "temp": "00_Agent_Library/temp"
            },
            "features": {
                "mcp_servers": {
                    "enabled": True,
                    "auto_start": True
                },
                "skills": {
                    "enabled": True,
                    "auto_discover": True
                }
            }
        }

        self._save_layer("defaults.yaml", defaults)
        print("  ✅ 创建 defaults.yaml")

        # 2. environment.yaml
        environment = {
            "mode": "development",
            "debug": True,
            "testing": False
        }

        self._save_layer("environment.yaml", environment)
        print("  ✅ 创建 environment.yaml")

        # 3. local.yaml (添加到 .gitignore)
        if not (self.config_dir / "local.yaml").exists():
            local = {
                "user": {
                    "name": "",
                    "email": ""
                },
                "api_keys": {}
            }
            self._save_layer("local.yaml", local)
            print("  ✅ 创建 local.yaml")

        # 4. 项目配置示例
        example_projects = {
            "market_supervision": {
                "name": "市场监管智能体",
                "enabled": True,
                "database": {
                    "type": "sqlite",
                    "path": "04_Data_&_Resources/operators_database.db"
                },
                "ocr": {
                    "engine": "baidu",
                    "fallback": "paddle"
                },
                "templates": {
                    "path": "01_Active_Projects/market_supervision_agent/templates"
                }
            },
            "memory_agent": {
                "name": "记忆助手",
                "enabled": True,
                "database": {
                    "type": "chromadb",
                    "path": "01_Active_Projects/memory_agent/chroma_db"
                },
                "embedding": {
                    "model": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
                }
            },
            "file_organizer": {
                "name": "文件整理工具",
                "enabled": True,
                "rules": {
                    "path": "01_Active_Projects/file_organizer/config.json"
                }
            }
        }

        for project_name, config in example_projects.items():
            self.set_project_config(project_name, config)
            print(f"  ✅ 创建项目配置: {project_name}")

        print("\n[INFO] 默认配置初始化完成")

    # ========================================================================
    # 配置验证
    # ========================================================================

    def validate(self) -> List[str]:
        """
        验证配置

        返回:
            错误列表（空列表表示验证通过）
        """
        errors = []

        # 检查必需的配置层
        for layer in self.layers:
            layer_file = self.config_dir / layer
            if not layer_file.exists():
                errors.append(f"缺少配置层: {layer}")

        # 验证默认配置
        defaults = self._load_layer("defaults.yaml")
        required_keys = ["version", "workspace", "database", "paths"]
        for key in required_keys:
            if key not in defaults:
                errors.append(f"defaults.yaml 缺少必需的键: {key}")

        return errors

    # ========================================================================
    # 配置导出和导入
    # ========================================================================

    def export_config(self, output_path: Path = None) -> None:
        """
        导出完整配置

        参数:
            output_path: 输出路径（默认为当前时间戳）
        """
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.workspace_root / "05_Outputs" / f"config_export_{timestamp}.yaml"

        output_path.parent.mkdir(parents=True, exist_ok=True)

        config = self.get_all()
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True, default_flow_style=False)

        print(f"[INFO] 配置已导出: {output_path}")

    def import_config(self, input_path: Path, merge: bool = True) -> None:
        """
        导入配置

        参数:
            input_path: 输入文件路径
            merge: 是否合并（True）或替换（False）
        """
        with open(input_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        if merge:
            # 合并到 local 层
            local = self._load_layer("local.yaml")
            merged = self._deep_merge(local, config)
            self._save_layer("local.yaml", merged)
        else:
            # 替换 defaults 层
            self._save_layer("defaults.yaml", config)

        self._clear_cache()
        print(f"[INFO] 配置已导入: {input_path}")

    # ========================================================================
    # 配置快照
    # ========================================================================

    def create_snapshot(self, name: str = None) -> str:
        """
        创建配置快照

        参数:
            name: 快照名称（默认为时间戳）

        返回:
            快照路径
        """
        if name is None:
            name = datetime.now().strftime("%Y%m%d_%H%M%S")

        snapshots_dir = self.config_dir / "snapshots"
        snapshots_dir.mkdir(exist_ok=True)

        snapshot_path = snapshots_dir / f"{name}.yaml"
        self.export_config(snapshot_path)

        return str(snapshot_path)

    def list_snapshots(self) -> List[str]:
        """列出所有快照"""
        snapshots_dir = self.config_dir / "snapshots"
        if not snapshots_dir.exists():
            return []

        return [f.stem for f in snapshots_dir.glob("*.yaml")]

    def restore_snapshot(self, name: str) -> None:
        """恢复快照"""
        snapshot_path = self.config_dir / "snapshots" / f"{name}.yaml"
        if not snapshot_path.exists():
            raise FileNotFoundError(f"快照不存在: {name}")

        self.import_config(snapshot_path, merge=False)
        print(f"[INFO] 已恢复快照: {name}")


# ============================================================================
# 配置管理器 CLI
# ============================================================================

def main():
    """命令行接口"""
    import argparse

    parser = argparse.ArgumentParser(description="Office Agent Workspace 配置中心")
    parser.add_argument("command", choices=[
        "init", "get", "set", "list", "validate", "export", "snapshot"
    ], help="命令")
    parser.add_argument("--key", help="配置键")
    parser.add_argument("--value", help="配置值")
    parser.add_argument("--layer", help="配置层")
    parser.add_argument("--project", help="项目名称")
    parser.add_argument("--output", help="输出路径")

    args = parser.parse_args()

    config = ConfigCenter()

    if args.command == "init":
        config.init_defaults()
        print("\n✅ 配置中心初始化完成！")

    elif args.command == "get":
        if not args.key:
            print("❌ 请指定配置键 --key")
            return

        value = config.get(args.key, layer=args.layer)
        if isinstance(value, (dict, list)):
            print(json.dumps(value, ensure_ascii=False, indent=2))
        else:
            print(value)

    elif args.command == "set":
        if not args.key or not args.value:
            print("❌ 请指定配置键 --key 和值 --value")
            return

        # 尝试解析值类型
        try:
            value = json.loads(args.value)
        except:
            value = args.value

        config.set(args.key, value, layer=args.layer or "local")

    elif args.command == "list":
        if args.project:
            # 列出项目配置
            config_data = config.get_project_config(args.project)
            print(json.dumps(config_data, ensure_ascii=False, indent=2))
        else:
            # 列出所有项目
            projects = config.list_projects()
            print(f"可用项目 ({len(projects)}):")
            for project in projects:
                print(f"  - {project}")

    elif args.command == "validate":
        errors = config.validate()
        if errors:
            print("❌ 配置验证失败:")
            for error in errors:
                print(f"  - {error}")
        else:
            print("✅ 配置验证通过")

    elif args.command == "export":
        output_path = Path(args.output) if args.output else None
        config.export_config(output_path)

    elif args.command == "snapshot":
        if args.key:  # args.key 作为快照名称
            snapshot_path = config.create_snapshot(args.key)
            print(f"✅ 快照已创建: {snapshot_path}")
        else:
            snapshots = config.list_snapshots()
            print(f"可用快照 ({len(snapshots)}):")
            for snapshot in snapshots:
                print(f"  - {snapshot}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # 交互式模式
        print("=" * 60)
        print("Office Agent Workspace - 配置中心")
        print("=" * 60)

        config = ConfigCenter()

        # 初始化默认配置
        config.init_defaults()

        # 验证配置
        print("\n[验证配置]")
        errors = config.validate()
        if errors:
            print("❌ 验证失败:")
            for error in errors:
                print(f"  - {error}")
        else:
            print("✅ 配置验证通过")

        # 显示项目列表
        print("\n[项目列表]")
        for project in config.list_projects():
            print(f"  - {project}")

        # 创建快照
        print("\n[创建快照]")
        snapshot = config.create_snapshot("initial")
        print(f"✅ 初始快照: {snapshot}")

        print("\n" + "=" * 60)
        print("✅ 配置中心设置完成！")
        print("=" * 60)
    else:
        main()
