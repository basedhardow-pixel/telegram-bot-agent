import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from handlers import start, handle_message
from config import TELEGRAM_TOKEN
import logging

logging.basicConfig(level=logging.INFO)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message), group=1)
    
    print("✅ Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()