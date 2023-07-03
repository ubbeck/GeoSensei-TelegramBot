import telebot
import random
from feedback.gifs_id import gifs

def check_hits(message, bot: telebot, user: dict) -> None:

    gf = gif_id()
    bot.send_animation(message.chat.id, gf)

def gif_id() -> str:

    num = random.randint(0,6)
    gif: str = gifs[num]['file_id']
    return gif
    