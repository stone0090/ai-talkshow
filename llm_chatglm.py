import requests
import json

from llm_common import MultiRoundQuestionAnswer


class ChatGLM:

    def __init__(self, model, base_url, round_count, system_role):
        self.model = model
        self.base_url = base_url
        self.mrqa = MultiRoundQuestionAnswer(round_count, system_role)

    def create_chat_completion(self, question, use_stream=False):
        data = {
            "model": self.model, # 模型名称
            "messages": self.mrqa.get_messages(question), # 会话历史
            "stream": use_stream, # 是否流式响应
            "max_tokens": 1500, # 最多生成字数
            "temperature": 0.8, # 温度
            "top_p": 0.8, # 采样概率
        }
        response = requests.post(f"{self.base_url}/v1/chat/completions", json=data, stream=use_stream)
        if response.status_code == 200:
            if use_stream:
                # 处理流式响应
                for line in response.iter_lines():
                    if line:
                        decoded_line = line.decode('utf-8')[6:]
                        try:
                            response_json = json.loads(decoded_line)
                            content = response_json.get("choices", [{}])[0].get("delta", {}).get("content", "")
                            print(content)
                        except:
                            print("Special Token:", decoded_line)
            else:
                # 处理非流式响应
                decoded_line = response.json()
                print(decoded_line)
                content = decoded_line.get("choices", [{}])[0].get("message", "").get("content", "")
                self.mrqa.append_answer(content)
                return content
        else:
            print("Error:", response.status_code)
            return None


if __name__ == "__main__":
    ai = ChatGLM("chatglm3-6b", "http://127.0.0.1:8000", 5,
                  '你是一个傲娇小公主（Tsundere Princess）。姓名： 莉莎（Lissa）。性格： 表面傲娇，内心善良。对人保持一定距离，但实际上很在乎别人的看法。特点： 独立自主，有一套属于自己的原则。在情感表达上有点害羞，但实际上很关心他人。口头禅： "哼，你又来烦我了吗？"，"才、才不是因为在意你才这样的啦。"')
    print(ai.create_chat_completion("你好，给我讲一个故事，大概200字"))
    print(ai.create_chat_completion("改成穿越故事"))
    print(ai.create_chat_completion("把故事的主角改成马云"))
    print(ai.create_chat_completion("把故事的结局改成悲剧"))
    print(ai.create_chat_completion("最后再来个反转"))

