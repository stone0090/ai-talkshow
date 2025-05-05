from typing import Optional, List, Tuple
from src.core.ai_agent import AIAgent
from src.utils.logger import logger_manager

class DebateManager:
    def __init__(self, config: dict):
        self.config = config
        self.logger = logger_manager.get_logger(__name__)
        self.logger.debug(f"Initializing debate manager with config: {config}")
        
        # 获取辩论配置
        self.max_turns = config.get("max_turns", 5)
        self.topics = config.get("topics", {})
        self.logger.debug(f"Debate configuration: max_turns={self.max_turns}, topics={self.topics}")
        
        # 初始化AI代理
        self.ai1: Optional[AIAgent] = None
        self.ai2: Optional[AIAgent] = None
        self.current_turn = 0
        self.history: List[Tuple[str, str]] = []

    def initialize_agents(self, ai1: AIAgent, ai2: AIAgent) -> None:
        """初始化AI代理"""
        self.ai1 = ai1
        self.ai2 = ai2
        self.logger.info("AI agents initialized")
        self.logger.debug(f"AI1: {ai1.nickname}, AI2: {ai2.nickname}")

    def start_debate(self) -> None:
        """开始辩论"""
        if not self.ai1 or not self.ai2:
            self.logger.error("AI agents not initialized")
            raise ValueError("AI agents not initialized")
        
        self.logger.info(f"Starting debate on topic: {self.topics.get('main', '')}")
        self.current_turn = 0
        self.history = []
        self.logger.debug("Debate history initialized")

        self.logger.info("Debate started with opening statements")
        self.logger.debug(f"AI1 stance: {self.topics.get('ai1', '')}")
        self.logger.debug(f"AI2 stance: {self.topics.get('ai2', '')}")

        # 生成开场白
        try:
            opening1 = self.ai1.generate_response("请发表你的开场白", self._get_system_prompt(self.ai1))
            self.logger.debug(f"AI1 opening statement generated: {opening1[:100]}...")
            
            opening2 = self.ai2.generate_response("请发表你的开场白", self._get_system_prompt(self.ai2))
            self.logger.debug(f"AI2 opening statement generated: {opening2[:100]}...")
            
            self.history.append(("ai1", opening1))
            self.history.append(("ai2", opening2))
            self.logger.debug("Opening statements added to history")
        except Exception as e:
            self.logger.error(f"Error generating opening statements: {str(e)}", exc_info=True)
            raise

    def next_turn(self) -> bool:
        """进行下一轮辩论"""
        if not self.ai1 or not self.ai2:
            raise ValueError("AI agents not initialized")
        
        if self.current_turn >= self.max_turns:
            self.logger.info("Debate reached maximum turns")
            return False
        
        # 获取上一轮的内容
        last_speaker, last_content = self.history[-1]
        current_speaker = self.ai2 if last_speaker == "ai1" else self.ai1
        
        # 生成回复
        response = current_speaker.generate_response(
            f"请对以下观点进行反驳：{last_content}",
            self._get_system_prompt(current_speaker)
        )
        
        self.history.append(("ai2" if last_speaker == "ai1" else "ai1", response))
        self.current_turn += 1
        
        self.logger.info(f"Completed turn {self.current_turn}")
        return True

    def _get_system_prompt(self, agent: AIAgent) -> str:
        """获取系统提示"""
        agent_code = "ai1" if agent == self.ai1 else "ai2"
        return (
            f"你是辩论机器人{agent.get_nickname()}，今天要讨论的主题是[{self.topics.get('main', '')}]，"
            f"你是{'正方辩友' if agent == self.ai1 else '反方辩友'}，"
            f"你支持的观点是[{self.topics.get(agent_code, '')}]，"
            "你的任务是在这场辩论赛中赢得胜利！"
        )

    def get_history(self) -> List[Tuple[str, str]]:
        """获取辩论历史"""
        return self.history

    def run_debate(self) -> None:
        """运行完整的辩论流程，包括语音播放"""
        # 开始辩论
        self.start_debate()
        
        # 播放开场白
        for speaker, content in self.history:
            if speaker == "ai1":
                self.ai1.speak(content)
            else:
                self.ai2.speak(content)
        
        # 进行辩论
        while self.next_turn():
            # 获取最新一轮的对话
            history = self.get_history()
            last_speaker, last_content = history[-1]
            
            # 播放语音
            if last_speaker == "ai1":
                self.ai1.speak(last_content)
            else:
                self.ai2.speak(last_content)
        
        self.logger.info("Debate completed successfully")
