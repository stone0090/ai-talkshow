import asyncio
import os
import subprocess
import logging
import pygame

from common.utils import list_duration_from_vtt, calculate_total_duration
from common.vts import vts_open_mouth

# 配置日志，设置日志级别为 INFO，格式化日志输出
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


async def play_voice(media_path):
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
            print("开始播放声音")
            pygame.mixer.init()
            pygame.mixer.music.load(media_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(1)
        finally:
            pygame.mixer.quit()  # 确保资源释放

    await loop.run_in_executor(None, play_sync)


async def open_mouth(vtt_path, vts_port):
    """
    根据字幕文件调整嘴型。
    
    :param vtt_path: 字幕文件路径
    :param vts_port: VTS 服务端口
    """
    print("开始变化嘴型")
    subtitles = list_duration_from_vtt(vtt_path)
    total_duration = calculate_total_duration(subtitles)
    await vts_open_mouth(vts_port, total_duration)


async def play_voice_and_open_mouth(media_path, vtt_path, vts_port):
    """
    同时播放音频并调整嘴型。
    
    :param media_path: 音频文件路径
    :param vtt_path: 字幕文件路径
    :param vts_port: VTS 服务端口
    """
    task1 = asyncio.create_task(play_voice(media_path))
    task2 = asyncio.create_task(open_mouth(vtt_path, vts_port))
    await asyncio.gather(task1, task2)


class TTS:
    """
    文本转语音（TTS）类，用于生成语音文件并播放。
    
    :param voice: 语音类型
    :param media_path: 生成的音频文件路径
    :param vtt_path: 生成的字幕文件路径
    """
    def __init__(self, voice, media_path, vtt_path):
        self.voice = voice
        self.media_path = media_path
        self.vtt_path = vtt_path

    def speak(self, text, vts_port=None):
        """
        将文本转换为语音并播放。
        
        :param text: 要转换为语音的文本
        :param vts_port: VTS 服务端口（可选）
        """
        if text is None:
            return

        text = text.replace("\n", "")
        if os.path.exists(self.media_path):
            os.remove(self.media_path)
        if os.path.exists(self.vtt_path):
            with open(self.vtt_path, 'w', encoding='utf-8') as file:
                file.truncate()

        command = f'edge-tts --voice {self.voice} ' \
                  f'--text "{text}" ' \
                  f'--write-media {self.media_path} ' \
                  f'--write-subtitles {self.vtt_path} '

        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"执行命令失败: {e}")
            return

        # 使用 asyncio.run 管理事件循环
        try:
            if vts_port is None:
                asyncio.run(play_voice(self.media_path))
            else:
                asyncio.run(play_voice_and_open_mouth(self.media_path, self.vtt_path, vts_port))
        except Exception as e:
            logging.error(f"播放音频或调整嘴型时发生错误: {e}")

    def modify_vtt_file(self, text):
        """
        修改字幕文件内容。
        
        :param text: 新的字幕内容
        """
        os.makedirs(os.path.dirname(self.vtt_path), exist_ok=True)
        with open(self.vtt_path, 'w', encoding='utf-8') as file:
            file.write(text)


if __name__ == "__main__":
    # 女声示例
    female_tts1 = TTS("zh-CN-XiaoxiaoNeural", "../tmp/ai1.mp3", "../tmp/ai1.vtt")
    female_tts1.speak("你好，请问有什么可以帮到您？")

    female_tts2 = TTS("zh-CN-XiaoyiNeural", "../tmp/ai1.mp3", "../tmp/ai1.vtt")
    female_tts2.speak("你好，请问有什么可以帮到您？")

    female_tts3 = TTS("zh-CN-liaoning-XiaobeiNeural", "../tmp/ai1.mp3", "../tmp/ai1.vtt")
    female_tts3.speak("你好，请问有什么可以帮到您？")

    female_tts4 = TTS("zh-CN-shaanxi-XiaoniNeural", "../tmp/ai1.mp3", "../tmp/ai1.vtt")
    female_tts4.speak("你好，请问有什么可以帮到您？")

    female_tts5 = TTS("zh-TW-HsiaoChenNeural", "../tmp/ai1.mp3", "../tmp/ai1.vtt")
    female_tts5.speak("你好，请问有什么可以帮到您？")

    female_tts6 = TTS("zh-TW-HsiaoYuNeural", "../tmp/ai1.mp3", "../tmp/ai1.vtt")
    female_tts6.speak("你好，请问有什么可以帮到您？")

    # 男声示例
    male_tts1 = TTS("zh-CN-YunjianNeural", "../tmp/ai2.mp3", "../tmp/ai2.vtt")
    male_tts1.speak("你好，请问有什么可以帮到您？")

    male_tts2 = TTS("zh-CN-YunxiNeural", "../tmp/ai2.mp3", "../tmp/ai2.vtt")
    male_tts2.speak("你好，请问有什么可以帮到您？")

    male_tts3 = TTS("zh-CN-YunxiaNeural", "../tmp/ai2.mp3", "../tmp/ai2.vtt")
    male_tts3.speak("你好，请问有什么可以帮到您？")

    male_tts4 = TTS("zh-CN-YunyangNeural", "../tmp/ai2.mp3", "../tmp/ai2.vtt")
    male_tts4.speak("你好，请问有什么可以帮到您？")

    male_tts5 = TTS("zh-TW-YunJheNeural", "../tmp/ai2.mp3", "../tmp/ai2.vtt")
    male_tts5.speak("你好，请问有什么可以帮到您？")
