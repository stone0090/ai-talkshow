import os
import json
import dashscope
from http import HTTPStatus
from random import random
from typing import Optional, List, Dict
from src.core.ai_agent import AIAgent
from src.utils.logger import logger_manager


class QwenAgent(AIAgent):
    def __init__(self, agent_code: str, config: dict):
        self.logger = logger_manager.get_logger(f"qwen_agent.{agent_code}")
        super().__init__(agent_code, config)
        self.model = config.get("model", "qwen-plus-0112")
        self.api_key = os.getenv("QWEN_API_KEY", "")
        # 设置系统角色
        self.system_role = (
            f"你是来自阿里云的大规模语言模型{self.model}，你叫通义千问，昵称是{self.nickname}，"
            f"你能够回答问题、创作文字，还能表达观点、撰写代码等，你能帮助用户解决各种问题。"
        )
        self.audio_path = config.get("tts", {}).get("audio_path", "tmp")
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

            # 将问题和回答添加到历史记录
            self.add_to_history("user", prompt)
            self.add_to_history("assistant", response)
            
            return response
        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            raise

    def _create_chat_completion(self, messages: List[Dict[str, str]]) -> str:
        """调用通义千问API生成回答"""
        self.logger.debug(f"_create_chat_completion request: {json.dumps(messages, ensure_ascii=False)}")
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
            self.logger.debug(f"_create_chat_completion response: {content}")
            return content
        else:
            self.logger.error('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code, response.code, response.message
            ))
            raise Exception(f"API request failed: {response.message}")
