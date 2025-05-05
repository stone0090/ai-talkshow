from typing import List, Dict, Optional
from src.utils.logger import logger_manager

class ConversationHistory:
    def __init__(self, max_history: int = 3):
        self.max_history = max_history
        self.history: List[Dict[str, str]] = []
        self.logger = logger_manager.get_logger("conversation_history")
        self.logger.debug(f"Initialized conversation history with max_history={max_history}")
    
    def add_message(self, role: str, content: str) -> None:
        """添加一条消息到历史记录"""
        self.history.append({"role": role, "content": content})
        if len(self.history) > self.max_history * 2:  # 每轮对话包含一问一答
            self.history = self.history[-self.max_history * 2:]
            self.logger.debug(f"History truncated to {self.max_history * 2} messages")
        self.logger.debug(f"Added message: role={role}, content={content[:100]}...")
    
    def get_history(self) -> List[Dict[str, str]]:
        """获取历史记录"""
        history = self.history.copy()
        self.logger.debug(f"Retrieved history with {len(history)} messages")
        return history
    
    def clear(self) -> None:
        """清空历史记录"""
        self.history.clear()
        self.logger.debug("History cleared")
    
    def get_last_n_rounds(self, n: int) -> List[Dict[str, str]]:
        """获取最近n轮对话"""
        if n <= 0:
            self.logger.debug("Requested 0 or negative rounds, returning empty list")
            return []
        rounds = self.history[-min(n * 2, len(self.history)):]
        self.logger.debug(f"Retrieved last {n} rounds ({len(rounds)} messages)")
        return rounds 