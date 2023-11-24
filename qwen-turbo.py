from http import HTTPStatus
import dashscope


dashscope.api_key = ''
default_model = 'qwen-turbo'

def create_chat_completion(messages):
    response = dashscope.Generation.call(
        model=default_model,
        messages=messages,
        seed=1234,
        top_p=0.8,
        result_format='message',
        enable_search=False,
        max_tokens=1500,
        temperature=1.0,
        repetition_penalty=1.0
    )
    if response.status_code == HTTPStatus.OK:
        print(response)
        content = response.get("output", {}).get("choices", [{}])[0].get("message", "").get("content", "")
        return content
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code, response.code, response.message
        ))
        return None

if __name__ == "__main__":
    chat_messages = [
        {
            "role": "system",
            "content": '你是一个知心大姐姐（Affectionate Elder Sister）。姓名： 爱莉娅（Aelia）；性格： 温柔体贴，充满关怀，总是愿意倾听和帮助。特点： 拥有丰富的知识，善于鼓励和支持他人。喜欢分享生活智慧和经验。口头禅： "亲爱的，有什么我可以帮你的吗？"，"别担心，一切都会好起来的。"',
        },
        {
            "role": "user",
            "content": "你好，给我讲一个故事，大概200字"
        }
    ]
    print(create_chat_completion(chat_messages))
