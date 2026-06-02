from telegram import Update
from telegram.ext import ContextTypes
from agent.core import Agent
from agent.memory import Memory
import os

REDIS_URL = os.getenv("REDIS_URL")
memory = Memory(REDIS_URL)
agent = Agent(memory)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message = update.message.text
    
    if not message:
        await update.message.reply_text("Напишите текстовое сообщение.")
        return
    
    try:
        response = await agent.process(user_id, message)
        if not response or response.strip() == "":
            response = "Не удалось получить ответ. Попробуйте ещё раз."
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {str(e)}")