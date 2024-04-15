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
            stmt = text(
                "SELECT goodID, NameGood, CategoryID, Price, TO_BASE64(Images) FROM good;"
            )
            result = await session.execute(stmt, {"age_threshold": 30})
            rows = result.all()
            print(rows)
            await session.commit()
            return rows

    async def get_category(self):
        async with self.async_session() as session:
            stmt = text("SELECT CategoryID, NameCat FROM category;")
            result = await session.execute(stmt, {"age_threshold": 30})
            rows = result.all()
            await session.commit()
            return rows

    async def post_goods(self, product):
        try:
            async with self.async_session() as session:
                stmt = text(
                    "INSERT INTO good (NameGood, CategoryID, Price) VALUES (:name, :category_id, :price);"
                )
                params = {
                    "name": product.title,
                    "category_id": product.category,
                    "price": product.price,
                }
                result = await session.execute(stmt, params)
                await session.commit()  # Подтверждаем транзакцию после успешного выполнения
                return product
        except SQLAlchemyError as e:
            print(f"Ошибка при выполнении операции INSERT: {e}")

    async def post_categories(self, category):
        try:
            async with self.async_session() as session:
                stmt = text("INSERT INTO category (NameCat) VALUES (:name_category);")
                params = {
                    "name_category": category.title,
                }
                result = await session.execute(stmt, params)
                await session.commit()  # Подтверждаем транзакцию после успешного выполнения
                return category
        except SQLAlchemyError as e:
            print(f"Ошибка при выполнении операции INSERT: {e}")

    async def put_good(self, product, item_id):
        try:
            async with self.async_session() as session:
                stmt = text(
                    "UPDATE good SET NameGood = :name, CategoryID = :category_id, Price = :price WHERE GoodID = :good_id;"
                )
                params = {
                    "name": product.title,
                    "category_id": product.category,
                    "price": product.price,
                    "good_id": item_id,
                }
                result = await session.execute(stmt, params)
                await session.commit()  # Подтверждаем транзакцию после успешного выполнения
                return product
        except SQLAlchemyError as e:
            print(f"Ошибка при выполнении операции INSERT: {e}")

    async def delete_product(self, item_id):
        try:
            async with self.async_session() as session:
                stmt = text("DELETE FROM good WHERE GoodID = :good_id;")
                params = {
                    "good_id": item_id,
                }
                result = await session.execute(stmt, params)
                await session.commit()  # Подтверждаем транзакцию после успешного выполнения

        except SQLAlchemyError as e:
            print(f"Ошибка при выполнении операции INSERT: {e}")

    async def delete_category(self, item_id):
        try:
            async with self.async_session() as session:
                stmt = text("DELETE FROM category WHERE CategoryID = :category_id;")
                params = {
                    "category_id": item_id,
                }
                result = await session.execute(stmt, params)
                await session.commit()  # Подтверждаем транзакцию после успешного выполнения

        except SQLAlchemyError as e:
            print(f"Ошибка при выполнении операции INSERT: {e}")
