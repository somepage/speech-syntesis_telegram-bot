from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import logging


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Enter a text for transform text-to-speech, send /help for "
                                                          "more")


def change_language(bot, update):
    languages_buttons = [[InlineKeyboardButton(text=lang, callback_data=lang) for lang in languages.keys()]]
    languages_markup = InlineKeyboardMarkup(languages_buttons)
    bot.send_message(chat_id=update.message.chat_id, text="Choose a language", reply_markup=languages_markup)

    return LANG


def change_gender(bot, update):
    genders_buttons = [[InlineKeyboardButton(text=gen, callback_data=gen) for gen in genders]]
    genders_markup = InlineKeyboardMarkup(genders_buttons)
    bot.send_message(chat_id=update.message.chat_id, text="Choose a gender", reply_markup=genders_markup)

    return GENDER


def change_voice(bot, update):
    gender_id = gender.get(update.message.chat_id, default=voice_default)
    voices_buttons = [[InlineKeyboardButton(text=v, callback_data=v) for v in voices[gender_id]]]
    voices_markup = InlineKeyboardMarkup(voices_buttons)
    bot.send_message(chat_id=update.message.chat_id, text="Choose a voice", reply_markup=voices_markup)

    return VOICE


def change_emotion(bot, update):
    emotions_buttons = [[InlineKeyboardButton(text=em, callback_data=em) for em in emotions]]
    emotions_markup = InlineKeyboardMarkup(emotions_buttons)
    bot.send_message(chat_id=update.message.chat_id, text="Choose a voice", reply_markup=emotions_markup)

    return EMOTION


def callback_language(bot, update, user_data):
    user_data['language'] = languages[update.callback_query.data]
    bot.answer_callback_query(update.callback_query.id, text="Language successfully changed")


def callback_gender(bot, update, user_data):
    user_data['gender'] = update.callback_query.data
    bot.answer_callback_query(update.callback_query.id, text="Gender successfully changed")


def callback_voice(bot, update, user_data):
    user_data['voice'] = update.callback_query.data
    bot.answer_callback_query(update.callback_query.id, text="Voice successfully changed")


def callback_emotion(bot, update, user_data):
    user_data['emotion'] = update.callback_query.data
    bot.answer_callback_query(update.callback_query.id, text="Emotion successfully changed")


def send_speech(bot, update, user_data):
    pass


if __name__ == '__main__':
    updater = Updater(token='TOKEN')
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

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

    LANG, GENDER, VOICE, EMOTION = range(4)

    start_handler = CommandHandler('start', start)
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('change_language', change_language),
            CommandHandler('change_gender', change_gender),
            CommandHandler('change_voice', change_voice),
            CommandHandler('change_emotion', change_emotion)
        ],
        states={
            LANG: [CallbackQueryHandler(callback_language, pass_user_data=True)],
            GENDER: [CallbackQueryHandler(callback_gender, pass_user_data=True)],
            VOICE: [CallbackQueryHandler(callback_voice, pass_user_data=True)],
            EMOTION: [CallbackQueryHandler(callback_emotion, pass_user_data=True)],
        },
        fallbacks=[]
    )
    msg_handler = MessageHandler(Filters.text, send_speech)

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(msg_handler)

    updater.start_polling()
    updater.idle()
