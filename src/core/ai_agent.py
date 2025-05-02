from abc import ABC, abstractmethod
from typing import Optional, List, Dict
from src.utils.logger import logger_manager
from src.core.conversation import ConversationHistory

class AIAgent(ABC):
    def __init__(self, name: str, config: dict):
        self.name = name
        self.config = config
        self.logger = logger_manager.get_logger(f"ai_agent.{name}")
        self._active = True
        self.conversation = ConversationHistory()
    
    @abstractmethod
    def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """生成回答"""
        pass
    
    def speak(self, text: str) -> None:
        """语音输出"""
        if not self._active:
            self.logger.warning(f"{self.name} is not active, skipping speech")
            return
        try:
            self._speak_impl(text)
        except Exception as e:
            self.logger.error(f"Error in speech generation: {e}")
            raise
    
    @abstractmethod
    def _speak_impl(self, text: str) -> None:
        """具体的语音实现"""
        pass
    
    def activate(self) -> None:
        """激活代理"""
        self._active = True
        self.logger.info(f"{self.name} activated")
    
    def deactivate(self) -> None:
        """停用代理"""
        self._active = False
        self.logger.info(f"{self.name} deactivated")
    
    def is_active(self) -> bool:
        """检查代理是否激活"""
        return self._active
    
    def add_to_history(self, role: str, content: str) -> None:
        """添加消息到历史记录"""
        self.conversation.add_message(role, content)
    
    def get_history(self) -> List[Dict[str, str]]:
        """获取历史记录"""
        return self.conversation.get_history()
    
    def clear_history(self) -> None:
        """清空历史记录"""
        self.conversation.clear() 