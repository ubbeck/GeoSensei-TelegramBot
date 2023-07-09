import telebot
import random
from feedback.gifs_id import *

def check_hits(message, bot: telebot, hits: int) -> None:

    if(hits == 0):
        gf: str = no_hits[random.randrange(0, len(no_hits))]['file_id']
    elif(hits < 5):
        gf: str = less_5[random.randrange(0, len(less_5))]['file_id']
    elif(hits < 15):
        gf: str = over_5[random.randrange(0, len(over_5))]['file_id']    
    elif(hits < 25):
        gf: str = over_15[random.randrange(0, len(over_15))]['file_id']
    elif(hits < 50):
        gf: str = over_25[random.randrange(0, len(over_25))]['file_id']
    else:
        gf: str = over_50[0]['file_id']

    bot.send_animation(message.chat.id, gf)