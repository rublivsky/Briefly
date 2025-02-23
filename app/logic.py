import os
import pytz
import aiohttp
from dotenv import load_dotenv
from datetime import datetime
from openai import AsyncOpenAI

load_dotenv()

def time_now():
    tz = pytz.timezone('Europe/Kiev')  # Заменить на свой нужный часовой пояс
    return datetime.now(tz)

async def transcribe_audio(file_path: str, pref_language: str) -> str:
    """Отправляет аудиофайл в OpenAI Whisper (асинхронно)"""
    openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    async with aiohttp.ClientSession() as session:
        with open(file_path, "rb") as audio_file:
            response = await openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language=pref_language
            )
    return response.text  # Whisper возвращает транскрипцию
