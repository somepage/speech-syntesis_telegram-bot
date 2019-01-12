from telegram.ext import Updater, CommandHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import logging


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Enter a text for transform text-to-speech, send /help for "
                                                          "more")


def change_language(bot, update):
    languages_buttons = [[InlineKeyboardButton(text=lang, callback_data=lang) for lang in languages.keys()]]
    languages_markup = InlineKeyboardMarkup(languages_buttons)
    bot.send_message(chat_id=update.message.chat_id, text="Choose a language", reply_markup=languages_markup)


def change_gender(bot, update):
    genders_buttons = [[InlineKeyboardButton(text=gen, callback_data=gen) for gen in genders]]
    genders_markup = InlineKeyboardMarkup(genders_buttons)
    bot.send_message(chat_id=update.message.chat_id, text="Choose a gender", reply_markup=genders_markup)


def change_voice(bot, update):
    gender_id = gender.get(update.message.chat_id, default=voice_default)
    voices_buttons = [[InlineKeyboardButton(text=v, callback_data=v) for v in voices[gender_id]]]
    voices_markup = InlineKeyboardMarkup(voices_buttons)
    bot.send_message(chat_id=update.message.chat_id, text="Choose a voice", reply_markup=voices_markup)


def change_emotion(bot, update):
    emotions_buttons = [[InlineKeyboardButton(text=em, callback_data=em) for em in emotions]]
    emotions_markup = InlineKeyboardMarkup(emotions_buttons)
    bot.send_message(chat_id=update.message.chat_id, text="Choose a voice", reply_markup=emotions_markup)


updater = Updater(token='TOKEN')
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

start_handler = CommandHandler('start', start)
change_language_handler = CommandHandler('change_language', change_language)
change_gender_handler = CommandHandler('change_gender', change_gender)
change_voice_handler = CommandHandler('change_voice', change_voice)

language = {}
gender = {}
voice = {}
emotion = {}

language_default = 'Russian'
gender_default = 'Female'
voice_default = 'Oksana'
emotion_default = 'Neutral'  # by default

languages = {'Russian': 'ru-RU', 'English': 'en-US', 'Turkish': 'tr-TR'}
genders = ['Male', 'Female']
voices = {'Male': ['Zahar', 'Ermil'], 'Female': ['Alyss', 'Jane', 'Oksana', 'Omazh']}
emotions = ['Good', 'Evil', 'Neutral']

dispatcher.add_handler(start_handler)
dispatcher.add_handler(change_language_handler)
dispatcher.add_handler(change_gender_handler)
dispatcher.add_handler(change_voice_handler)
updater.start_polling()