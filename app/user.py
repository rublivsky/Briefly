import os
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from database.requests import set_user, set_language, check_user, check_language, set_uploaded_text
from app.keyboard import language_keyboard, questions_keyboard, main_menu_keyboard, geneterate_summary
from app.logic import time_now, transcribe_audio, ask_openai

router = Router()

user_data = {}

SUMAMARY_PROMPT = "Ты — помощник, который кратко резюмирует текст."
QUESTION_FROM_CONTEXT = "Исходя из текста дай ответ на вопрос"

class user(StatesGroup):
    choose_lang = State()
    main_menu = State()
    get_summary = State()
    ask_question = State()
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
    if message.text == "EN" or message.text == "RU":
        await set_language(message.from_user.id, message.text.strip())
        await state.clear()
        await message.answer(f"Теперь я буду делать сводку на этом языке: {message.text.strip()}")
    else:
        await message.answer("Выбери язык: EN / RU", reply_markup=language_keyboard)
    
    await message.answer("Можешь отправить мне аудио файл / голосовое сообщение / ссылку на ютуб и я сгенерирую сводку по нему.")
    
    
@router.message(F.text.in_(["Главное меню", "/main_menu"]))
async def main_menu(message: Message, state: FSMContext):
    await message.answer("Выбери действие:", reply_markup=main_menu_keyboard)
    

@router.message(F.voice)
async def handle_voice_message(message: Message ,state: FSMContext):
    telegram_id = message.from_user.id
    if telegram_id not in user_data:
        user_data[telegram_id] = {}
        
    bot = message.bot
    """Обрабатывает голосовое сообщение, скачивает и делает транскрипцию"""
    voice = message.voice
    file_info = await bot.get_file(voice.file_id)
    file_path = file_info.file_path
    local_file = f"downloads/{voice.file_id}.ogg"
    os.makedirs("downloads", exist_ok=True)
    
    await bot.download_file(file_path, local_file)
    transcript = await transcribe_audio(local_file, await check_language(message.from_user.id))
    user_data[telegram_id]["uploaded_text"] = transcript
    
    await message.answer(f"Вот что я понял из твоего голосового:\n\n{transcript}", reply_markup=geneterate_summary)
    
    os.remove(local_file)
    await state.set_state(user.get_summary)


# await state.clear() 
@router.message(F.text == "Сгенерировать сводку", user.get_summary)
async def summary(message: Message, state: FSMContext):
    await message.answer("Генерирую сводку, подождите немного...")
    summary_text = await ask_openai(user_data[message.from_user.id]["uploaded_text"], SUMAMARY_PROMPT)
    user_data[message.from_user.id]["response"] = summary_text
    await message.answer(f"Сводка готова:\n{summary_text}", reply_markup=questions_keyboard)
    await state.clear()
    

@router.message(F.text == "Задать вопрос")
async def ask_question(message: Message, state: FSMContext):
    await message.answer("Задайте вопрос:")
    await state.set_state(user.ask_question)
    

@router.message(user.ask_question)
async def get_question(message: Message, state: FSMContext):
    user_data[message.from_user.id]["question"] = message.text
    
    full_context = (f"{QUESTION_FROM_CONTEXT}\n {user_data[message.from_user.id]["question"]}Исходя из текста:\n{user_data[message.from_user.id]['uploaded_text']}")
    await message.answer("Подождите немного, ищу ответ на ваш вопрос...")
    question_response = await ask_openai(user_data[message.from_user.id]["question"], full_context)
    user_data[message.from_user.id]["question_response"] = question_response
    await message.answer(f"Ответ на ваш вопрос:\n{question_response}")
    await state.clear()
    
    await set_uploaded_text(time_now(), 
                            message.from_user.id, 
                            user_data[message.from_user.id]["uploaded_text"], 
                            user_data[message.from_user.id]["response"],
                            user_data[message.from_user.id]["question"],
                            user_data[message.from_user.id]["question_response"]
                            )
    
    # del user_data[message.from_user.id]
    