import os
import subprocess

import pygame

from subtitles import Subtitles


class TTS:
    def __init__(self, voice, media_path, vtt_path=None, subtitles_server_port=None):
        self.voice = voice
        self.mp3_path = media_path
        self.vtt_path = vtt_path
        if subtitles_server_port is not None:
            Subtitles(self.vtt_path, subtitles_server_port)

    def speak(self, text):
        text = text.replace("\n", "")
        if os.path.exists(self.mp3_path):
            os.remove(self.mp3_path)
        command = f'edge-tts --voice {self.voice} --write-media {self.mp3_path}  --text "{text}" '
        if self.vtt_path is not None:
            if os.path.exists(self.vtt_path):
                os.remove(self.vtt_path)
            command = command + f" --write-subtitles {self.vtt_path} "
        subprocess.run(command, shell=True)  # 执行命令行指令
        pygame.mixer.init()
        pygame.mixer.music.load(self.mp3_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(1)
        pygame.mixer.quit()


if __name__ == "__main__":
    female_tts1 = TTS("zh-CN-XiaoxiaoNeural", "tmp/tts_test.mp3", 8765)
    female_tts1.speak("对方辩友认为“在中国考公务员是最好的选择”，那么请您说明一下您的观点如何能在公务员岗位上更好地发挥价值？")

    # # 女声
    # female_tts1 = TTS("zh-CN-XiaoxiaoNeural", "tts_test.mp3")
    # female_tts1.speak("你好，请问有什么可以帮到您？")
    #
    # female_tts2 = TTS("zh-CN-XiaoyiNeural", "tts_test.mp3")
    # female_tts2.speak("你好，请问有什么可以帮到您？")
    #
    # female_tts3 = TTS("zh-CN-liaoning-XiaobeiNeural", "tts_test.mp3")
    # female_tts3.speak("你好，请问有什么可以帮到您？")
    #
    # female_tts4 = TTS("zh-CN-shaanxi-XiaoniNeural", "tts_test.mp3")
    # female_tts4.speak("你好，请问有什么可以帮到您？")
    #
    # female_tts5 = TTS("zh-TW-HsiaoChenNeural", "tts_test.mp3")
    # female_tts5.speak("你好，请问有什么可以帮到您？")
    #
    # female_tts6 = TTS("zh-TW-HsiaoYuNeural", "tts_test.mp3")
    # female_tts6.speak("你好，请问有什么可以帮到您？")
    #
    # # 男声
    # male_tts1 = TTS("zh-CN-YunjianNeural", "tts_test.mp3")
    # male_tts1.speak("你好，请问有什么可以帮到您？")
    #
    # male_tts2 = TTS("zh-CN-YunxiNeural", "tts_test.mp3")
    # male_tts2.speak("你好，请问有什么可以帮到您？")
    #
    # male_tts3 = TTS("zh-CN-YunxiaNeural", "tts_test.mp3")
    # male_tts3.speak("你好，请问有什么可以帮到您？")
    #
    # male_tts4 = TTS("zh-CN-YunyangNeural", "tts_test.mp3")
    # male_tts4.speak("你好，请问有什么可以帮到您？")
    #
    # male_tts5 = TTS("zh-TW-YunJheNeural", "tts_test.mp3")
    # male_tts5.speak("你好，请问有什么可以帮到您？")
