import os
import telebot

from dotenv import load_dotenv
from telebot.apihelper import ApiTelegramException

from game_modes.capitals_game import play_capitals
from game_modes.population_game import play_population

load_dotenv()
TOKEN_BOT = os.getenv('TOKEN_BOT')

try:
    bot = telebot.TeleBot(TOKEN_BOT)
except ApiTelegramException as e:
    print(f"Connection failure: {e}")

users: dict = {}

def set_commands() -> None:
    bot.set_my_commands([
        telebot.types.BotCommand("/start", "Initialize BOT"),
        telebot.types.BotCommand("/capitals", "Capital contest mode"),
        telebot.types.BotCommand("/population", "Higher-Lower mode"),
        telebot.types.BotCommand("/flags", "Flags contest mode"),
        telebot.types.BotCommand("/back", "Exit game mode"),
        telebot.types.BotCommand("/help", "What can this bot do?")
    ])

@bot.message_handler(commands=["start"])
def start(message) -> None:
    users[message.chat.id] = {'hits': 0, 'playedInThisRound' : []}
    bot.send_message(message.chat.id, "Welcome young grasshoper, choose a game mode \n"
        "\n"
        "/capitals   : Classic game mode\n"
        "/population : Higher-Lower mode\n"
        "/flags      : Flags contest mode")

@bot.message_handler(commands=["help"])
def bot_help(message) -> None:
    bot.send_message(message.chat.id, "Train with GeoSensei your geographic skills in 3 game modes.\n"
        "\n"
        "/capitals   : Classic game mode\n"
        "/population : Higher-Lower mode\n"
        "/flags      : Flags contest mode\n"
        "\n"
        "Use /back to exit the current game mode\n"
        "\n"
        "How many questions in a row can you answer? You have 5 seconds per question, so go for it!")

@bot.message_handler(commands=["capitals"])
def capitals(message) -> None:
    play_capitals(message, bot, users[message.chat.id])

@bot.message_handler(commands=["population"])
def population(message) -> None:
    play_population(message, bot, users[message.chat.id])

@bot.message_handler(commands=["flags"])
def flags(message) -> None:
    pass

@bot.message_handler(commands=["back"])
def back(message) -> None:
    
    bot.send_message(message.chat.id, "No Game Mode Activated\n"
        "Select one\n"
        "\n"
        "/capitals   : Classic game mode\n"
        "/population : Higher-Lower mode\n"
        "/flags      : Flags contest mode\n"
        "\n")

# ------------- MAIN ------------- #
if __name__ == '__main__':
    print("Init BOT...")
    set_commands()
    try:
        bot.infinity_polling()
    except ApiTelegramException as e:
        print(f"Connection failure: {e}")