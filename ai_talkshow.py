from ai.chatglm import ChatGLM
from ai.tongyi_online import TongYiOnline
from tts import TTS

topic = "考公是应届生最好的选择吗？"
ai1_topic = "考公是应届生最好的选择"
ai2_topic = "考公不是应届生最好的选择"

ai1_tts = TTS("zh-CN-XiaoxiaoNeural", "tmp/ai1.mp3", "tmp/ai1.vtt")
ai1 = TongYiOnline("qwen-max", "sk-b25b47f6cef342038f0d0e1d4ab717c6", 5,
                   f'你是辩论机器人tongyi，今天你要讨论的主题是[{topic}]，'
                   f'你的观点是[{ai1_topic}]，反方观点是[{ai2_topic}]，'
                   f'你的任务是在这场辩论赛中赢得胜利。')

ai2_tts = TTS("zh-CN-XiaoyiNeural", "tmp/ai2.mp3", "tmp/ai2.vtt")
ai2 = ChatGLM("chatglm3-6b", "http://127.0.0.1:8000", 5,
              f'你是辩论机器人glm，今天你要讨论的主题是[{topic}]，'
              f'你的观点是[{ai2_topic}]，反方观点是[{ai1_topic}]，'
              f'你的任务是在这场辩论赛中赢得胜利。')


def start():
    turn = 1  # 初始化轮次

    while True:
        if turn % 2 == 1:
            # ai1 提问，ai2 回答
            ai1_question = ai1.generate_question(f'你的观点是[{ai1_topic}]，对方的观点是[{ai2_topic}]'
                                                 f'请提出反驳对方辩友观点的问题，或找出对方回答的漏洞提出质疑'
                                                 f'无需询问我，请直接给出问题，字数不要超过200字。')
            print(f'ai1 question: {ai1_question}')
            ai1_tts.speak(ai1_question)
            ai2_answer = ai2.generate_answer(f'你的观点是[{ai2_topic}]，请回答[{ai1_question}]，字数不要超过200字。')
            print(f'ai2 answer: {ai2_answer}')
            ai2_tts.speak(ai2_answer)
            print('\n')
        else:
            # ai2 提问，ai1 回答
            ai2_question = ai1.generate_question(f'你的观点是[{ai2_topic}]，对方的观点是[{ai1_topic}]'
                                                 f'请提出反驳对方辩友观点的问题，或找出对方回答的漏洞提出质疑'
                                                 f'无需询问我，请直接给出问题，字数不要超过200字。')
            print(f'ai2 question: {ai2_question}')
            ai2_tts.speak(ai2_question)
            ai1_answer = ai2.generate_answer(f'你的观点是[{ai1_topic}]，请回答[{ai2_question}]，字数不要超过200字。')
            print(f'ai1 answer: {ai1_answer}')
            ai1_tts.speak(ai1_answer)
            print('\n')

        turn += 1

        # # 可以添加一些终止对话的条件，例如达到一定轮次或特定的结束信号
        # if turn > 100:
        #     break


if __name__ == "__main__":
    start()
