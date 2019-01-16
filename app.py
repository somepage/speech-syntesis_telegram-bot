from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ChatAction
import logging
import speechkit
from io import BytesIO


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Enter a text for transform text-to-speech, send / for "
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


def change_voice(bot, update, chat_data):
    if chat_data.get(update.message.chat_id, 0):
        gender_id = chat_data[1]
    else:
        gender_id = gender_default

    voices_buttons = [[InlineKeyboardButton(text=v, callback_data=v) for v in voices[gender_id]]]
    voices_markup = InlineKeyboardMarkup(voices_buttons)
    bot.send_message(chat_id=update.message.chat_id, text="Choose a voice", reply_markup=voices_markup)

    return VOICE


def change_emotion(bot, update):
    emotions_buttons = [[InlineKeyboardButton(text=em, callback_data=em) for em in emotions]]
    emotions_markup = InlineKeyboardMarkup(emotions_buttons)
    bot.send_message(chat_id=update.message.chat_id, text="Choose a emotion", reply_markup=emotions_markup)

    return EMOTION


def callback_language(bot, update, chat_data):
    query = update.callback_query

    if chat_data.get(query.message.chat_id, 0):
        chat_data[query.message.chat_id][LANG] = query.data
    else:
        chat_data[query.message.chat_id] = [
            query.data,
            gender_default,
            voice_default,
            emotion_default
        ]
    bot.answer_callback_query(update.callback_query.id, text="Language successfully changed")


def callback_gender(bot, update, chat_data):
    query = update.callback_query

    if chat_data.get(query.message.chat_id, 0):
        chat_data[query.message.chat_id][GENDER] = query.data
    else:
        chat_data[query.message.chat_id] = [
            language_default,
            query.data,
            voice_default,
            emotion_default
        ]
    bot.answer_callback_query(update.callback_query.id, text="Gender successfully changed")


def callback_voice(bot, update, chat_data):
    query = update.callback_query

    if chat_data.get(query.message.chat_id, 0):
        chat_data[query.message.chat_id][VOICE] = query.data
    else:
        chat_data[query.message.chat_id] = [
            language_default,
            gender_default,
            query.data,
            emotion_default
        ]
    bot.answer_callback_query(update.callback_query.id, text="Voice successfully changed")


def callback_emotion(bot, update, chat_data):
    query = update.callback_query

    if chat_data.get(query.message.chat_id, 0):
        chat_data[query.message.chat_id][EMOTION] = query.data
    else:
        chat_data[query.message.chat_id] = [
            language_default,
            gender_default,
            voice_default,
            query.data
        ]
    bot.answer_callback_query(update.callback_query.id, text="Emotion successfully changed")


def send_speech(bot, update, chat_data):
    bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.RECORD_AUDIO)
    text = update.message.text

    if chat_data.get(update.message.chat_id, 0):
        language = languages[chat_data[update.message.chat_id][LANG]]
        voice = chat_data[update.message.chat_id][VOICE].lower()
        emotion = chat_data[update.message.chat_id][EMOTION].lower()
    else:
        language = languages[language_default]
        voice = voice_default.lower()
        emotion = emotion_default.lower()

    global iam_token
    global folder_id
    speech_request = speechkit.synthesize(text, iam_token, folder_id, lang=language, voice=voice, emotion=emotion)

    if speech_request.status_code == 400:
        iam_token = speechkit.get_iam_token(oauth_token)
        speech_request = speechkit.synthesize(text, iam_token, folder_id, lang=language, voice=voice, emotion=emotion)

    bot.sendVoice(update.message.chat_id, BytesIO(speech_request.content))


if __name__ == '__main__':
    updater = Updater(token='TOKEN')
    folder_id = 'ID'
    oauth_token = 'OAUTH'
    iam_token = speechkit.get_iam_token(oauth_token)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

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
            CommandHandler('change_voice', change_voice, pass_chat_data=True),
            CommandHandler('change_emotion', change_emotion)
        ],
        states={
            LANG: [CallbackQueryHandler(callback_language, pass_chat_data=True)],
            GENDER: [CallbackQueryHandler(callback_gender, pass_chat_data=True)],
            VOICE: [CallbackQueryHandler(callback_voice, pass_chat_data=True)],
            EMOTION: [CallbackQueryHandler(callback_emotion, pass_chat_data=True)],
        },
        fallbacks=[]
    )
    msg_handler = MessageHandler(Filters.text, send_speech, pass_chat_data=True)

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(msg_handler)

    updater.start_polling()
    updater.idle()
