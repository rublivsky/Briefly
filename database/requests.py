from sqlalchemy import select, update, insert, text
from database.models import async_session, Users, Responses
from datetime import datetime

def connection(func):
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)
    return wrapper

@connection
async def set_user(session, telegram_id, username, bus_datetime):
    user = await session.scalar(select(Users).where(Users.telegram_id == telegram_id))
    if not user:
        session.add(Users(bus_datetime=bus_datetime,
                          telegram_id=telegram_id, 
                          username=username,
                          pref_language='RU'))
        await session.commit()
        return False
    else:
        return user
    
@connection
async def set_uploaded_text(session, bus_datetime, telegram_id, uploaded_text, response):
    session.add(Responses(bus_datetime=bus_datetime,
                          telegram_id=telegram_id,
                          uploaded_text=uploaded_text,
                          response=response))
    await session.commit()

@connection
async def set_language(session, telegram_id, language):
    await session.execute(update(Users).where(Users.telegram_id == telegram_id).values(pref_language=language))
    await session.commit()
    
@connection
async def check_user(session, telegram_id):
    user = await session.scalar(select(Users).where(Users.telegram_id == telegram_id))
    return user

@connection
async def check_language(session, telegram_id):
    user = await session.scalar(select(Users).where(Users.telegram_id == telegram_id))
    return user.pref_language

# @connection
# async def save_response_to_db(session, user_id: int, response: str):
#     async with SessionLocal() as session:
#         new_entry = UserResponse(user_id=user_id, response=response)
#         session.add(new_entry)
#         await session.commit()