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
