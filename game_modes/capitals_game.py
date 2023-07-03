import telebot
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from main import back
from feedback.feedback import check_hits

import random
import threading
import time

from countries_data import countries

NUM_COUNTRIES = len(countries)
TIME_LIMIT = 5

def play_capitals(message, bot: telebot, user: dict) -> None:
    
    user['hits'] = 0
    bot.send_message(message.chat.id, "How many capitals can you guess?")
    next_question(message, bot, user)

def get_candidates() -> list:
    
    candidates = []
    index = random.sample(range(NUM_COUNTRIES), 2)
    for i in index:
        candidates.append(countries[i]['city'])
    return candidates

def no_played_country(user: dict) -> dict:
    
    country = countries[random.randint(0, NUM_COUNTRIES - 1)]
    while(country['country'] in user['playedInThisRound']):
        country = countries[random.randint(0, NUM_COUNTRIES - 1)]
    return country

def check_answer(message, bot: telebot, user: dict, city: str):
    
    if 'timer' not in user:
        next_question(message, bot, user)
        return
    
    elif message.text == "/back":
        user['timer'].cancel()
        user.pop('timer')
        bot.send_message(message.chat.id, "Exiting capitals contest mode", reply_markup = ReplyKeyboardRemove())
        back(message)
        return

    elif message.text == city:
        user['timer'].cancel()
        bot.send_chat_action(message.chat.id, "typing")
        bot.send_message(message.chat.id, '<b><i>CORRECT</i></b>', parse_mode="html", disable_web_page_preview= True)
        user['hits'] += 1
        next_question(message, bot, user)
    else:
        user['timer'].cancel()
        bot.send_chat_action(message.chat.id, "typing")
        bot.send_message(message.chat.id, f"<b><i>INCORRECT</i></b>, the correct answer is <b><i>{city}</i></b>",parse_mode="html", disable_web_page_preview=True, reply_markup=ReplyKeyboardRemove())
        time.sleep(1)
        bot.send_chat_action(message.chat.id, "typing")
        bot.send_message(message.chat.id, ("&lt------- " + '<b><i>HITS </i></b>' + f"{user['hits']}" + " -------&gt"), parse_mode= "html", disable_web_page_preview= True)
        time.sleep(1)
        #check_hits(message, bot, user)
        bot.send_message(message.chat.id, "Use /capitals to play again")

def next_question(message, bot: telebot, user: dict):
    
    candidates = get_candidates()
    country = no_played_country(user)

    while(country['city'] in candidates):
        no_played_country(user)
    
    user['playedInThisRound'].append(country['country'])

    candidates.append(country['city'])

    random.shuffle(candidates)

    markup = ReplyKeyboardMarkup(
        one_time_keyboard= False,
        input_field_placeholder= "Choose One",
        resize_keyboard= False,
        row_width=1
    )

    markup.add(candidates[0], candidates[1], candidates[2])

    bot.send_chat_action(message.chat.id, "typing")
    user['timer'] = threading.Timer(TIME_LIMIT, handle_timeout, args=[message, bot, user])
    user['timer'].start()
    answer = bot.send_message(message.chat.id, (f"{country['country']}" + " " + f"{country['flag'].encode().decode('unicode_escape')}"),reply_markup=markup)
    bot.register_next_step_handler(answer, check_answer, bot, user, country['city'])

def handle_timeout(message, bot: telebot, user: dict):
    
    user['timer'].cancel()
    user.pop('timer')
    bot.send_message(message.chat.id, "Lose By Time Out", reply_markup = ReplyKeyboardRemove())
    user['hits'] = 0
    user['playedInThisRound'].clear()
    bot.send_message(message.chat.id, "Use /capitals to play again")