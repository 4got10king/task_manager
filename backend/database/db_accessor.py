import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from pathlib import Path

from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase

logger = logging.getLogger("database")

class DatabaseAccessor:
    """
    Класс для работы с SQLite базой данных через асинхронное подключение.
    Поддерживает миграции через Alembic.
    """
    def __init__(self, database_url: str):
        """
        Args:
            database_url: URL для подключения к SQLite, например 'sqlite+aiosqlite:///./database.db'
        """
        self._database_url = database_url
        self._engine = None
        self._async_session_maker = None

    def run(self) -> None:
        """Инициализация подключения к базе данных"""
        self._engine = create_async_engine(
            self._database_url,
            connect_args={"check_same_thread": False},
            echo=False
        )
        
        self._async_session_maker = sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
            class_=AsyncSession
        )

    async def stop(self) -> None:
        """Закрытие соединения с базой данных"""
        if self._engine:
            await self._engine.dispose()

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Контекстный менеджер для получения сессии базы данных.
        
        Yields:
            AsyncSession: Асинхронная сессия SQLAlchemy
        """
        if not self._async_session_maker:
            raise RuntimeError("Database not initialized. Call .run() first")
            
        async with self._async_session_maker() as session:
            yield session

    async def init_db(self, Base: DeclarativeBase) -> None:
        """
        Создание всех таблиц в базе данных.
        Использовать только если не используется Alembic.
        
        Args:
            Base: Базовый класс моделей SQLAlchemy
        """
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def check_connection(self) -> None:
        """Проверка подключения к базе данных"""
        try:
            async with self.get_session() as session:
                await session.execute(text("SELECT 1"))
                logger.info("Successfully connected to SQLite database")
        except Exception as e:
            logger.error(f"Failed to connect to the database: {e}")
            raise

    async def check_alembic_version(self) -> None:
        """Проверка версии миграций Alembic"""
        try:
            async with self.get_session() as session:
                result = await session.execute(
                    text("SELECT version_num FROM alembic_version")
                )
                version = result.scalar()
                if version:
                    logger.info(f"Current Alembic version: {version}")
                else:
                    logger.warning("No Alembic version found")
        except ProgrammingError:
            logger.warning("Alembic version table not found. Migrations may not be applied")