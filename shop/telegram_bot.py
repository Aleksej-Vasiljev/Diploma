import os
from dotenv import load_dotenv
import telebot

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = telebot.TeleBot(TOKEN)

def send_order_notification(message):
    bot.send_message(chat_id=CHAT_ID, text=message)