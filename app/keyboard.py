from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup

language_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='RU'), KeyboardButton(text='EN')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

geneterate_summary = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Сгенерировать сводку')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

questions_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Задать вопрос')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Получить сводку'), KeyboardButton(text='История запросов')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)