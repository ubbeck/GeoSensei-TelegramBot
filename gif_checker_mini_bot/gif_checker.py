import telebot
import os

from dotenv import load_dotenv

load_dotenv()
TOKEN_BOT = os.getenv('TOKEN_BOT')

bot = telebot.TeleBot(TOKEN_BOT)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Send me Telegram GIFS")

@bot.message_handler(content_types= ["animation"])
def take_id(message):
    print(message.animation.file_id)

if __name__ == "__main__":
    print("Init BOT...")
    bot.infinity_polling()