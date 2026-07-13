from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

from app.models import Base, Task

# Загружаем переменные окружения
load_dotenv()

# Строка подключения к PostgreSQL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/reportflow_db"
)

# Создаём асинхронный движок
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=10,
    max_overflow=20
)

# Создаём фабрику сессий
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def init_db():
    """Инициализация БД - создаёт таблицы если их нет"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    """Получить сессию БД"""
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()


async def create_task(task_id: str, user_id: str, filename: str, input_file_path: str):
    """Создаёт новую задачу в БД"""
    async with async_session_factory() as session:
        task = Task(
            id=task_id,
            user_id=user_id,
            original_filename=filename,
            input_file_path=input_file_path,
            status="Processing"
        )
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return task


async def get_task(task_id: str):
    """Получает задачу по ID"""
    async with async_session_factory() as session:
        task = await session.get(Task, task_id)
        return task


async def update_task_status(
    task_id: str,
    status: str,
    pdf_file_path: str = None,
    chart_file_path: str = None,
    error_message: str = None
):
    """Обновляет статус задачи"""
    async with async_session_factory() as session:
        task = await session.get(Task, task_id)
        if task:
            task.status = status
            if pdf_file_path:
                task.pdf_file_path = pdf_file_path
            if chart_file_path:
                task.chart_file_path = chart_file_path
            if error_message:
                task.error_message = error_message
            await session.commit()
            await session.refresh(task)
        return task