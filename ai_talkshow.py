from ai.chatglm import ChatGLM
from ai.qwen_online import QwenOnline
from config import CHAT_GLM_SERVER_URL, TONGYI_API_KEY
from common.tts import TTS

topic = "考公是应届生最好的选择吗？"
ai1_topic = "考公是应届生最好的选择！"
ai2_topic = "考公不是应届生最好的选择！"

ai1 = QwenOnline(model="qwen-plus-0112",
                 api_key=TONGYI_API_KEY,
                 round_count=5,
                 system_role=f'你是辩论机器人ai1，今天你要讨论的主题是[{topic}]，你支持的观点是[{ai1_topic}]，你反方的观点是[{ai2_topic}]，你的任务是在这场辩论赛中赢得胜利！',
                 tts=TTS(voice="zh-CN-XiaoxiaoNeural", media_path="tmp/ai1.mp3", vtt_path="tmp/ai1.vtt"),
                 #vts_port=8001)
                 )

ai2 = QwenOnline(model="qwen-plus-1220",
                 api_key=TONGYI_API_KEY,
                 round_count=5,
                 system_role=f'你是辩论机器人ai2，今天你要讨论的主题是[{topic}]，你支持的观点是[{ai2_topic}]，你反方的观点是[{ai1_topic}]，你的任务是在这场辩论赛中赢得胜利！',
                 tts=TTS(voice="zh-CN-XiaoyiNeural", media_path="tmp/ai2.mp3", vtt_path="tmp/ai2.vtt"),
                 #vts_port=8002)
                 )

def question_and_answer(ai1, ai2):
    # ai1 提问
    ai2.deactivate_subtitle()
    ai1.speak('下面由我来提问')
    ai1_question = ai1.generate_question(f'你的观点是[{ai1_topic}]，反方的观点是[{ai2_topic}]，请肯定自己的观点，并提出反驳对方辩友观点的问题，无需询问我，请直接给出问题，字数不要超过100字。')
    print(f'ai1 question: {ai1_question}')
    ai1.speak(ai1_question)
    print('\n')
    # ai2 回答
    ai1.deactivate_subtitle()
    ai2.send_subtitle('正在思考中...')
    ai2_answer = ai2.generate_answer(f'你的观点是[{ai2_topic}]，请回答[{ai1_question}]，字数不要超过100字。')
    print(f'ai2 answer: {ai2_answer}')
    ai2.speak(ai2_answer)
    print('\n')


def start():
    turn = 1  # 初始化轮次
    while True:
        if turn % 2 == 1:
            # ai1 提问，ai2 回答
            question_and_answer(ai1, ai2)
        else:
            # ai2 提问，ai1 回答
            question_and_answer(ai2, ai1)
        turn += 1
        # 可以添加一些终止对话的条件，例如达到一定轮次或特定的结束信号
        if turn > 5:
            break


if __name__ == "__main__":
    start()
