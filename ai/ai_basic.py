import asyncio
from abc import abstractmethod

from ai.utils import MultiRoundQuestionAnswer
from common.vts import vts_authenticate


class AiBasic:

    def __init__(self, model, api_key, round_count, system_role, tts=None, vts_port=None):
        self.model = model
        self.api_key = api_key
        self.mrqa = MultiRoundQuestionAnswer(round_count, system_role)
        print(
            f"TongYiOnline inited, model: {self.model}, round_count: {self.mrqa.round_count}, system_role: {self.mrqa.system_role}")
        if tts is not None:
            self.tts = tts
            self.tts.modify_vtt_file(f'WEBVTT\n00:00:00.100 --> 00:00:03.900\n...')
        if vts_port is not None:
            self.vts_port = vts_port
            asyncio.run(vts_authenticate(vts_port))

    @abstractmethod
    def create_chat_completion(self, question):
        pass

    def generate_question(self, message):
        return self.create_chat_completion(message)

    def generate_answer(self, message):
        return self.create_chat_completion(message)

    def speak(self, text):
        if self.tts is not None:
            self.activate_subtitle()
            self.tts.speak(text, self.vts_port)

    def activate_subtitle(self):
        if self.tts is not None:
            self.tts.modify_vtt_file(f'CLASS\nonline')

    def deactivate_subtitle(self):
        if self.tts is not None:
            self.tts.modify_vtt_file(f'CLASS\noffline')

    def send_subtitle(self, message):
        if self.tts is not None:
            self.activate_subtitle()
            self.tts.modify_vtt_file(f'WEBVTT\n00:00:00.100 --> 00:00:03.900\n{message}')
