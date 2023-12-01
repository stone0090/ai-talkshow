import os
import subprocess
import pygame


class TTS:
    def __init__(self, voice, media_path, vtt_path=None):
        self.voice = voice
        self.mp3_path = media_path
        self.vtt_path = vtt_path

    def speak(self, text):
        if text is None:
            return
        text = text.replace("\n", "")
        if os.path.exists(self.mp3_path):
            os.remove(self.mp3_path)
        command = f'edge-tts --voice {self.voice} --write-media {self.mp3_path}  --text "{text}" '
        if self.vtt_path is not None:
            if os.path.exists(self.vtt_path):
                with open(self.vtt_path, 'w') as file:
                    file.truncate()
            command = command + f" --write-subtitles {self.vtt_path} "
        subprocess.run(command, shell=True)  # 执行命令行指令
        pygame.mixer.init()
        pygame.mixer.music.load(self.mp3_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(1)
        pygame.mixer.quit()


if __name__ == "__main__":
    # 女声
    female_tts1 = TTS("zh-CN-XiaoxiaoNeural", "tmp/ai1.mp3", "tmp/ai1.vtt")
    female_tts1.speak("你好，请问有什么可以帮到您？")

    female_tts2 = TTS("zh-CN-XiaoyiNeural", "tmp/ai1.mp3", "tmp/ai1.vtt")
    female_tts2.speak("你好，请问有什么可以帮到您？")

    female_tts3 = TTS("zh-CN-liaoning-XiaobeiNeural", "tmp/ai1.mp3", "tmp/ai1.vtt")
    female_tts3.speak("你好，请问有什么可以帮到您？")

    female_tts4 = TTS("zh-CN-shaanxi-XiaoniNeural", "tmp/ai1.mp3", "tmp/ai1.vtt")
    female_tts4.speak("你好，请问有什么可以帮到您？")

    female_tts5 = TTS("zh-TW-HsiaoChenNeural", "tmp/ai1.mp3", "tmp/ai1.vtt")
    female_tts5.speak("你好，请问有什么可以帮到您？")

    female_tts6 = TTS("zh-TW-HsiaoYuNeural", "tmp/ai1.mp3", "tmp/ai1.vtt")
    female_tts6.speak("你好，请问有什么可以帮到您？")

    # 男声
    male_tts1 = TTS("zh-CN-YunjianNeural", "tmp/ai2.mp3", "tmp/ai2.vtt")
    male_tts1.speak("你好，请问有什么可以帮到您？")

    male_tts2 = TTS("zh-CN-YunxiNeural", "tmp/ai2.mp3", "tmp/ai2.vtt")
    male_tts2.speak("你好，请问有什么可以帮到您？")

    male_tts3 = TTS("zh-CN-YunxiaNeural", "tmp/ai2.mp3", "tmp/ai2.vtt")
    male_tts3.speak("你好，请问有什么可以帮到您？")

    male_tts4 = TTS("zh-CN-YunyangNeural", "tmp/ai2.mp3", "tmp/ai2.vtt")
    male_tts4.speak("你好，请问有什么可以帮到您？")

    male_tts5 = TTS("zh-TW-YunJheNeural", "tmp/ai2.mp3", "tmp/ai2.vtt")
    male_tts5.speak("你好，请问有什么可以帮到您？")
