import os
import dashscope
from http import HTTPStatus
from random import random
from typing import Optional, List, Dict
from src.core.ai_agent import AIAgent
from src.utils.logger import logger_manager


class QwenAgent(AIAgent):
    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        self.config = config
        self.model = config.get("model", "qwen-plus-0112")
        self.api_key = os.getenv("QWEN_API_KEY", "")
        self.logger = logger_manager.get_logger(f"ai_agent.{name}")
        
        # 获取辩论配置
        debate_config = config.get("debate", {})
        topics_config = debate_config.get("topics", {})
        
        # 设置系统角色
        self.system_role = (
            f"你是辩论机器人{name}，今天你要讨论的主题是[{topics_config.get('main', '')}]，"
            f"你支持的观点是[{topics_config.get('ai1' if name == 'ai1' else 'ai2', '')}]，"
            f"你反方的观点是[{topics_config.get('ai2' if name == 'ai1' else 'ai1', '')}]，"
            "你的任务是在这场辩论赛中赢得胜利！"
        )
        self.media_path = config.get("tts", {}).get("media_path", "tmp")
        self.vtt_path = config.get("tts", {}).get("vtt_path", "tmp")

    def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """生成回答"""
        try:
            # 构建消息列表，包含系统提示、历史对话和当前问题
            messages = []
            
            # 添加系统提示
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            else:
                messages.append({"role": "system", "content": self.system_role})
            
            # 添加历史对话
            history = self.get_history()
            messages.extend(history)
            
            # 添加当前问题
            messages.append({"role": "user", "content": prompt})
            
            # 调用模型生成回答
            response = self._create_chat_completion(messages)
            self.logger.info(f"Response: {response}")
            
            # 将问题和回答添加到历史记录
            self.add_to_history("user", prompt)
            self.add_to_history("assistant", response)
            
            return response
        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            raise

    def _create_chat_completion(self, messages: List[Dict[str, str]]) -> str:
        """调用通义千问API生成回答"""
        dashscope.api_key = self.api_key
        seed = 1 + int(1000 * random())
        response = dashscope.Generation.call(
            model=self.model,
            messages=messages,
            seed=seed,
            top_p=0.8,
            result_format='message',
            enable_search=True,
            max_tokens=1500,
            temperature=1.0,
            repetition_penalty=1.0
        )
        if response.status_code == HTTPStatus.OK:
            content = response.get("output", {}).get("choices", [{}])[0].get("message", "").get("content", "")
            return content
        else:
            self.logger.error('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code, response.code, response.message
            ))
            raise Exception(f"API request failed: {response.message}")
