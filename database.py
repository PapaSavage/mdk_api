from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import asyncio

DATABASE_URL = (
    "mysql+aiomysql://p684612_mdk_bd:w68h46U2KR@p684612.mysql.ihc.ru/p684612_mdk_bd"
)


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
            await session.commit()
            return rows
        

    async def get_orders(self):
        async with self.async_session() as session:
            # Запрос информации о заказах
            order_stmt = text(
                "SELECT "
                "   o.OrderID, "
                "   u.Name AS customer_name, "
                "   u.Phonenumber AS customer_phone, "
                "   u.Email AS customer_email, "
                "   o.Status, "
                "   o.Description AS order_description "
                "FROM "
                "   orders o "
                "JOIN "
                "   user u ON o.UserID = u.UserID;"
            )
            order_result = await session.execute(order_stmt)
            orders = order_result.all()
            # orders_with_items = []
            # async for order in order_result:
            #     order_dict = dict(order)
            #     order_id = order_dict['OrderID']
            #     item_stmt = text(
            #         "SELECT "
            #         "   g.NameGood AS title, "
            #         "   g.CategoryID AS category, "
            #         "   g.Price "
            #         "FROM "
            #         "   orderitem oi "
            #         "JOIN "
            #         "   good g ON oi.GoodID = g.GoodID "
            #         "WHERE "
            #         "   oi.OrderID = :order_id;"
            #     )
            #     item_result = await session.execute(item_stmt, {"order_id": order_id})
            #     items = []
            #     async for item in item_result:
            #         items.append(dict(item))
            #     order_dict['items'] = items
            #     orders_with_items.append(order_dict)

            # await session.commit()
            return(orders)



    async def get_category(self):
        async with self.async_session() as session:
            stmt = text("SELECT CategoryID, NameCat FROM category;")
            result = await session.execute(stmt, {"age_threshold": 30})
            rows = result.all()
            await session.commit()
            return rows

    async def post_goods(self, file, title, category, price):
        try:
            async with self.async_session() as session:
                stmt = text(
                    "INSERT INTO good (NameGood, CategoryID, Price, Images) VALUES (:name, :category_id, :price, :image);"
                )
                params = {
                    "name": title,
                    "category_id": category,
                    "price": price,
                    "image": file,
                }
                result = await session.execute(stmt, params)
                await session.commit()

                return True
                # Подтверждаем транзакцию после успешного выполнения

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

    async def put_good_without_image(self, title, category, price, item_id):
        try:
            async with self.async_session() as session:
                stmt = text(
                    "UPDATE good SET NameGood = :name, CategoryID = :category_id, Price = :price WHERE GoodID = :good_id;"
                )
                params = {
                    "name": title,
                    "category_id": category,
                    "price": price,
                    "good_id": item_id,
                }
                result = await session.execute(stmt, params)
                await session.commit()

        except SQLAlchemyError as e:
            print(f"Ошибка при выполнении операции INSERT: {e}")

    async def put_good_with_image(self, file, title, category, price, item_id):
        try:
            async with self.async_session() as session:
                stmt = text(
                    "UPDATE good SET NameGood = :name, CategoryID = :category_id, Price = :price, Images = :image WHERE GoodID = :good_id;"
                )
                params = {
                    "name": title,
                    "category_id": category,
                    "price": price,
                    "good_id": item_id,
                    "image": file,
                }
                result = await session.execute(stmt, params)
                await session.commit()

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

    async def put_image(self, contents, item_id):
        try:
            async with self.async_session() as session:
                stmt = text("UPDATE good SET Images = :image WHERE GoodID = :good_id;")
                params = {
                    "image": contents,
                    "id": item_id,
                }
                result = await session.execute(stmt, params)
                await session.commit()  # Подтверждаем транзакцию после успешного выполнения
        except SQLAlchemyError as e:
            print(f"Ошибка при выполнении операции INSERT: {e}")
