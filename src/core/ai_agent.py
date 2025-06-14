import asyncio
from abc import ABC, abstractmethod
from typing import Optional, List, Dict
from src.services.tts_service import TTSService
from src.services.vts_service import VTSService
from src.services.vtt_service import VTTService
from src.utils.logger import logger_manager
from src.core.conversation import ConversationHistory


class AIAgent(ABC):
    def __init__(self, agent_code: str, config: dict):
        self.logger = logger_manager.get_logger(f"ai_agent.{agent_code}")
        self.agent_code = agent_code
        self.config = config
        self.nickname = config.get("nickname", agent_code)
        self.system_role = config.get("system_role", agent_code)
        self.max_history = config.get("max_history", 3)
        self.tts_voice = config.get("tts_voice", None)
        self.tts_service = TTSService(agent_code, self.tts_voice) if self.tts_voice else None
        self.vts_port = config.get("vts_port", None)
        self.vts_service = VTSService(agent_code, self.vts_port) if self.vts_port else None
        self.vtt_port = config.get("vtt_port", None)
        self.vtt_service = VTTService(self.tts_service.vtt_path, self.vtt_port) if self.vtt_port else None
        self.conversation = ConversationHistory(self.max_history)
        self.logger.debug("AI agent initialized successfully")

    @abstractmethod
    def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """生成回答"""
        pass

    async def speak(self, text: str) -> None:
        """语音合成和播放声音"""
        if not self.tts_voice or not self.tts_service:
            self.logger.debug("Voice not configured, skipping speech synthesis")
            return

        try:
            self.logger.debug(f"Generating speech for text: {text[:10]}...")
            audio_path, vtt_path = await self.tts_service.synthesize(text=text)

            if self.vts_service is not None and self.vts_service.vts is not None:
                await self.vts_service.authenticate()

            if self.vts_service is not None and self.vts_service.vts is not None:
                if self.vtt_service is not None:
                    await asyncio.gather(
                        self.tts_service.play_voice(audio_path),
                        self.vts_service.open_mouth_by_vtt(vtt_path),
                        self.vtt_service.send_subtitle_by_vtt(vtt_path)
                    )
                else:
                    await asyncio.gather(
                        self.tts_service.play_voice(audio_path),
                        self.vts_service.open_mouth_by_vtt(vtt_path),
                    )
            else:
                if self.vtt_service is not None:
                    await asyncio.gather(
                        self.tts_service.play_voice(audio_path),
                        self.vtt_service.send_subtitle_by_vtt(vtt_path)
                    )
                else:
                    await asyncio.gather(
                        self.tts_service.play_voice(audio_path),
                    )
        except Exception as e:
            self.logger.error(f"Error in speech implementation: {str(e)}", exc_info=True)
            raise

    async def send_subtitle(self, text: str) -> None:
        await self.vtt_service.send_subtitle_by_text(text)

    def get_nickname(self) -> str:
        """获取name"""
        return self.nickname

    def add_to_history(self, role: str, content: str) -> None:
        """添加消息到历史记录"""
        self.conversation.add_message(role, content)

    def get_history(self) -> List[Dict[str, str]]:
        """获取历史记录"""
        return self.conversation.get_history()

    def clear_history(self) -> None:
        """清空历史记录"""
        self.conversation.clear()
