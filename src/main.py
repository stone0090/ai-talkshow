import os
import sys
from utils.config import ConfigManager
from utils.logger import logger_manager
from models.qwen import QwenAgent
from core.debate import DebateManager

def main():
    # 加载配置
    config_path = os.path.join(os.path.dirname(__file__), "..", "config", "config.yaml")
    config_manager = ConfigManager(config_path)
    
    # 设置日志
    logger = logger_manager.setup_logger(
        "ai_talkshow",
        config_manager.get("logging.file"),
        config_manager.get("logging.level"),
        config_manager.get("logging.max_size"),
        config_manager.get("logging.backup_count")
    )

    logger.info("AI Talkshow starting...")
    
    try:
        # 初始化AI代理
        ai1 = QwenAgent(
            name="ai1",
            config=config_manager.get("debate.topics"),
            model=config_manager.get("models.qwen.model"),
            api_key=config_manager.get_from_env("models.qwen.api_key", "QWEN_API_KEY"),
            voice=config_manager.get("tts.voices.ai1")
        )

        ai2 = QwenAgent(
            name="ai2",
            config=config_manager.config,
            model=config_manager.get("models.qwen.model"),
            api_key=config_manager.get_from_env("models.qwen.api_key", "QWEN_API_KEY"),
            voice=config_manager.get("tts.voices.ai2")
        )
        
        # 创建辩论管理器
        debate_manager = DebateManager(ai1, ai2, config_manager.config)
        
        # 运行辩论
        debate_manager.run_debate()
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
