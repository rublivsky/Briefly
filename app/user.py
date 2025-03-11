import os
import re
# import mimetypes
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from database.requests import set_user, set_language, check_user, check_language, set_uploaded_text, set_questions, set_questions_response, get_text
from app.keyboard import questions_keyboard, main_menu_keyboard, language_kb
from app.logic import time_now, transcribe_audio, AskingOpenAI

router = Router()

ALLOWED_EXTENSIONS = {".mp3", ".wav", ".flac", ".m4a", ".ogg", ".webm", ".mp4"}
ALLOWED_MIME_TYPES = {"audio/mpeg", "audio/wav", "audio/flac", "audio/mp4", "audio/ogg", "audio/webm", "video/mp4", "video/webm"}
YOUTUBE_REGEX = re.compile(r"^(https?:\/\/)?(www\.)?(youtube\.com\/(watch\?v=|embed\/|v\/)|youtu\.be\/)[\w-]+")
PROMPT_SUMM = "Ты — помощник, который кратко резюмирует текст."

def prompt_answer_quest(context: str):
    ask_quest =  "Нужно ответить на вопрос. Исходя из контекста: {context}"
    return ask_quest

user_data = {}
class user(StatesGroup):
    choose_lang = State()
    ask_quest = State()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    if await check_user(message.from_user.id):
        await message.answer("Можешь отправить мне аудио файл / голосовое сообщение / ссылку на ютуб и я сгенерирую сводку по нему.")
    else:
        await state.update_data(callbacks=[])  # Создаём пустой список
        await set_user(message.from_user.id, message.from_user.username, time_now())
        await state.set_state(user.choose_lang)
        await message.answer("Привет! Я могу делать сводку по информации которую ты мне предоставишь.\nДля начала выбери язык:", 
                             reply_markup=language_kb())
        

@router.callback_query(user.choose_lang, F.data.startswith("language_"))
async def collect_callback(callback: CallbackQuery, state: FSMContext):
    language = callback.data.split("_")[1]
    set_language(callback.from_user.id, language.upper())
    await callback.message.answer(f"✅ Ваш язык сохранён: {language.upper()}")
    await state.clear()
    await callback.answer()


@router.message(F.voice)
async def handle_voice_message(message: Message):
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
    
    await message.answer(f"Вот что я понял из твоего голосового:\n\n{transcript}")
    
    os.remove(local_file)

    await message.answer("Генерирую сводку, подождите немного...")
    summary_text = await AskingOpenAI(user_data[message.from_user.id]["uploaded_text"], PROMPT_SUMM)
    user_data[message.from_user.id]["response"] = summary_text

    await set_uploaded_text(time_now(), message.from_user.id, user_data[message.from_user.id]["uploaded_text"], user_data[message.from_user.id]["response"])
    del user_data[message.from_user.id]

    await message.answer(f"Сводка готова:\n{summary_text}", reply_markup=questions_keyboard())
    

@router.message(F.text.regexp(YOUTUBE_REGEX))
async def handle_youtube_link(message: Message):
    await message.answer("Генерирую сводку...")
    

@router.message(F.document | F.audio)
async def check_audio_file(message: Message):
    if message.document:
        file_name = message.document.file_name
        file_ext = file_name[file_name.rfind(".") :].lower()
        mime_type = message.document.mime_type
    elif message.audio:
        file_ext = message.audio.file_name[message.audio.file_name.rfind(".") :].lower()
        mime_type = message.audio.mime_type
    else:
        return  # Если это не документ и не аудио, просто выходим

    # Проверяем расширение и MIME-тип
    if file_ext in ALLOWED_EXTENSIONS and mime_type in ALLOWED_MIME_TYPES:
        # await message.answer("✅ Файл подходит для обработки в Whisper!")
        pass
    else:
        await message.answer('❌ Неподдерживаемый формат файла.\nДля транскрипции отправьте:\n".mp3", ".wav", ".flac", ".m4a", ".ogg", ".webm", ".mp4"')
        
@router.callback_query(F.data.startswith("question"))
async def ask_question(callback: CallbackQuery, state: FSMContext):
    await state.set_state(user.ask_quest)
    await callback.answer("Введите ваш вопрос")
    
@router.message(user.ask_quest)
async def response_ask(message: Message, state: FSMContext):
    context = await get_text(message.from_user.id)
    await set_questions(message.from_user.id, message.text)
    answer = await AskingOpenAI(message.text, prompt_answer_quest(context))
    await set_questions_response(message.from_user.id, answer)
    await message.answer(f"Вот ответ на твой вопрос:\n{answer}")
    await state.clear()