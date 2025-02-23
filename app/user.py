import os
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from database.requests import set_user, set_language, check_user, check_language
from app.keyboard import language_keyboard, questions_keyboard, main_menu_keyboard
from app.logic import time_now, transcribe_audio
# from main import bot

router = Router()

class user(StatesGroup):
    choose_lang = State()
    main_menu = State()
    get_summary = State()
    get_history = State()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    if await check_user(message.from_user.id):
        await message.answer("Можешь отправить мне аудио файл / голосовое сообщение / ссылку на ютуб и я сгенерирую сводку по нему.")
    else:
        await set_user(message.from_user.id, message.from_user.username, time_now())
        await message.answer("Привет! Я могу делать сводку по информации которую ты мне предоставишь.\nДля начала выбери язык:", 
                             reply_markup=language_keyboard)
        await state.set_state(user.choose_lang)
        
@router.message(user.choose_lang)
async def choose_lang(message: Message, state: FSMContext):
    if message.text == "EN" or message.text == "RU" or message.text == "UA":
        await set_language(message.from_user.id, message.text.strip())
        await state.clear()
        await message.answer(f"Теперь я буду делать сводку на этом языке: {message.text.strip()}")
    else:
        await message.answer("Выбери язык: EN / RU / UA", reply_markup=language_keyboard)
    
    await message.answer("Можешь отправить мне аудио файл / голосовое сообщение / ссылку на ютуб и я сгенерирую сводку по нему.")
    
    
@router.message(F.text.in_(["Главное меню", "/main_menu"]))
async def main_menu(message: Message, state: FSMContext):
    await message.answer("Выбери действие:", reply_markup=main_menu_keyboard)
    

@router.message(F.voice)
async def handle_voice_message(message: Message):
    # from main import bot
    bot = message.bot
    """Обрабатывает голосовое сообщение, скачивает и делает транскрипцию"""
    voice = message.voice
    file_info = await bot.get_file(voice.file_id)
    file_path = file_info.file_path
    local_file = f"downloads/{voice.file_id}.ogg"
    # Создаём папку, если её нет
    os.makedirs("downloads", exist_ok=True)
    # Скачиваем файл
    await bot.download_file(file_path, local_file)
    # Делаем транскрипцию
    transcript = await transcribe_audio(local_file, await check_language(message.from_user.id))
    # Отправляем текст пользователю
    await message.answer(f"Вот что я понял из твоего голосового:\n\n{transcript}")
    # Удаляем файл после обработки
    os.remove(local_file)