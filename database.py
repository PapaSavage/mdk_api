from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import asyncio

DATABASE_URL = "mysql+aiomysql://p684612_mdk_bd_d:MidNightHero123@p684612.mysql.ihc.ru/p684612_mdk_bd_d"


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

    async def get_orders_by_user(self, user_id):
        async with self.async_session() as session:
            stmt = text(
                "SELECT o.OrderID,u.Name AS customer_name, u.Phonenumber AS customer_phone, u.Email AS customer_email, o.Status, o.Description AS order_description, (SELECT GROUP_CONCAT(g.GoodID, '-', g.NameGood, '-', g.CategoryID, '-', g.Price) FROM orderitem ot JOIN good g ON g.GoodID = ot.GoodID WHERE ot.OrderID = o.OrderID) as order_details FROM orders o JOIN user u ON o.UserID = u.UserID where u.UserID = :user_id;"
            )
            order_params = {
                "user_id": user_id,
            }
            result = await session.execute(stmt, order_params)
            orders = result.all()
            await session.commit()
            orders_with_items = []

            for order in orders:
                # Преобразуем строку order[6] (order_description) в список, разделяя по '-'
                order_description_parts = order[6].split(",")

                # Создаем новый список, содержащий информацию о заказе и список товаров
                order_with_items = list(order)  # Создаем копию списка order
                order_with_items[6] = list(
                    map(
                        lambda x: x.split("-"),
                        order_description_parts,
                    )
                )

                dumplist = list()

                for good in order_with_items[6]:
                    dumplist.append(
                        {
                            "id": int(good[0]),
                            "title": good[1],
                            "category": int(good[2]),
                            "price": float(good[3]),
                        }
                    )

                order_with_items[6] = dumplist

                # Заменяем order_description на список товаров
                orders_with_items.append(order_with_items)

            print(orders_with_items)

            return orders_with_items

    async def get_orders(self):
        async with self.async_session() as session:
            order_stmt = text(
                "SELECT o.OrderID ,u.Surname AS customer_surname ,u.Name AS customer_name, u.Lastname AS customer_lastname, u.Phonenumber AS customer_phone, u.Email AS customer_email, o.Status, o.Description AS order_description, (SELECT GROUP_CONCAT(g.GoodID, '-', g.NameGood, '-', g.CategoryID, '-', g.Price, '-', ot.Quantity) FROM orderitem ot JOIN good g ON g.GoodID = ot.GoodID WHERE ot.OrderID = o.OrderID) as order_details FROM orders o JOIN user u ON o.UserID = u.UserID;"
            )
            order_result = await session.execute(order_stmt)
            orders = order_result.all()

            orders_with_items = []

            for order in orders:
                # Преобразуем строку order[6] (order_description) в список, разделяя по '-'
                order_description_parts = order[8].split(",")

                # Создаем новый список, содержащий информацию о заказе и список товаров
                order_with_items = list(order)  # Создаем копию списка order
                order_with_items[8] = list(
                    map(
                        lambda x: x.split("-"),
                        order_description_parts,
                    )
                )

                dumplist = list()

                for good in order_with_items[8]:
                    dumplist.append(
                        {
                            "id": int(good[0]),
                            "title": good[1],
                            "category": int(good[2]),
                            "price": float(good[3]),
                            "quantity": int(good[4]),
                        }
                    )

                order_with_items[8] = dumplist

                # Заменяем order_description на список товаров
                orders_with_items.append(order_with_items)

            print(orders_with_items)

            return orders_with_items

    async def get_category(self):
        async with self.async_session() as session:
            stmt = text("SELECT CategoryID, NameCat FROM category;")
            result = await session.execute(stmt, {"age_threshold": 30})
            rows = result.all()
            await session.commit()
            return rows

    async def post_order(self, order_item):
        try:
            async with self.async_session() as session:

                user_stmt = text("Select UserID from user where UserID = :user_id;")
                user_params = {
                    "user_id": order_item.customer_id,
                }
                user_result = await session.execute(user_stmt, user_params)
                await session.commit()
                user_result = user_result.all()
                user_id = order_item.customer_id
                inserted_id = None

                if len(user_result) == 0:
                    if order_item.customer_id != None:
                        user_stmt = text(
                            "INSERT INTO user (UserID, Surname, Name, Lastname, Phonenumber, Email) VALUES (:user_id, :surname, :name, :lastname, :phone, :email);"
                        )
                        user_params = {
                            "user_id": order_item.customer_id,
                            "surname": order_item.customer_surname,
                            "name": order_item.customer_name,
                            "lastname": order_item.customer_lastname,
                            "phone": order_item.customer_phone,
                            "email": order_item.customer_email,
                        }
                        user_result = await session.execute(user_stmt, user_params)
                        await session.commit()
                    else:
                        user_stmt = text(
                            "INSERT INTO user (Surname, Name, Lastname, Phonenumber, Email) VALUES (:surname, :name, :lastname, :phone, :email);"
                        )
                        user_params = {
                            "surname": order_item.customer_surname,
                            "name": order_item.customer_name,
                            "lastname": order_item.customer_lastname,
                            "phone": order_item.customer_phone,
                            "email": order_item.customer_email,
                        }
                        user_result = await session.execute(user_stmt, user_params)
                        await session.commit()
                        inserted_id = user_result.lastrowid
                else:
                    user_stmt = text(
                        "UPDATE user SET Surname = :surname, Name = :name, Lastname = :lastname, Phonenumber = :phone, Email = :email WHERE UserID = :user_id;"
                    )
                    user_params = {
                        "user_id": order_item.customer_id,
                        "surname": order_item.customer_surname,
                        "name": order_item.customer_name,
                        "lastname": order_item.customer_lastname,
                        "phone": order_item.customer_phone,
                        "email": order_item.customer_email,
                    }
                    user_result = await session.execute(user_stmt, user_params)
                    await session.commit()

                order_stmt = text(
                    "INSERT INTO orders (UserID, Status, Description, Address) VALUES (:user_id, :status, :description, :address);"
                )
                print(inserted_id)
                if inserted_id != None:
                    order_params = {
                        "user_id": inserted_id,
                        "status": order_item.status,
                        "description": order_item.description,
                        "address": order_item.order_address,
                    }
                else:
                    order_params = {
                        "user_id": user_id,
                        "status": order_item.status,
                        "description": order_item.description,
                        "address": order_item.order_address,
                    }
                order_result = await session.execute(order_stmt, order_params)
                await session.commit()
                order_id = order_result.lastrowid

                for good in order_item.goods:
                    order_item_stmt = text(
                        "INSERT INTO orderitem (OrderID, GoodID, Quantity) VALUES (:order_id, :good_id, :quantity);"
                    )
                    order_item_params = {
                        "order_id": order_id,
                        "good_id": good.id,
                        "quantity": good.quantity,
                    }
                    await session.execute(order_item_stmt, order_item_params)
                    await session.commit()
                return order_id
        except SQLAlchemyError as e:
            print(f"Ошибка при выполнении операции INSERT: {e}")

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

    async def put_orders(self, order_id, status):
        try:
            async with self.async_session() as session:
                stmt = text(
                    "UPDATE orders SET Status = :status WHERE OrderID = :order_id;"
                )
                params = {
                    "status": status,
                    "order_id": order_id,
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
                    "good_id": item_id,
                }
                result = await session.execute(stmt, params)
                await session.commit()  # Подтверждаем транзакцию после успешного выполнения
        except SQLAlchemyError as e:
            print(f"Ошибка при выполнении операции INSERT: {e}")
