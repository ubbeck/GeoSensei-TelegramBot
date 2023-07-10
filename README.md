# GeoSensei-TelegramBot
Geography quiz game for telegram, developed on Python using [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
## Game features
The bot has three game modes, capitals, flags and population (Higher-Lower). 
* **Capitals mode**: The bot asks questions about the capitals of different countries. The user must guess the correct capital.
* **Flags mode**: The bot displays the flag of a country and the user must guess which country it corresponds to. 
* **Higher-Lower (population) mode**: The bot displays the name of a country and an estimated population. The user must guess whether the population of another country is higher or lower.
 
In Capitals and Flags modes, the bot displays 3 possible answers on a custom keyboard buttons, in Higher-Lower mode there are only these two buttons. The player has a time limit to answer (5 seconds by default) in all modes.   
## Installation
1. Clone this repository on your local machine.
2. Install the project dependencies by running pip install -r requirements.txt.
3. Get a Telegram bot token by following the instructions on [BotFather](https://core.telegram.org/bots/features#creating-a-new-bot)
4. Create an .env file in the root directory of the project and add the following content:
   
   ```
   TOKEN=your-telegram-bot-token
   ```
5. Run main.py to start the bot.

## Using Telegram's gif gallery
Optionally, to give some feedback to the player, you can use the feedback module, which simply sends a gif from the telegram gallery based on the number of hits.   
The list of gifs is intentionally empty because the gif element identifier varies with each TOKEN.  
You can modify this module to upload and send your own gifs or use the **gif_checker_mini_bot** to capture the telegram identifiers and add them to the list.

## Gif Checker (mini_bot)
According to [Telegram documentation](https://core.telegram.org/bots/api#sending-files), there are 3 ways to send a file:  

1. If the file is already stored somewhere on the Telegram servers, you don't need to reupload it: each file object has a file_id field, simply pass this file_id as a parameter instead of uploading.There are no limits for files sent this way.
2. Provide Telegram with an HTTP URL for the file to be sent. Telegram will download and send the file. 5 MB max size for photos and 20 MB max for other types of content.
3. Post the file using multipart/form-data in the usual way that files are uploaded via the browser. 10 MB max size for photos, 50 MB for other files

We are interested in the first way, using files stored on telegram servers.  
To use this method we need the file_id associated with the file but Telegram also indicates that this identifier is unique for each BOT, i.e. for each TOKEN you generate you will need new identifiers for the same files.   

To get these file_id, you can use the gif_checker_mini_bot.
1. With the **_same TOKEN that you will use in the main bot_**, run the gif_checker.py file to start the bot.
2. From Telegram, the bot will ask you to send it gifs.
3. Select the gifs in the telegram gallery and send them as you normally do.
4. In your execution console, the bot will print out the file_id, which you can add to the list of gifs as a text string.
