from sqlalchemy import select, update, insert, text
from database.models import async_session, Users, Responses
from datetime import datetime

def connection(func):
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)
    return wrapper

@connection
async def set_user(session, telegram_id, username):
    user = await session.scalar(select(Users).where(Users.telegram_id == telegram_id))
    if not user:
        session.add(Users(bus_datetime=datetime.now().strftime('%d.%m.%Y %H:%M:%S'), 
                          telegram_id=telegram_id, 
                          username=username))
        await session.commit()
        return False
    else:
        return user
    
@connection
async def set_language(session, telegram_id, language):
    await session.execute(update(Users).where(Users.telegram_id == telegram_id).values(pref_language=language))
    await session.commit()
    
@connection
async def check_user(session, telegram_id):
    user = await session.scalar(select(Users).where(Users.telegram_id == telegram_id))
    return user

