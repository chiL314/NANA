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
        from persona.persona_builder import get_system_prompt
        self.system_prompt = get_system_prompt()

    def get_reply(self, history):
        messages = [{"role": "system", "content": self.system_prompt}] + history
        try:
            completion = self.client.chat.completions.create(
                model=config.MODEL_NAME,
                messages=messages,
                temperature=0.8,
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"LMM Error: {e}")
            return "呜呜，信号不好，你刚刚说什么？"