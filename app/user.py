from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from database.requests import set_user, set_language, check_user

router = Router()

class user_choose(StatesGroup):
    choose_lang = State()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    if check_user(message.from_user.id):
        await message.answer("Можешь отправить мне аудио файл / голосовое сообщение / ссылку на ютуб и я сгенерирую сводку по нему.")
    else:
        set_user(message.from_user.id, message.from_user.username)
        await message.answer("Привет! Я могу делать сводку по информации которую ты мне предоставишь.\nДля начала выбери язык EN / RU / UA")
        await state.set_state(user_choose.choose_lang)
        
@router.message(user_choose.choose_lang)
async def choose_lang(message: Message, state: FSMContext):
    if message.text == "EN" or message.text == "RU" or message.text == "UA":
        set_language(message.from_user.id, message.text.strip())
        await state.clear()
        await message.answer(f"Теперь я буду делать сводку на этом языке: {message.text.strip()}")
    else:
        await message.answer("Выбери язык EN / RU / UA")
    
    await message.answer("Можешь отправить мне аудио файл / голосовое сообщение / ссылку на ютуб и я сгенерирую сводку по нему.")
 