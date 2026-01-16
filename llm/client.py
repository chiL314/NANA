# llm/client.py
from openai import OpenAI
import config
import os


class LLMClient:
    def __init__(self):
        # 彻底禁用代理
        for env_var in ["http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "all_proxy", "ALL_PROXY"]:
            if env_var in os.environ:
                del os.environ[env_var]

        self.client = OpenAI(
            api_key=config.API_KEY,
            base_url=config.BASE_URL,
            timeout=10.0
        )

    def get_reply(self, history, memory_summary=""):
        """
        获取 AI 回复
        
        参数:
            history: 对话历史
            memory_summary: 记忆摘要（用于增强 system prompt）
        """
        from persona.persona_builder import get_system_prompt
        
        # 动态构建包含记忆的 system prompt
        system_prompt = get_system_prompt(memory_summary)
        messages = [{"role": "system", "content": system_prompt}] + history
        
        try:
            completion = self.client.chat.completions.create(
                model=config.MODEL_NAME,
                messages=messages,
                temperature=0.8,
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"LLM Error: {e}")
            return "呜呜，信号不好，你刚刚说什么？"
