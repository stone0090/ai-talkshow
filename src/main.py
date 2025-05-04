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
    logger_manager.setup_logger(
        name="ai_talkshow",
        level=logging_config.get("level", "INFO"),
        log_file=logging_config.get("file", "log/ai_talkshow.log"),
        max_size=logging_config.get("max_size", 10485760),
        backup_count=logging_config.get("backup_count", 5)
    )

def main():
    # 加载配置
    config = load_config()
    
    # 设置日志
    setup_logging(config)
    logger = logger_manager.get_logger(__name__)
    
    try:

        # 初始化AI代理
        models_config = config.get("models", {})
        ai1_config = models_config.get("ai1", {})
        ai1 = QwenAgent("ai1", ai1_config)
        ai2_config = models_config.get("ai2", {})
        ai2 = QwenAgent("ai2", ai2_config)

        # 初始化辩论管理器
        debate_config = config.get("debate", {})
        debate_manager = DebateManager(debate_config)
        debate_manager.initialize_agents(ai1, ai2)
        
        # 开始辩论
        debate_manager.run_debate()
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        raise

if __name__ == "__main__":
    main()
