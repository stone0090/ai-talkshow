import asyncio
import os
import subprocess
import logging
import pygame
from abc import ABC, abstractmethod
from typing import Optional, List, Dict
from src.services.tts import TTSService
from src.utils.logger import logger_manager
from src.core.conversation import ConversationHistory

class AIAgent(ABC):
    def __init__(self, name: str, config: dict):
        self.logger = logger_manager.get_logger(f"ai_agent.{name}")
        self.name = name
        self.config = config
        self.voice = config.get("voice", "zh-CN-XiaoxiaoNeural")
        self.tts_service = TTSService(name, self.voice)
        self.conversation = ConversationHistory()
    
    @abstractmethod
    def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """生成回答"""
        pass
    
    def speak(self, text: str) -> None:
        """语音合成和播放声音"""
        try:
            audio_path, vtt_path = self.tts_service.synthesize(text=text)
            asyncio.run(_play_voice(audio_path))
            # self.tts_service.modify_vtt_file(text)
            return
        except Exception as e:
            self.logger.error(f"Error in speech implementation: {e}")
            raise

    def add_to_history(self, role: str, content: str) -> None:
        """添加消息到历史记录"""
        self.conversation.add_message(role, content)
    
    def get_history(self) -> List[Dict[str, str]]:
        """获取历史记录"""
        return self.conversation.get_history()
    
    def clear_history(self) -> None:
        """清空历史记录"""
        self.conversation.clear()

async def _play_voice(media_path):
    """
    异步播放音频文件。

    :param media_path: 音频文件的路径
    """
    loop = asyncio.get_event_loop()

    def play_sync():
        """
        同步播放音频文件，使用 pygame 模块。
        确保在播放完成后释放资源。
        """
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(media_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(1)
        finally:
            pygame.mixer.quit()  # 确保资源释放

    await loop.run_in_executor(None, play_sync)