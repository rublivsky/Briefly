import os
import pytz
import aiohttp
from dotenv import load_dotenv
from datetime import datetime
from openai import AsyncOpenAI
import yt_dlp as youtube_dl

load_dotenv()
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def time_now():
    tz = pytz.timezone('Europe/Kiev')
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

async def AskingOpenAI(text: str, prompt: str):
    try:
        response = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text}
            ]
        )

        summary = response.choices[0].message.content
        return summary
    except Exception as e:
        return f"Ошибка при обработке запроса: {e}"
    
    
async def get_youtube_subtitles_or_transcribe(url: str, pref_language: str) -> str:
    ydl_opts = {
        'writesubtitles': True,
        'subtitleslangs': [pref_language],
        'skip_download': True,
        'quiet': True,
        'verbose': True
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(url, download=False)
        except Exception as e:
            return f"Произошла ошибка при обработке видео: {e}"
        
        subtitles = info_dict.get('subtitles', {})

        if pref_language in subtitles:
            subtitle_url = subtitles[pref_language][0]['url']
            async with aiohttp.ClientSession() as session:
                async with session.get(subtitle_url) as response:
                    subtitle_text = await response.text()
            return subtitle_text
        else:
            file_name = f"{info_dict['id']}.mp3"
            audio_file_path = f'/tmp/{file_name}'
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(audio_file_path), exist_ok=True)
            
            ydl_opts['outtmpl'] = audio_file_path
            ydl_opts['format'] = 'bestaudio/best'
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return await transcribe_audio(audio_file_path, pref_language)
