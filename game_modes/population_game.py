import telebot
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from feedback.feedback import check_hits

import random
import copy
import threading
import time

from countries_data import countries

NUM_COUNTRIES = len(countries)
TIME_LIMIT = 5

def play_population(message, bot: telebot, user: dict) -> None:
    
    user['hits'] = 0
    user['playedInThisRound'].clear()
    c1 = countries[random.randrange(NUM_COUNTRIES)]
    c2 = None
    user['playedInThisRound'].append(c1['country'])
    bot.send_chat_action(message.chat.id, "typing")
    bot.send_message(message.chat.id, "Which country is more populus?")
    next_question(message, bot, user, c1, c2)

def set_countries(user: dict, c1: dict, c2: dict) -> None:
    
    if(user['hits'] == 0):
        c2 = copy.deepcopy(countries[random.randrange(NUM_COUNTRIES)])
        while(c2['country'] in user['playedInThisRound']):
            c2 = copy.deepcopy(countries[random.randrange(NUM_COUNTRIES)])
    else:
        c1 = copy.deepcopy(c2)
        user['playedInThisRound'].append(c1['country'])
        while(c2['country'] in user['playedInThisRound']):
            c2 = copy.deepcopy(countries[random.randrange(NUM_COUNTRIES)])
    return c1, c2

def check_answer(message, bot: telebot, user: dict, c1: dict, c2: dict) -> None:
    
    if 'timer' not in user:
        next_question(message, bot, user, c1, c2)
        return
    
    elif message.text == "/back":
        user['timer'].cancel()
        user.pop('timer')
        user['hits'] = 0
        user['playedInThisRound'].clear()
        bot.send_message(message.chat.id, "Exiting Higher-Lower Mode", reply_markup = ReplyKeyboardRemove())
        time.sleep(1)
        bot.send_message(message.chat.id, "Select new Game Mode from Menu")
        return
    
    higher = c1 if c1['population'] > c2['population'] else c2
    attemp = c2['country'] if message.text == "Higher" else c1['country']

    if(higher['country'] == attemp):
        user['timer'].cancel()
        bot.send_chat_action(message.chat.id, "typing")
        bot.send_message(message.chat.id, '<b><i>CORRECT</i></b>', parse_mode="html", disable_web_page_preview= True)
        user['hits'] += 1
        next_question(message, bot, user, c1, c2)
    else:
        user['timer'].cancel()
        bot.send_chat_action(message.chat.id, "typing")
        bot.send_message(message.chat.id, f"<b><i>INCORRECT</i></b>, {c2['country']} {c2['flag'].encode().decode('unicode_escape')} has {c2['population']: ,}",parse_mode="html", disable_web_page_preview=True, reply_markup=ReplyKeyboardRemove())
        bot.send_chat_action(message.chat.id, "typing")
        bot.send_message(message.chat.id, ("&lt------- " + '<b><i>HITS </i></b>' + f"{user['hits']}" + " -------&gt"), parse_mode= "html", disable_web_page_preview= True)
        # check_hits(message, bot, user)
        bot.send_message(message.chat.id, "Use /population to play again")

def next_question(message, bot: telebot, user: dict, c1:dict, c2: dict) -> None:
    
    c1, c2 = set_countries(user, c1, c2)

    markup = ReplyKeyboardMarkup(
        one_time_keyboard = False,
        input_field_placeholder= "Choose One",
        resize_keyboard= False,
        row_width= 1
    )

    markup.add("Higher", "Lower")

    bot.send_chat_action(message.chat.id, "typing")
    user['timer'] = threading.Timer(TIME_LIMIT, handle_timeout, args=[message, bot, user])
    user['timer'].start()
    bot.send_message(message.chat.id, f"{c1['country']} {c1['flag'].encode().decode('unicode_escape')} {c1['population']: ,}")
    answer = bot.send_message(message.chat.id, f"{c2['country']} {c2['flag'].encode().decode('unicode_escape')}", reply_markup=markup)
    bot.register_next_step_handler(answer, check_answer, bot, user, c1, c2)

def handle_timeout(message, bot: telebot, user: dict) -> None:
    
    user['timer'].cancel()
    user.pop('timer')
    bot.send_message(message.chat.id, "Lose By Time Out", reply_markup = ReplyKeyboardRemove())
    user['hits'] = 0
    user['playedInThisRound'].clear()
    bot.send_message(message.chat.id, "Use /population to play again")