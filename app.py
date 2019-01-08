from telegram.ext import Updater, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import logging


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Enter a text for transform text-to-speech")


def change_language(bot, update):
    languages_markup = ReplyKeyboardMarkup(keyboard=[list(languages.keys())], resize_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text="Choose a language", reply_markup=languages_markup)
    bot.update()


def change_gender(bot, update):
    remove_buttons = ReplyKeyboardRemove(remove_keyboard=True)
    genders = ['Male', 'Female']
    gender_markup = ReplyKeyboardMarkup(keyboard=[genders], resize_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text="Choose a gender", reply_markup=gender_markup)


def change_voice(bot, update):
    voices = {'Male': ['Zahar', 'Ermil'], 'Female': ['Alyss', 'Jane', 'Oksana', 'Omazh']}
    voice_markup = ReplyKeyboardMarkup(keyboard=[list(voices[gender])], resize_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text="Choose a voice", reply_markup=voice_markup)


def change_emotion(bot, update):
    emotions = ['Good', 'Evil', 'Neutral']
    emotions_markup = ReplyKeyboardMarkup(keyboard=[emotions], resize_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text="Choose a voice", reply_markup=emotions_markup)


updater = Updater(token='TOKEN')
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

start_handler = CommandHandler('start', start)
change_language_handler = CommandHandler('change_language', change_language)
change_gender_handler = CommandHandler('change_gender', change_gender)
change_voice_handler = CommandHandler('change_voice', change_voice)
language = 'Russian'
gender = 'Male'
voice = 'Ermil'
emotion = 'Neutral'
languages = {'Russian': 'ru-RU', 'English': 'en-US', 'Turkish': 'tr-TR'}

dispatcher.add_handler(start_handler)
dispatcher.add_handler(change_language_handler)
dispatcher.add_handler(change_gender_handler)
dispatcher.add_handler(change_voice_handler)
updater.start_polling()
