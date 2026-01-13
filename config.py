# config.py
# 所有敏感信息都从 .env 读取，保护密钥不被上传到 GitHub

import os
from dotenv import load_dotenv

# 自动加载项目根目录下的 .env 文件
load_dotenv()

# 通义千问（DashScope）配置 - 从环境变量读取
API_KEY = os.getenv("DASHSCOPE_API_KEY")
if not API_KEY:
    raise ValueError(
        "DASHSCOPE_API_KEY 未设置！\n"
        "请在项目根目录创建 .env 文件，并添加：\n"
        "DASHSCOPE_API_KEY=sk-你的真实key"
    )

BASE_URL = os.getenv("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "qwen-plus")

# 微信目标好友名称（可以给默认值，也可以从 .env 读）
TARGET_NAME = os.getenv("TARGET_NAME")

# 如果你有其他配置，也可以继续加在这里
# 例如：
# MAX_HISTORY = 10
# SLEEP_INTERVAL = 0.5