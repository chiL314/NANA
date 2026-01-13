# config.py （这个可以 commit）
import os
from dotenv import load_dotenv

load_dotenv()  # 自动加载 .env 文件（如果存在）

# 必填项，如果没找到会报错（方便调试）
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
if not DASHSCOPE_API_KEY:
    raise ValueError("DASHSCOPE_API_KEY 未设置！请在 .env 文件中配置")

DASHSCOPE_BASE_URL = os.getenv("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")

TARGET_NAME = os.getenv("TARGET_NAME", "默认好友")  # 可以给默认值

# 其他非敏感配置可以直接写在这里
MAX_HISTORY = 10