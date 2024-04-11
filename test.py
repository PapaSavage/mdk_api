from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import asyncio

DATABASE_URL = "mysql+aiomysql://root:@localhost/mdk_bd"


class workwithbd:
    def __init__(self) -> None:
        self.engine = create_async_engine(DATABASE_URL, echo=True, future=True)

        self.async_session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

        self.Base = declarative_base()

    async def check_connection(self):
        try:
            async with self.async_session() as session:
                # Use SQLAlchemy's text construct to execute raw SQL
                result = await session.execute(text("SELECT 1"))
                print("Подключение к базе данных успешно!")
        except SQLAlchemyError as e:
            print(f"Ошибка подключения к базе данных: {e}")

    async def get_goods(self):
        async with self.async_session() as session:
            stmt = text("SELECT goodID, NameGood, СategoryID, Price, Images FROM good;")
            result = await session.execute(stmt, {"age_threshold": 30})
            rows = result.all()
            return rows

    async def get_category(self):
        async with self.async_session() as session:
            stmt = text("SELECT goodID, NameGood, СategoryID, Price, Images FROM good;")
            result = await session.execute(stmt, {"age_threshold": 30})
            rows = result.all()
            return rows
