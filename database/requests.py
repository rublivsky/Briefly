from sqlalchemy import select, update, insert, text
from database.models import async_session, Users, Responses

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

@connection
async def set_questions(session, telegram_id, question):
    response = await session.scalar(select(Responses).where(Responses.telegram_id == telegram_id).order_by(Responses.bus_datetime.desc()))
    if response:
        await session.execute(update(Responses).where(Responses.id == response.id).values(questions=question))
        await session.commit()

@connection
async def set_questions_response(session, telegram_id, questions_response):
    response = await session.scalar(select(Responses).where(Responses.telegram_id == telegram_id).order_by(Responses.bus_datetime.desc()))
    if response:
        await session.execute(update(Responses).where(Responses.id == response.id).values(questions_response=questions_response))
        await session.commit()

@connection
async def get_text(session, telegram_id):
    response = await session.scalar(select(Responses).where(Responses.telegram_id == telegram_id))
    return response.uploaded_text