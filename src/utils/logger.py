import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional, Dict

class LoggerManager:
    _instance = None
    _loggers: Dict[str, logging.Logger] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoggerManager, cls).__new__(cls)
        return cls._instance
    
    def setup_logger(
        self,
        name: str,
        log_file: str,
        level: str = "INFO",
        max_size: int = 10485760,
        backup_count: int = 5
    ) -> logging.Logger:
        """设置并返回一个配置好的logger实例"""
        if name in self._loggers:
            return self._loggers[name]
            
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, level.upper()))
        logger.propagate = False  # 防止日志向上传播
        
        # 创建日志目录
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 文件处理器
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(getattr(logging, level.upper()))
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, level.upper()))
        
        # 格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加处理器
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        self._loggers[name] = logger
        return logger
    
    def get_logger(self, name: str) -> logging.Logger:
        """获取logger实例，如果不存在则创建一个默认的"""
        if name not in self._loggers:
            return self.setup_logger(
                name,
                "log/ai_talkshow.log",
                "INFO",
                10485760,
                5
            )
        return self._loggers[name]

# 创建全局单例实例
logger_manager = LoggerManager()

# 提供便捷的接口函数
def setup_logger(
    name: str,
    log_file: str,
    level: str = "INFO",
    max_size: int = 10485760,
    backup_count: int = 5
) -> logging.Logger:
    """设置并返回一个配置好的logger实例"""
    return logger_manager.setup_logger(name, log_file, level, max_size, backup_count)

def get_logger(name: str) -> logging.Logger:
    """获取logger实例"""
    return logger_manager.get_logger(name) 