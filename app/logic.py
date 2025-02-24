import os
import pytz
import aiohttp
from dotenv import load_dotenv
from datetime import datetime
from openai import AsyncOpenAI

load_dotenv()

openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def time_now():
    tz = pytz.timezone('Europe/Kiev')  # Заменить на свой нужный часовой пояс
    return datetime.now(tz)

async def transcribe_audio(file_path: str, pref_language: str) -> str:
    async with aiohttp.ClientSession() as session:
        with open(file_path, "rb") as audio_file:
            response = await openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language=pref_language
            )
    return response.text

async def summarize_text(text: str):
    try:
        response = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ты — помощник, который кратко резюмирует текст."},
                {"role": "user", "content": text}
            ]
        )

        summary = response.choices[0].message.content
        return summary
    except Exception as e:
        return f"Ошибка при обработке запроса: {e}"
