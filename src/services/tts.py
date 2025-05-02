import os
from typing import Optional, Tuple
from src.utils.logger import get_logger

class TTSService:
    def __init__(self, config: dict):
        self.config = config
        self.logger = get_logger("tts_service")
        self.media_path = config.get("tts.media_path", "tmp")
        self.vtt_path = config.get("tts.vtt_path", "tmp")
        self._ensure_directories()
    
    def _ensure_directories(self) -> None:
        """确保必要的目录存在"""
        for path in [self.media_path, self.vtt_path]:
            if not os.path.exists(path):
                os.makedirs(path)
                self.logger.info(f"Created directory: {path}")
    
    def synthesize(self, text: str, voice: str, output_prefix: str) -> Tuple[str, str]:
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
            # 生成音频文件路径
            audio_path = os.path.join(self.media_path, f"{output_prefix}.mp3")
            vtt_path = os.path.join(self.vtt_path, f"{output_prefix}.vtt")
            
            # TODO: 实现具体的TTS合成逻辑
            # 这里需要根据实际的TTS服务实现具体的合成逻辑
            
            self.logger.info(f"Generated audio: {audio_path}")
            self.logger.info(f"Generated subtitle: {vtt_path}")
            
            return audio_path, vtt_path
            
        except Exception as e:
            self.logger.error(f"Error in TTS synthesis: {e}")
            raise
    
    def cleanup(self, prefix: Optional[str] = None) -> None:
        """
        清理生成的文件
        
        Args:
            prefix: 要清理的文件前缀，如果为None则清理所有文件
        """
        try:
            if prefix:
                files_to_remove = [
                    os.path.join(self.media_path, f"{prefix}.mp3"),
                    os.path.join(self.vtt_path, f"{prefix}.vtt")
                ]
            else:
                files_to_remove = []
                for path in [self.media_path, self.vtt_path]:
                    for file in os.listdir(path):
                        if file.endswith(('.mp3', '.vtt')):
                            files_to_remove.append(os.path.join(path, file))
            
            for file in files_to_remove:
                if os.path.exists(file):
                    os.remove(file)
                    self.logger.info(f"Removed file: {file}")
                    
        except Exception as e:
            self.logger.error(f"Error in cleanup: {e}")
            raise 