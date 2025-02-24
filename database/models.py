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
    bus_datetime: Mapped[DateTime] = mapped_column(DateTime,)
    telegram_id = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column(String(length=30), nullable=True)
    pref_language: Mapped[str] = mapped_column(String(length=10), default="RU")

class Responses(Base):
    __tablename__ = "responses"
    id: Mapped[int] = mapped_column(primary_key=True)
    bus_datetime: Mapped[DateTime] = mapped_column(DateTime,)
    telegram_id = mapped_column(BigInteger, ForeignKey(Users.telegram_id))
    uploaded_text: Mapped[str] = mapped_column(String(length=4000))
    response: Mapped[str] = mapped_column(String(length=2000))
    question: Mapped[str] = mapped_column(String(length=200), nullable=True)
    question_response: Mapped[str] = mapped_column(String(length=1000), nullable=True)

async def async_main():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)