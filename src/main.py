import asyncio
import os
import yaml
import subprocess
from src.core.debate import DebateManager
from src.models.qwen import QwenAgent
from src.utils.logger import logger_manager
from src.services.bilibili_service import BilibiliService


def load_config() -> dict:
    config_path = os.path.join(os.path.dirname(__file__), "..", "config", "config.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def setup_logging(config: dict) -> None:
    logging_config = config.get("logging", {})
    # 设置全局日志配置
    logger_manager.set_config(logging_config)
    # 创建主logger
    logger_manager.setup_logger("ai_talkshow")


def start_static_server(logger, static_server_config):
    try:
        port = static_server_config.get("port", {})
        root = static_server_config.get("root", {})
        process = subprocess.Popen(
            ["python", "-m", "http.server", port, "--directory", root],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        logger.info(f"Static file server started successfully: http://localhost:{port}")
        return process
    except Exception as e:
        logger.error(f"Error in start_static_server: {str(e)}")
        return None


async def main_async():
    # 加载配置
    config = load_config()
    logger = logger_manager.get_logger(__name__)
    logger.debug("Configuration loaded successfully")

    # 设置日志
    setup_logging(config)
    logger.debug("Logging system initialized")

    # 启动静态文件服务器
    static_server_config = config.get("static_server", {})
    static_server = start_static_server(logger, static_server_config)
    if not static_server:
        logger.warning(f"static_server initializing failed!")

    # 初始化bilibili弹幕服务
    bilibili_config = config.get("bilibili", {})
    logger.debug(f"Initializing bilibili service with config: {bilibili_config}")
    bilibili = BilibiliService(bilibili_config)

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
        debate_manager = DebateManager(debate_config, bilibili)
        debate_manager.initialize_agents(ai1, ai2)

        # 开始辩论
        logger.info("Starting debate session")
        # await debate_manager.run_debate()
        await asyncio.gather(
            bilibili.start(),
            debate_manager.run_debate()
        )
        logger.info("Debate session completed")

    except Exception as e:
        logger.error(f"Error in main: {str(e)}", exc_info=True)
        raise
    finally:
        if static_server:
            static_server.terminate()
            static_server.wait()
        if bilibili:
            await bilibili.stop()


def main():
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
