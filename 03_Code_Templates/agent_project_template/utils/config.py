"""
配置文件管理模块
"""

import yaml
from pathlib import Path
from typing import Any, Dict


class Config:
    """配置类"""

    def __init__(self, config_path: str = 'config.yaml'):
        """初始化配置

        Args:
            config_path: 配置文件路径
        """
        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if not self.config_path.exists():
            # 如果配置文件不存在，创建默认配置
            return self._create_default_config()

        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}

    def _create_default_config(self) -> Dict[str, Any]:
        """创建默认配置"""
        default_config = {
            'app': {
                'name': 'My Agent',
                'version': '1.0.0',
                'debug': False
            },
            'paths': {
                'input': 'data/input',
                'output': 'data/output',
                'temp': 'data/temp'
            },
            'logging': {
                'level': 'INFO',
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                'file': 'logs/app.log'
            }
        }

        # 保存默认配置
        self.save(default_config)
        return default_config

    def save(self, config: Dict[str, Any] = None):
        """保存配置到文件"""
        config = config or self.config
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True, default_flow_style=False)

    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default

        return value if value is not None else default

    def set(self, key: str, value: Any):
        """设置配置值"""
        keys = key.split('.')
        config = self.config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value
        self.save()

    def __repr__(self) -> str:
        return f"Config({self.config})"

    def __getitem__(self, key: str) -> Any:
        return self.get(key)

    def __setitem__(self, key: str, value: Any):
        self.set(key, value)
