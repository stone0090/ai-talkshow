import os
import asyncio
import os
import subprocess
import pygame
from typing import Optional, Tuple
from src.utils.logger import logger_manager

class TTSService:
    def __init__(self, name: str, voice: str):
        self.logger = logger_manager.get_logger(f"tts_service.{name}")
        self.name = name
        self.voice = voice
        self.tmp_path = "tmp"
        self.output_prefix = name
        # self.output_prefix = f"{name}_{os.urandom(4).hex()}"
        self._ensure_directories()

    def synthesize(self, text: str) -> Tuple[str, str]:
        """
        合成语音并生成字幕
        
        Args:
            text: 要合成的文本
            voice: 语音名称
            output_prefix: 输出文件前缀
            
        Returns:
            tuple: (音频文件路径, 字幕文件路径)
        """
        try:
            # 获取临时文件路径，清理临时文件
            audio_path, vtt_path = self._get_tmp_file_path()
            self._cleanup_tmp_file()

            # 替换换行符，确保文本没有换行符，否则生成音频失败
            text = text.replace("\n", "")

            # 具体的TTS合成逻辑
            command = f'edge-tts --voice {self.voice} ' \
                      f'--text "{text}" ' \
                      f'--write-media {audio_path} ' \
                      f'--write-subtitles {vtt_path} '
            self.logger.info(f"Running command: {command}")
            subprocess.run(command, shell=True, check=True)

            self.logger.info(f"Generated audio: {audio_path}")
            self.logger.info(f"Generated subtitle: {vtt_path}")
            
            return audio_path, vtt_path
        except Exception as e:
            self.logger.error(f"Error in TTS synthesis: {e}")
            raise

    def _ensure_directories(self) -> None:
        """确保必要的目录存在"""
        for path in [self.tmp_path]:
            if not os.path.exists(path):
                os.makedirs(path)
                self.logger.info(f"Created directory: {path}")

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
