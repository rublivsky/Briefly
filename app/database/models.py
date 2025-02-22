import os
import dotenv
from sqlalchemy import ForeignKey, String, BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession
import asyncpg
import sqlite3
import datetime

dotenv.load_dotenv()

DATABASE_URL = f"sqlite+aiosqlite:///{os.path.join(os.path.dirname(__file__), 'db.sqlite3')}"
# DATABASE_URL = os.getenv("DATABASE_URL", "").replace("postgres://", "postgresql+asyncpg://")
async_engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(async_engine, class_=AsyncSession)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    bus_datetime: Mapped[str] = mapped_column(DateTime, default=lambda: datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S'))
    telegram_id = mapped_column(BigInteger, nullable=True, unique=True)
    username: Mapped[str] = mapped_column(String(length=30), nullable=True)
    contact: Mapped[str] = mapped_column(String(length=20), nullable=True)

class Responses(Base):
    __tablename__ = "responses"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str] = mapped_column(DateTime, default=lambda: datetime.datetime.now().strftime('%d.%m.%Y'))
    time: Mapped[str] = mapped_column(DateTime, default=lambda: datetime.datetime.now().strftime('%H:%M:%S'))
    telegram_id = mapped_column(BigInteger, ForeignKey(Users.telegram_id))
    response: Mapped[str] = mapped_column(String(length=2000))
    date: Mapped[str] = mapped_column(DateTime)
    questions: Mapped[str] = mapped_column(String(length=200))
    questions_response: Mapped[str] = mapped_column(String(length=1000))

async def async_main():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)