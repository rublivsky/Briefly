from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def language_kb():
    buttons = [
        InlineKeyboardButton(text="🇷🇺 Русский", callback_data="language_ru"),
        InlineKeyboardButton(text="🇬🇧 English", callback_data="language_en")
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons])


# questions_keyboard = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton(text='Задать вопрос')]
#     ],
#     resize_keyboard=True,
#     one_time_keyboard=True
# )

def questions_keyboard():
    buttons = [
        InlineKeyboardButton(text="Задать вопрос", callback_data="question")
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons])


main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='История запросов'), KeyboardButton(text='В главное меню')]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)