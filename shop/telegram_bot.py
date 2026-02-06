import os
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = Bot(token=TOKEN)

async def send_order_notification(message):
    await bot.send_message(chat_id=CHAT_ID, text=message)