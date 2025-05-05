import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional, Dict

class LoggerManager:
    _instance = None
    _loggers: Dict[str, logging.Logger] = {}
    _config = {
        "level": "INFO",
        "file": "log/ai_talkshow.log",
        "max_size": 10485760,
        "backup_count": 5
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoggerManager, cls).__new__(cls)
        return cls._instance
    
    def set_config(self, config: dict) -> None:
        """设置全局日志配置"""
        self._config.update(config)
        # 更新所有已存在的logger的配置
        for logger in self._loggers.values():
            self._update_logger_config(logger)
    
    def _update_logger_config(self, logger: logging.Logger) -> None:
        """更新logger的配置"""
        # 设置日志级别
        logger.setLevel(getattr(logging, self._config["level"].upper()))
        
        # 移除现有的处理器
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # 创建日志目录
        log_dir = os.path.dirname(self._config["file"])
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 文件处理器
        file_handler = RotatingFileHandler(
            self._config["file"],
            maxBytes=self._config["max_size"],
            backupCount=self._config["backup_count"],
            encoding='utf-8'
        )
        file_handler.setLevel(getattr(logging, self._config["level"].upper()))
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, self._config["level"].upper()))
        
        # 格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加处理器
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    def setup_logger(self, name: str) -> logging.Logger:
        """设置并返回一个配置好的logger实例"""
        logger = logging.getLogger(name)
        logger.propagate = False  # 防止日志向上传播
        self._update_logger_config(logger)
        self._loggers[name] = logger
        return logger
    
    def get_logger(self, name: str) -> logging.Logger:
        """获取logger实例，如果不存在则创建一个新的"""
        if name not in self._loggers:
            return self.setup_logger(name)
        return self._loggers[name]

# 创建全局单例实例
logger_manager = LoggerManager()

# 提供便捷的接口函数
def setup_logger(name: str) -> logging.Logger:
    """设置并返回一个配置好的logger实例"""
    return logger_manager.setup_logger(name)

def get_logger(name: str) -> logging.Logger:
    """获取logger实例"""
    return logger_manager.get_logger(name) 