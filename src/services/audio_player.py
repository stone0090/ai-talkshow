import asyncio
import pygame
from src.utils.logger import logger_manager

logger = logger_manager.get_logger(f"audio_player")

async def play_voice(audio_path):
    """
    异步播放音频文件。

    :param audio_path: 音频文件的路径
    """
    logger.info(f"[{audio_path}] playing audio...")
    loop = asyncio.get_event_loop()

    def play_sync():
        """
        同步播放音频文件，使用 pygame 模块。
        确保在播放完成后释放资源。
        """
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(1)
        finally:
            pygame.mixer.quit()  # 确保资源释放

    logger.info("[{audio_path}] audio playback completed...")
    await loop.run_in_executor(None, play_sync)



def main():
    audio_path = "tmp/ai1.mp3"
    asyncio.run(play_voice(audio_path))


if __name__ == "__main__":
    main()
