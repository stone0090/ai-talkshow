from typing import Optional
from src.core.ai_agent import AIAgent
from src.utils.logger import logger_manager

class DebateManager:
    def __init__(self, ai1: AIAgent, ai2: AIAgent, config: dict):
        self.ai1 = ai1
        self.ai2 = ai2
        self.config = config
        # 使用日志管理器获取 logger
        self.logger = logger_manager.get_logger("debate_manager")
        self.current_turn = 0
        self.max_turns = config.get("debate.max_turns", 5)
        self.topic = config.get("debate.topics.main", "")
        self.ai1_topic = config.get("debate.topics.ai1", "")
        self.ai2_topic = config.get("debate.topics.ai2", "")
        
        # 设置AI代理的系统提示
        self.ai1_system_prompt = (
            f"你是辩论机器人{ai1.name}，今天你要讨论的主题是[{self.topic}]，"
            f"你支持的观点是[{self.ai1_topic}]，"
            f"你反方的观点是[{self.ai2_topic}]，"
            "你的任务是在这场辩论赛中赢得胜利！"
        )
        self.ai2_system_prompt = (
            f"你是辩论机器人{ai2.name}，今天你要讨论的主题是[{self.topic}]，"
            f"你支持的观点是[{self.ai2_topic}]，"
            f"你反方的观点是[{self.ai1_topic}]，"
            "你的任务是在这场辩论赛中赢得胜利！"
        )
    
    def _execute_turn(self) -> None:
        """执行一轮辩论"""
        if self.current_turn % 2 == 0:
            # AI1提问，AI2回答
            self._question_and_answer(self.ai1, self.ai2, self.ai1_system_prompt, self.ai2_system_prompt)
        else:
            # AI2提问，AI1回答
            self._question_and_answer(self.ai2, self.ai1, self.ai2_system_prompt, self.ai1_system_prompt)
    
    def _question_and_answer(
        self,
        questioner: AIAgent,
        responder: AIAgent,
        questioner_system_prompt: str,
        responder_system_prompt: str
    ) -> None:
        """执行问答环节"""
        try:
            # 提问者生成问题
            question_prompt = (
                "请肯定自己的观点，并提出反驳对方辩友观点的问题。"
                "如果没有历史回答记录，请直接根据当前辩题给出一个新问题。"
                "无需询问我，请直接给出问题，字数不要超过100字。"
            )
            question = questioner.generate_response(question_prompt, questioner_system_prompt)
            self.logger.info(f"{questioner.name} question: {question}")
            questioner.speak(question)
            
            # 回答者生成回答
            responder.deactivate()
            answer_prompt = f"请回答[{question}]，字数不要超过100字。"
            answer = responder.generate_response(answer_prompt, responder_system_prompt)
            self.logger.info(f"{responder.name} answer: {answer}")
            responder.speak(answer)
            
        except Exception as e:
            self.logger.error(f"Error in question and answer: {e}")
            raise
    
    def run_debate(self) -> None:
        """运行整个辩论"""
        self.logger.info(f"Starting debate on topic: {self.topic}")
        while self.current_turn < self.max_turns:
            self.logger.info(f"Starting turn {self.current_turn + 1}")
            self._execute_turn()
            self.current_turn += 1
        self.logger.info("Debate completed")
