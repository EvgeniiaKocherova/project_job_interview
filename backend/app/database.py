import os
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Создаем АСИНХРОННЫЙ движок
async_engine = create_async_engine(DATABASE_URL, echo=True)

async def create_db_and_tables():
    # Специальный мост для создания таблиц через асинхронный движок
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    # Асинхронная сессия для работы с БД в эндпоинтах
    async with AsyncSession(async_engine) as session:
        yield session