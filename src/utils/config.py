import os
import yaml
from typing import Any, Dict

class ConfigManager:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self._validate_config()
    
    def _load_config(self, path: str) -> Dict[str, Any]:
        """加载YAML配置文件"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            return config
        except Exception as e:
            raise ValueError(f"Failed to load config file: {e}")
    
    def _validate_config(self) -> None:
        """验证配置的完整性"""
        required_sections = ['bilibili', 'models', 'tts', 'debate', 'logging']
        for section in required_sections:
            if section not in self.config:
                raise ValueError(f"Missing required config section: {section}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值，支持点号分隔的嵌套键"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value
    
    def get_from_env(self, key: str, env_var: str, default: Any = None) -> Any:
        """从环境变量获取配置值"""
        value = self.get(key)
        if value == "":
            value = os.getenv(env_var, default)
        return value 