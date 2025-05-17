import telebot
from telebot import types
from googletrans import Translator

bot = telebot.TeleBot("7421035921:AAHE10_aStkoSuThn0Ewt7jc9Hk5aRVtD0k")  # Замените на ваш токен
translator = Translator()
user_states = {}

# Список популярных языков
LANGUAGES = {
    "🇬🇧 English": "en",
    "🇰🇷 Korean": "ko",
    "🇷🇺 Russian": "ru",
    "🇩🇪 German": "de",
    "🇫🇷 French": "fr",
    "🇪🇸 Spanish": "es",
    "🇨🇳 Chinese": "zh-cn",
    "🇯🇵 Japanese": "ja",
    "🇮🇹 Italian": "it",
    "🇹🇷 Turkish": "tr"
}

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "Привет! Напиши /translate чтобы перевести текст.")

@bot.message_handler(commands=['translate'])
def ask_language(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

    for lang in LANGUAGES:
        markup.add(lang)

    user_states[chat_id] = {'step': 'awaiting_language'}
    bot.send_message(chat_id, "Выберите язык перевода:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    chat_id = message.chat.id
    text = message.text.strip()

    if chat_id in user_states:
        state = user_states[chat_id]

        # Шаг выбора языка
        if state['step'] == 'awaiting_language':
            if text in LANGUAGES:
                state['lang'] = LANGUAGES[text]
                state['step'] = 'awaiting_text'
                bot.send_message(chat_id, "Отправьте текст, который нужно перевести:", reply_markup=types.ReplyKeyboardRemove())
            else:
                bot.send_message(chat_id, "Пожалуйста, выбери язык с кнопок.")

        # Шаг ввода текста
        elif state['step'] == 'awaiting_text':
            try:
                lang = state['lang']
                translation = translator.translate(text, dest=lang)
                bot.send_message(chat_id, f"Перевод: {translation.text}")
            except Exception as e:
                bot.send_message(chat_id, f"Ошибка: {str(e)}")
            user_states.pop(chat_id)
    else:
        bot.send_message(chat_id, "Напиши /translate чтобы начать.")

# Запуск
bot.polling()
