import mysql.connector

class connection:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            if self.connection.is_connected():
                print(f"Успешно подключено к базе данных: {self.database}")
                self.cursor = self.connection.cursor()
                return self.cursor

        except mysql.connector.Error as err:
            print(f"Ошибка: {err}")


class workwithbd(connection):
    def auth(self, login, password):
        # self.connect()  

        query = "SELECT * FROM user WHERE Login = %s  AND Password = %s"
        self.cursor.execute(query,(login, password))

        rows = self.cursor.fetchall()
        

        if len(rows) > 0:
            print("Авторизация успешна.")
            row = rows[-1]
            print(row[-1])
            return row[-1]
        else:
            print("Неверные учетные данные.")
            return 2

    def register(self, login, password):
            # self.connect()  

            query = "SELECT * FROM user WHERE Login = %s "
            self.cursor.execute(query, (login,))

            rows = self.cursor.fetchall()


            if len(rows) == 0:
                query1 = f"""INSERT INTO user (UserID, Surname, Name, Lastname, Phonenumber, Email, Login, Password, ISAdmin) VALUES (null, null, null, null, null, null, '{login}', '{password}', '0');"""
                self.cursor.execute(query1)
                self.connection.commit()


                return True
            else:
                print("Найдено совпадение пользователя.")
                return False
            
    def userID(self, login, password):
        query = "SELECT userID FROM user WHERE Login = %s AND Password = %s"
        self.cursor.execute(query, (login,password))

        rows = self.cursor.fetchall()
        return rows[0][0]
                  
    def settings(self, login, password):
            # self.connect()  

            query = "SELECT * FROM user WHERE Login = %s AND Password = %s"
            self.cursor.execute(query, (login,password))

            rows = self.cursor.fetchall()
            row = rows[-1]
            print(row)
            return row
            
    def savechanges(self, login, password, row):
            #  self.connect()  

            query = """
            SELECT login 
            from user 
            WHERE Login = %s 
            """
            self.cursor.execute(query, (row[5],))
            rows = self.cursor.fetchall()
            print(rows[0][0], login)
            if rows == 0 or rows[0][0] == login:
                query = """
                UPDATE user 
                SET Surname = %s, Name = %s, Lastname = %s, Phonenumber = %s, Email = %s, Login = %s, Password = %s 
                WHERE Login = %s AND Password = %s
                """
                
                values = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], login, password)

                self.cursor.execute(query, values)
                self.connection.commit()
                return True
            else:
                return False
    
    def admin(self):
            #  self.connect()  

            query = "SELECT good.GoodID, good.NameGood, category.NameCat, good.Price, good.Image, good.Description, good.good FROM good LEFT JOIN category ON good.СategoryID = category.CategoryID; "
            self.cursor.execute(query)

            rows = self.cursor.fetchall()
            return rows
    
    def savegood(self, row):
            # self.connect()  
            if row[0] != '':
                query = "SELECT * FROM good WHERE GoodID = %s"
                self.cursor.execute(query, (row[0],))
                rows = self.cursor.fetchall()
            else:
                 rows = []

            
            if len(rows) == 0:
                query1 = "INSERT INTO good (GoodID, NameGood, СategoryID, Price, Image, Description, good) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                self.cursor.execute(query1, (row[0], row[1], int(row[2]), row[4], row[5], row[3], row[6]))
                self.connection.commit()
                return True
            else:
                
                return False
                 
    def viewgood(self, id):
            # self.connect()  

            query = "SELECT * FROM good WHERE GoodID = %s"
            self.cursor.execute(query, (id,))

            rows = self.cursor.fetchall()
            row = rows[-1]
            # print(row)
            return row  
         

    def changegood(self, row, id):
            # self.connect()  
            if  row[5] == 1:
                query1 = "UPDATE good SET NameGood = %s, СategoryID = %s, Price = %s, Description = %s, good = %s WHERE GoodID = %s"
                self.cursor.execute(query1, (row[1], int(row[2]), row[4], row[3], row[6], id))
                self.connection.commit()
            else:     
                query1 = "UPDATE good SET NameGood = %s, СategoryID = %s, Price = %s, Image = %s, Description = %s, good = %s WHERE GoodID = %s"
                self.cursor.execute(query1, (row[1], int(row[2]), row[4], row[5], row[3], row[6], id))
                self.connection.commit()
            return True


    def viewapps(self):
            # self.connect()  

            query = "SELECT goodID, NameGood, Price, image FROM good WHERE  СategoryID = 1"
            self.cursor.execute(query)

            rows = self.cursor.fetchall()
            
            # print(rows)
            return rows

    def findapps(self, s):
            # self.connect()  

            query = "SELECT goodID, NameGood, Price, image FROM good WHERE СategoryID = 1 AND NameGood LIKE %s"
            self.cursor.execute(query, ('%' + s + '%',))

            rows = self.cursor.fetchall()
            
            # print(rows)
            return rows
    
    def findgames(self, s):
            # self.connect()  

            query = "SELECT goodID, NameGood, Price, image FROM good WHERE СategoryID = 2 AND NameGood LIKE %s"
            self.cursor.execute(query, ('%' + s + '%',))

            rows = self.cursor.fetchall()
            
            # print(rows)
            return rows

    def viewgames(self):
            # self.connect()  

            query = "SELECT goodID, NameGood, Price, image  FROM good WHERE  СategoryID = 2"
            self.cursor.execute(query)

            rows = self.cursor.fetchall()
            
            # print(rows)
            return rows
    
    def viewcart(self,userid):
            # self.connect() 
            
            query = """
                SELECT cartitem.cartitemID, good.NameGood, good.Price, cartitem.Quantity 
                FROM cart 
                JOIN user ON cart.UserID = user.UserID 
                JOIN cartitem ON cart.CartID = cartitem.CartID 
                JOIN good ON cartitem.GoodID = good.GoodID 
                WHERE cart.userid = %s  AND cart.status = 'In Cart'
            """

            self.cursor.execute(query, (userid,))
            rows = self.cursor.fetchall()
            print(rows)

            if len(rows) > 0:
                return rows
            else:
                rows = []
                return rows
            
    def add_to_cart(self, userid, id):
         # self.connect()
        query = """
                SELECT cartID
                FROM cart  
                WHERE UserID = %s AND status = 'In Cart'
            """

        self.cursor.execute(query, (userid,))
        rows = self.cursor.fetchall()
        cartid = rows[0][0]
        query = """
                SELECT cartitemid
                FROM cartitem  
                WHERE cartID = %s AND GoodID = %s
            """

        self.cursor.execute(query, (cartid, id))
        rows = self.cursor.fetchall()
        if len (rows) == 0:
            query = "INSERT INTO cartitem (cartitemID, CartID, GoodID, Quantity) VALUES (null, %s, %s, 1)"

            self.cursor.execute(query, (cartid,id))
            self.connection.commit()
        else:
            cartitemid = rows[0][0]
            query = """
                SELECT quantity
                FROM cartitem 
                WHERE cartitemID = %s 
            """
            self.cursor.execute(query, (cartitemid,))
            rows = self.cursor.fetchall()


            quantity = rows[0][0]
            query1 = "UPDATE cartitem SET quantity = %s WHERE cartitemID = %s"
            self.cursor.execute(query1, (quantity + 1, cartitemid))
            self.connection.commit()
             


    def checkcart(self, userid):
         # self.connect()
        query = """
                SELECT cartID
                FROM cart 
                WHERE UserID = %s AND cart.status = 'In Cart'
            """

        self.cursor.execute(query, (userid,))
        rows = self.cursor.fetchall()

        if len (rows) == 0:
            print(userid)
            query = "INSERT INTO cart (cartID, UserID, Status) VALUES (null, %s, 'In Cart')"
            self.cursor.execute(query, (int(userid),))
            self.connection.commit()
            return True
        else:
            return True
                 
             
    def plus(self, id):
            # self.connect()  
            query = """
                SELECT quantity
                FROM cartitem 
                WHERE cartitemID = %s 
            """
            self.cursor.execute(query, (id,))
            rows = self.cursor.fetchall()
            quantity = rows[0][0]
            query1 = "UPDATE cartitem SET quantity = %s WHERE cartitemID = %s"
            self.cursor.execute(query1, (quantity+1, id))
            self.connection.commit()
            return True    

    def minus(self, id):
         # self.connect()
        query = """
            SELECT quantity
            FROM cartitem 
            WHERE cartitemID = %s 
        """
        self.cursor.execute(query, (id,))
        rows = self.cursor.fetchall()


        quantity = rows[0][0]
        
        if quantity == 1:
            query1 = "DELETE FROM cartitem WHERE cartitemID = %s"
            self.cursor.execute(query1, (id,))
            self.connection.commit()
        else:     
            query1 = "UPDATE cartitem SET quantity = %s WHERE cartitemID = %s"
            self.cursor.execute(query1, (quantity - 1, id))
            self.connection.commit()

        return True

    def delete(self, id):
         # self.connect()
       
        query1 = "DELETE FROM cartitem WHERE cartitemID = %s"
        self.cursor.execute(query1, (id,))
        self.connection.commit()


        return True
    
    def deletegood(self, id):
         # self.connect()
       
        query1 = "DELETE FROM good WHERE goodID = %s"
        self.cursor.execute(query1, (id,))
        self.connection.commit()


        return True
    
    def payment(self, userid, sum):
         # self.connect()
        query = """
            SELECT cartid
            FROM cart 
            WHERE UserID = %s AND status = 'In Cart' 
        """
        self.cursor.execute(query, (userid,))
        rows = self.cursor.fetchall()


        cartid = rows[0][0]

        query = """
                UPDATE Cart
                SET status = 'Paid'
                WHERE UserID = %s AND status = 'In Cart'
            """

        self.cursor.execute(query, (userid,))
        self.connection.commit() 

        query1 = "insert into payment (PaymentID, userid, cartid, amount, paymentdate) values (null, %s, %s, %s, NOW())"
        self.cursor.execute(query1, (userid, cartid, sum))
        self.connection.commit()
        return True
    

    def history(self, userid):
         # self.connect()
        query = """
            SELECT payment.paymentDate, good.NameGood, good.Price, cartitem.Quantity, good.Good 
            FROM payment
            JOIN cart ON payment.cartID = cart.cartID 
            JOIN user ON cart.UserID = user.UserID 
            JOIN cartitem ON cart.CartID = cartitem.CartID 
            JOIN good ON cartitem.GoodID = good.GoodID 
            WHERE payment.userid = %s  AND cart.status = 'Paid'
        """
        self.cursor.execute(query, (userid,))
        rows = self.cursor.fetchall()
        if len (rows) == 0:
            return []
        else:
             return rows
        
    def receit(self, userid):
         # self.connect()
        query = """
        SELECT
            payment.paymentDate,
            good.NameGood,
            good.Price,
            cartitem.Quantity,
            good.Good
            
        FROM
            payment
        JOIN cart ON payment.cartID = cart.cartID
        JOIN cartitem ON cart.CartID = cartitem.CartID
        JOIN good ON cartitem.GoodID = good.GoodID
        WHERE
            payment.userid = %s
            AND cart.status = 'Paid'
            AND payment.paymentDate = (
                SELECT MAX(paymentDate)
                FROM payment
                WHERE userid = %s
                AND cart.status = 'Paid'
            );

        """
        self.cursor.execute(query, (userid,userid))
        rows = self.cursor.fetchall()
        if len (rows) == 0:
            return []
        else:
             return rows
        

    def otchet(self):
         # self.connect()
        query = """
        SELECT
            payment.paymentDate,
            good.NameGood,
            good.Price,
            cartitem.Quantity        
        FROM
            payment
        JOIN cart ON payment.cartID = cart.cartID
        JOIN cartitem ON cart.CartID = cartitem.CartID
        JOIN good ON cartitem.GoodID = good.GoodID
        WHERE cart.status = 'Paid'

        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        if len (rows) == 0:
            return []
        else:
             return rows
             
