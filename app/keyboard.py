from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup

language_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='RU'), KeyboardButton(text='EN'), KeyboardButton(text='UA')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

questions_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            {"text": "Задать вопрос?", "callback_data": "question"}
        ]
    ]
)

main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Получить сводку'), KeyboardButton(text='История запросов')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)