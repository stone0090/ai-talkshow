import asyncio
import time
import os
import subprocess

import pygame

from common.utils import parse_webvtt, calculate_duration
from common.vts import vts_open_mouth


async def play_voice(media_path):
    await asyncio.sleep(1.2)
    loop = asyncio.get_event_loop()

    def play_sync():
        print("开始播放声音")
        pygame.mixer.init()
        pygame.mixer.music.load(media_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(1)
        pygame.mixer.quit()

    # 在事件循环的不同线程中运行Pygame的操作
    await loop.run_in_executor(None, play_sync)


async def open_mouth(vtt_path, vts_port):
    print("开始变化嘴型")
    subtitles = parse_webvtt(vtt_path)
    total_duration = calculate_duration(subtitles)
    await vts_open_mouth(vts_port, total_duration)


async def play_voice_and_open_mouth(media_path, vtt_path, vts_port):
    task2 = asyncio.create_task(open_mouth(vtt_path, vts_port))
    task1 = asyncio.create_task(play_voice(media_path))
    await asyncio.gather(task1, task2)


class TTS:
    def __init__(self, voice, media_path, vtt_path):
        self.voice = voice
        self.media_path = media_path
        self.vtt_path = vtt_path

    def speak(self, text, vts_port=None):
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
        command = command + f" --write-subtitles {self.vtt_path} "
        subprocess.run(command, shell=True)  # 执行命令行指令
        if vts_port is None:
            asyncio.run(play_voice(self.media_path))
        else:
            asyncio.run(play_voice_and_open_mouth(self.media_path, self.vtt_path, vts_port))
        time.sleep(0.2)

    def modify_vtt_file(self, text):
        with open(self.vtt_path, 'w', encoding='utf-8') as file:
            file.write(text)
        time.sleep(0.2)


if __name__ == "__main__":
    # 女声
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

    # 男声
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
