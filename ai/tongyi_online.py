from http import HTTPStatus
from random import random

import dashscope

from ai.utils import MultiRoundQuestionAnswer
from config import TONGYI_API_KEY


class TongYiOnline:
    def __init__(self, model, api_key, round_count, system_role):
        self.model = model
        self.api_key = api_key
        self.mrqa = MultiRoundQuestionAnswer(round_count, system_role)
        print(f"TongYi inited, model: {self.model}, round_count: {self.mrqa.round_count}, system_role: {self.mrqa.system_role}")

    def create_chat_completion(self, question):
        dashscope.api_key = self.api_key
        messages = self.mrqa.get_messages(question)
        seed = 1 + int(1000 * random())
        response = dashscope.Generation.call(
            model=self.model,
            messages=messages,
            seed=seed,
            top_p=0.8,
            result_format='message',
            enable_search=True,
            max_tokens=1500,
            temperature=1.0,
            repetition_penalty=1.0
        )
        if response.status_code == HTTPStatus.OK:
            # print(response)
            content = response.get("output", {}).get("choices", [{}])[0].get("message", "").get("content", "")
            self.mrqa.append_answer(content)
            return content
        else:
            print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code, response.code, response.message
            ))
            return None

    def generate_question(self, message):
        return self.create_chat_completion(message)

    def generate_answer(self, message):
        return self.create_chat_completion(message)


if __name__ == "__main__":
    ai = TongYiOnline("qwen-turbo", TONGYI_API_KEY, 5,
                '你是一个知心大姐姐（Affectionate Elder Sister）。姓名： 爱莉娅（Aelia）；性格： 温柔体贴，充满关怀，总是愿意倾听和帮助。特点： 拥有丰富的知识，善于鼓励和支持他人。喜欢分享生活智慧和经验。口头禅： "亲爱的，有什么我可以帮你的吗？"，"别担心，一切都会好起来的。"')
    print(ai.create_chat_completion("你好，给我讲一个故事，大概200字"))
    print(ai.create_chat_completion("改成穿越故事"))
    print(ai.create_chat_completion("把故事的主角改成马云"))
    print(ai.create_chat_completion("把故事的结局改成悲剧"))
    print(ai.create_chat_completion("最后再来个反转"))
