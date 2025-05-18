import asyncio
import os
import yaml
from src.core.debate import DebateManager
from src.models.qwen import QwenAgent
from src.utils.logger import logger_manager

def load_config() -> dict:
    """加载配置文件"""
    config_path = os.path.join(os.path.dirname(__file__), "..", "config", "config.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def setup_logging(config: dict) -> None:
    """设置日志"""
    logging_config = config.get("logging", {})
    # 设置全局日志配置
    logger_manager.set_config(logging_config)
    # 创建主logger
    logger_manager.setup_logger("ai_talkshow")

def main():
    # 加载配置
    config = load_config()
    logger = logger_manager.get_logger(__name__)
    logger.debug("Configuration loaded successfully")
    
    # 设置日志
    setup_logging(config)
    logger.debug("Logging system initialized")
    
    try:
        # 初始化AI代理
        models_config = config.get("models", {})
        logger.debug(f"Initializing AI agents with config: {models_config}")
        
        ai1_config = models_config.get("ai1", {})
        ai1 = QwenAgent("ai1", ai1_config)
        logger.debug("ai1 initialized...")
        
        ai2_config = models_config.get("ai2", {})
        ai2 = QwenAgent("ai2", ai2_config)
        logger.debug("ai2 initialized...")

        # 初始化辩论管理器
        debate_config = config.get("debate", {})
        logger.debug(f"Initializing debate manager with config: {debate_config}")
        debate_manager = DebateManager(debate_config)
        debate_manager.initialize_agents(ai1, ai2)
        
        # 开始辩论
        logger.info("Starting debate session")
        asyncio.run(debate_manager.run_debate())
        logger.info("Debate session completed")
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
