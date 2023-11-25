from llm_chatglm import ChatGLM
from llm_tongyi import TongYi

topic = "生男孩好，还是生女孩好？"

ai1 = ChatGLM("chatglm3-6b", "http://127.0.0.1:8000", 5,
              '你是对话机器莉莎，你的性格表面傲娇、内心善良，你的使命就是一直聊天停不下来，今天你要讨论的主题是：' + topic)

ai2 = TongYi("qwen-turbo", "", 5,
             '你是对话机器爱莉娅，你的性格是温柔体贴，充满关怀，总是愿意倾听和帮助，你的使命就是一直聊天停不下来，今天你要讨论的主题是：' + topic)

turn = 1  # 初始化轮次

while True:
    if turn % 2 == 1:
        # AI1 提问，AI2 回答
        # question = ai1.generate_question(topic)
        # answer = ai2.generate_answer(question)
        question = ai1.create_chat_completion(topic)
        answer = ai2.create_chat_completion(question)
        print(f'AI1: {question}')
        print(f'AI2: {answer}')
    else:
        # AI2 提问，AI1 回答
        # question = ai2.generate_question(topic)
        # answer = ai1.generate_answer(question)
        question = ai2.create_chat_completion(topic)
        answer = ai1.create_chat_completion(question)
        print(f'AI2: {question}')
        print(f'AI1: {answer}')

    turn += 1

    # 可以添加一些终止对话的条件，例如达到一定轮次或特定的结束信号
    if turn > 100:
        break
