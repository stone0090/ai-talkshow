from llm_chatglm import ChatGLM
from llm_tongyi import TongYi
from tts import TTS

topic = "考公是不是应届生最好的选择？"
topic1 = "考公是应届生最好的选择"
topic2 = "考公不是应届生最好的选择"

tongyi = TongYi("qwen-max", "", 5,
                f'你是辩论机器人tongyi，今天你要讨论的主题是[{topic}]，你的观点是[{topic1}]，反方观点是[{topic2}]，你的任务是在这场辩论赛中赢得胜利。')
tongyi_tts = TTS("zh-CN-XiaoxiaoNeural", "tmp/tts_tongyi.mp3", "tmp/tts_tongyi.vtt")

glm = ChatGLM("chatglm3-6b", "http://127.0.0.1:8000", 5,
              f'你是辩论机器人glm，今天你要讨论的主题是[{topic}]，你的观点是[{topic2}]，反方观点是[{topic1}]，你的任务是在这场辩论赛中赢得胜利。')
glm_tts = TTS("zh-CN-XiaoyiNeural", "tmp/tts_glm.mp3", "tmp/tts_glm.vtt")

turn = 1  # 初始化轮次

while True:
    if turn % 2 == 1:
        # AI1 提问，AI2 回答
        question = glm.generate_question(topic2, topic1)
        print(f'glm question: {question}')
        glm_tts.speak(question)
        answer = tongyi.generate_answer(topic1, question)
        print(f'tongyi answer: {answer}')
        tongyi_tts.speak(answer)
        print('\n')
    else:
        # AI2 提问，AI1 回答
        question = tongyi.generate_question(topic1, topic2)
        print(f'tongyi question: {question}')
        tongyi_tts.speak(question)
        answer = glm.generate_answer(topic2, question)
        print(f'glm answer: {answer}')
        glm_tts.speak(answer)
        print('\n')

    turn += 1

    # 可以添加一些终止对话的条件，例如达到一定轮次或特定的结束信号
    if turn > 100:
        break
