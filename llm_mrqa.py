class MultiRoundQuestionAnswer:
    def __init__(self, round_count, system_role):
        if round_count < 2:
            round_count = 2
        self.round_count = round_count
        self.system_role = system_role
        self.history_questions_answers = []

    def get_messages(self, question):
        self.history_questions_answers.append(
            {
                "role": "user",
                "content": question
            }
        )
        if len(self.history_questions_answers) > self.round_count * 2:
            self.history_questions_answers.pop(0)
            self.history_questions_answers.pop(0)
        messages = [
            {
                "role": "system",
                "content": self.system_role,
            }
        ]
        messages.extend(self.history_questions_answers)
        return messages

    def append_answer(self, answer):
        self.history_questions_answers.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

    @staticmethod
    def generate_question(agree_topic, against_topic):
        return f'你的观点是[{agree_topic}]，对方的观点是[{against_topic}]' \
               f'请找出对方辩友回答的漏洞提出质疑，或提出反驳对方辩友观点的问题，' \
               f'无需询问我，请直接给出问题，字数不要超过200字。'

    @staticmethod
    def generate_answer(agree_topic, question):
        return f'你的观点是[{agree_topic}]，请回答[{question}]，字数不要超过200字。'
