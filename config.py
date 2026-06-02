import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "qwen/qwen3.6-plus-preview:free")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
