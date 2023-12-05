from abc import abstractmethod

from ai.utils import MultiRoundQuestionAnswer


class AiBasic:

    def __init__(self, model, api_key, round_count, system_role, tts=None):
        self.model = model
        self.api_key = api_key
        self.mrqa = MultiRoundQuestionAnswer(round_count, system_role)
        print(
            f"TongYiOnline inited, model: {self.model}, round_count: {self.mrqa.round_count}, system_role: {self.mrqa.system_role}")
        self.tts = tts
        if self.tts is not None:
            self.tts.modify_vtt_file(f'WEBVTT\n00:00:00.100 --> 00:00:03.900\n...')

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
            self.tts.speak(text)

    def speak_with_cache(self, text, media_path, vtt_path):
        if self.tts is not None:
            self.activate_subtitle()
            self.tts.speak_with_cache(text, media_path, vtt_path)

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
