import asyncio
import os
import edge_tts
import json
from typing import Optional, Tuple
from src.utils.logger import logger_manager
from src.services.vts import VTSService
from src.services.audio_player import play_voice
from src.services.subtitle import calculate_mouth_open_duration


class TTSService:
    def __init__(self, agent_code: str, voice: str):
        self.logger = logger_manager.get_logger(f"tts_service.{agent_code}")
        self.agent_code = agent_code
        self.voice = voice
        self.tmp_path = "tmp"
        self.output_prefix = agent_code
        # self.output_prefix = f"{agent_code}_{os.urandom(4).hex()}"
        self._ensure_directories()

    async def synthesize(self, text: str) -> Tuple[str, str]:
        """合成语音和字幕
        
        Args:
            text: 要合成的文本
        
        Returns:
            tuple: 包含音频文件路径和字幕文件路径的元组
        """
        # 获取临时文件路径，清理临时文件
        audio_path, vtt_path = self._get_tmp_file_path()
        self._cleanup_tmp_file()

        try:
            self.logger.debug(f"Synthesizing speech for text: {text[:10]}...")

            async def generate_audio_async() -> None:
                communicate = edge_tts.Communicate(text, self.voice)
                await communicate.save(audio_path, vtt_path)

            await generate_audio_async()
            self.logger.debug(f"Speech synthesis completed: audio saved to {audio_path}, subtitles saved to {vtt_path}")

            # 将 vtt 文件中的 text 字段转换为中文
            self._convert_vtt_text_to_chinese(vtt_path)

            return audio_path, vtt_path
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
            # 根据操作系统选择路径分隔符
            audio_path, vtt_path = self._get_tmp_file_path()
            if os.path.exists(audio_path):
                os.remove(audio_path)
            if os.path.exists(vtt_path):
                os.remove(vtt_path)
        except Exception as e:
            self.logger.error(f"Error in _init_audio_and_vtt_file: {e}")
            raise


async def main():
    """测试函数"""
    # 创建两个TTS服务实例，使用不同的语音
    tts1 = TTSService("ai1", "zh-CN-XiaoxiaoNeural")
    vts1 = VTSService("ai1", 8001)
    test_text1 = "你好，我是小千，很高兴认识你！"
    audio_path1, vtt_path1 = await tts1.synthesize(test_text1)
    await vts1.authenticate()
    print(f"ai1 生成结果:")
    print(f"音频文件: {audio_path1}")
    print(f"字幕文件: {vtt_path1}")

    # 修改这里：使用await代替嵌套的asyncio.run
    await asyncio.gather(
        play_voice(audio_path1),
        vts1.open_mouth(calculate_mouth_open_duration(vtt_path1))
    )

    tts2 = TTSService("ai2", "zh-CN-XiaoyiNeural")
    vts2 = VTSService("ai2", 8002)
    test_text2 = "你好，我是小问，今天我们来讨论一个有趣的话题。"
    audio_path2, vtt_path2 = await tts2.synthesize(test_text2)
    await vts2.authenticate()
    print(f"ai2 生成结果:")
    print(f"音频文件: {audio_path2}")
    print(f"字幕文件: {vtt_path2}")

    # 修改这里：直接使用await
    await asyncio.gather(
        play_voice(audio_path2),
        vts2.open_mouth(calculate_mouth_open_duration(vtt_path2))
    )


if __name__ == "__main__":
    asyncio.run(main())
