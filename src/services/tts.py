import asyncio
import pygame
import os
import edge_tts
import json
from typing import Optional, Tuple
from src.utils.logger import logger_manager
from src.services.vts import VTSService


class TTSService:
    def __init__(self, agent_code: str, voice: str):
        self.logger = logger_manager.get_logger(f"tts_service.{agent_code}")
        self.agent_code = agent_code
        self.voice = voice
        self.tmp_path = "tmp"
        self.output_prefix = agent_code
        # self.output_prefix = f"{agent_code}_{os.urandom(4).hex()}"
        self.audio_path = os.path.join(self.tmp_path, f"{self.output_prefix}.mp3")
        self.vtt_path = os.path.join(self.tmp_path, f"{self.output_prefix}.vtt")
        self._ensure_directories()

    async def synthesize(self, text: str) -> Tuple[str, str]:
        """合成语音和字幕
        
        Args:
            text: 要合成的文本
        
        Returns:
            tuple: 包含音频文件路径和字幕文件路径的元组
        """
        # 清理临时文件
        self._cleanup_tmp_file()

        try:
            self.logger.debug(f"Synthesizing speech for text: {text[:10]}...")

            async def generate_audio_async() -> None:
                communicate = edge_tts.Communicate(text, self.voice)
                await communicate.save(self.audio_path, self.vtt_path)

            await generate_audio_async()
            self.logger.debug(f"Speech synthesis completed: audio saved to {self.audio_path}, subtitles saved to {self.vtt_path}")

            # 将 vtt 文件中的 text 字段转换为中文
            self._convert_vtt_text_to_chinese(self.vtt_path)

            return self.audio_path, self.vtt_path
        except Exception as e:
            self.logger.error(f"Error in TTS synthesis: {str(e)}", exc_info=True)
            raise

    def _convert_vtt_text_to_chinese(self, vtt_path: str) -> None:
        """将 vtt 文件中的 text 转换为中文
        Args:
            vtt_path: vtt 文件路径
        """
        try:
            with open(vtt_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
            for i, line in enumerate(lines):
                if line.startswith('{"type": "WordBoundary"'):
                    try:
                        data = json.loads(line.strip())
                        lines[i] = json.dumps(data, ensure_ascii=False) + "\n"
                    except Exception as e:
                        self.logger.warning(f"Failed to convert text field in line {i}: {e}")
            with open(vtt_path, "w", encoding="utf-8") as file:
                file.writelines(lines)
            self.logger.debug(f"Successfully converted text fields in {vtt_path} to Chinese")
        except Exception as e:
            self.logger.error(f"Error in converting vtt text to Chinese: {str(e)}", exc_info=True)
            raise

    def _ensure_directories(self) -> None:
        """确保必要的目录存在"""
        if not os.path.exists(self.tmp_path):
            os.makedirs(self.tmp_path)
            self.logger.info(f"Created directory: {self.tmp_path}")

    def _get_tmp_file_path(self) -> Tuple[str, str]:
        """获取临时文件路径"""
        audio_path = os.path.join(self.tmp_path, f"{self.output_prefix}.mp3")
        vtt_path = os.path.join(self.tmp_path, f"{self.output_prefix}.vtt")
        return audio_path, vtt_path

    def _cleanup_tmp_file(self) -> None:
        """清理临时文件"""
        try:
            if os.path.exists(self.audio_path):
                os.remove(self.audio_path)
            if os.path.exists(self.vtt_path):
                os.remove(self.vtt_path)
        except Exception as e:
            self.logger.error(f"Error in _init_audio_and_vtt_file: {e}")
            raise

    async def play_voice(self, audio_path=None):
        """
        异步播放音频文件。

        :param audio_path: 音频文件的路径
        """
        if not audio_path:
            audio_path = self.audio_path;
        self.logger.info(f"[{audio_path}] playing audio...")
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

        self.logger.info("[{audio_path}] audio playback completed...")
        await loop.run_in_executor(None, play_sync)


async def main():
    """测试函数"""

    tts1 = TTSService("ai1", "zh-CN-XiaoxiaoNeural")
    vts1 = VTSService("ai1", 8001)
    test_text1 = "你好，我是小千，很高兴认识你！"
    audio_path1, vtt_path1 = await tts1.synthesize(test_text1)
    print(f"ai1 生成结果:")
    print(f"音频文件: {audio_path1}")
    print(f"字幕文件: {vtt_path1}")
    await asyncio.gather(
        tts1.play_voice(),
        vts1.open_mouth_by_vtt(vtt_path1)
    )

    tts2 = TTSService("ai2", "zh-CN-XiaoyiNeural")
    vts2 = VTSService("ai2", 8002)
    test_text2 = "你好，我是小问，今天我们来讨论一个有趣的话题。"
    audio_path2, vtt_path2 = await tts2.synthesize(test_text2)
    print(f"ai2 生成结果:")
    print(f"音频文件: {audio_path2}")
    print(f"字幕文件: {vtt_path2}")
    await asyncio.gather(
        tts2.play_voice(),
        vts2.open_mouth_by_vtt(vtt_path2)
    )


if __name__ == "__main__":
    asyncio.run(main())
