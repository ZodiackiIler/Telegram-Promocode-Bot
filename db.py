import sqlite3
import mysql.connector

from config import MYSQL_ADDRESS, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD, MYSQL_PORT, SQLITE3_CONNECT, DATABASE_TYPE

class MySQLDatabase:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=MYSQL_ADDRESS,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        # Запрос для создания таблицы promo_exists
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS promo_exists (
                id               INT AUTO_INCREMENT PRIMARY KEY,
                promo_code       VARCHAR(255) NOT NULL,
                promocode_bal    VARCHAR(255) NOT NULL,
                promocode_count  VARCHAR(255) NOT NULL,
                promocode_coin   TEXT,
                promocode_desc   TEXT,
                promocode_active VARCHAR(255) NOT NULL,
                activate_enable  VARCHAR(5) DEFAULT 'True'
            )
        ''')

        # Запрос для создания таблицы users
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id        INT AUTO_INCREMENT PRIMARY KEY,
                user_id   VARCHAR(255) NOT NULL,
                username  VARCHAR(255) NOT NULL,
                promocode VARCHAR(255) NOT NULL
            )
        ''')

        # Применение изменений к базе данных
        self.connection.commit()

    def get_active_promocodes(self):
        query = "SELECT * FROM promo_exists WHERE activate_enable = '1'"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def user_exists(self, user_id):
        query = "SELECT * FROM users WHERE user_id = %s"
        self.cursor.execute(query, (user_id,))
        result = self.cursor.fetchall()
        return bool(len(result))
    
    def promocode_exists(self, promocode_id):
        query = "SELECT * FROM promo_exists WHERE promo_code = %s"
        self.cursor.execute(query, (promocode_id,))
        result = self.cursor.fetchall()
        return bool(len(result))
    
    def get_promocode(self, promocode_id):
        query = "SELECT * FROM promo_exists WHERE promo_code = %s"
        self.cursor.execute(query, (promocode_id,))
        result = self.cursor.fetchall()
        return result[0]
    
    def activate_enable(self, promocode_id):
        query = "SELECT * FROM promo_exists WHERE promo_code = %s"
        self.cursor.execute(query, (promocode_id,))
        result = self.cursor.fetchall()
        return result[0][7]
    
    def user_activates(self, user_id, promocode_id):
        query = "SELECT * FROM users WHERE user_id = %s AND promocode = %s"
        self.cursor.execute(query, (user_id, promocode_id))
        result = self.cursor.fetchall()
        return bool(result)  

    def add_active_promocode(self, user_id, username, promocode_id):
        query = "INSERT INTO users (user_id, username, promocode) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (user_id, username, promocode_id))
        self.connection.commit()

    def add_promocode(self, promocode_id, balance, coins, count, description):
        query = "INSERT INTO promo_exists (promo_code, promocode_bal, promocode_coins, promocode_count, promocode_desc, promocode_active) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(query, (promocode_id, balance, coins, count, description, '0'))
        self.connection.commit()

    def deactivate_promocode(self, promocode_id):
        query = "UPDATE promo_exists SET activate_enable = 'False' WHERE promo_code = %s"
        self.cursor.execute(query, (promocode_id,))
        self.connection.commit()

    def promo_active_count_add(self, promocode_id):
        query = "UPDATE promo_exists SET promocode_active = promocode_active + 1 WHERE promo_code = %s"
        self.cursor.execute(query, (promocode_id,))
        self.connection.commit()
    
    def deactivate_promocode_if_count(self, promocode_id):
        query = "SELECT * FROM promo_exists WHERE promo_code = %s"
        self.cursor.execute(query, (promocode_id,))
        result = self.cursor.fetchall()
        if result[0][6] >= result[0][3]:
            query = "UPDATE promo_exists SET activate_enable = 'False' WHERE promo_code = %s"
            self.cursor.execute(query, (promocode_id,))
            self.connection.commit()

    def get_all_promocodes(self):
        self.cursor.execute("SELECT * FROM promo_exists WHERE activate_enable = '1'")
        promocodes = self.cursor.fetchall()
        return promocodes

    def __del__(self):
        self.connection.close()

class SQLiteDatabase:
    def __init__(self):
        self.connection = sqlite3.connect(SQLITE3_CONNECT)
        self.cursor = self.connection.cursor()
        self.create_table()
        
    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS promo_exists (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                promo_code       TEXT    NOT NULL,
                promocode_bal    TEXT    NOT NULL,
                promocode_count  TEXT    NOT NULL,
                promocode_coin   TEXT,
                promocode_desc   TEXT,
                promocode_active TEXT    NOT NULL,
                activate_enable  TEXT    DEFAULT 'True' 
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id   TEXT    NOT NULL,
                username  TEXT    NOT NULL,
                promocode TEXT    NOT NULL
            )
        ''')

        self.connection.commit()

    def get_active_promocodes(self):
        query = "SELECT * FROM promo_exists WHERE activate_enable = '1'"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def user_exists(self, user_id):
        query = "SELECT * FROM users WHERE user_id = ?"
        self.cursor.execute(query, (user_id,))
        result = self.cursor.fetchall()
        return bool(len(result))
    
    def promocode_exists(self, promocode_id):
        query = "SELECT * FROM promo_exists WHERE promo_code = ?"
        self.cursor.execute(query, (promocode_id,))
        result = self.cursor.fetchall()
        return bool(len(result))
    
    def get_promocode(self, promocode_id):
        query = "SELECT * FROM promo_exists WHERE promo_code = ?"
        self.cursor.execute(query, (promocode_id,))
        result = self.cursor.fetchall()
        return result[0]
    
    def activate_enable(self, promocode_id):
        query = "SELECT * FROM promo_exists WHERE promo_code = ?"
        self.cursor.execute(query, (promocode_id,))
        result = self.cursor.fetchall()
        return result[0][7]
    
    def user_activates(self, user_id, promocode_id):
        query = "SELECT * FROM users WHERE user_id = ? AND promocode = ?"
        self.cursor.execute(query, (user_id, promocode_id))
        result = self.cursor.fetchall()
        return bool(len(result))
    
    def add_active_promocode(self, user_id, username, promocode_id):
        query = "INSERT INTO users (user_id, username, promocode) VALUES (?, ?, ?)"
        self.cursor.execute(query, (user_id, username, promocode_id))
        self.connection.commit()

    def add_promocode(self, promocode_id, balance, coins, count, description):
        query = "INSERT INTO promo_exists (promo_code, promocode_bal, promocode_coins, promocode_count, promocode_desc, promocode_active) VALUES (?, ?, ?, ?, ?, ?)"
        self.cursor.execute(query, (promocode_id, balance, coins, count, description, '0'))
        self.connection.commit()

    def deactivate_promocode(self, promocode_id):
        query = "UPDATE promo_exists SET activate_enable = 'False' WHERE promo_code = ?"
        self.cursor.execute(query, (promocode_id,))
        self.connection.commit()

    def promo_active_count_add(self, promocode_id):
        query = "UPDATE promo_exists SET promocode_active = promocode_active + 1 WHERE promo_code = ?"
        self.cursor.execute(query, (promocode_id,))
        self.connection.commit()

    def deactivate_promocode_if_count(self, promocode_id):
        query = "SELECT * FROM promo_exists WHERE promo_code = ?"
        self.cursor.execute(query, (promocode_id,))
        result = self.cursor.fetchall()
        if result[0][6] >= result[0][3]:
            query = "UPDATE promo_exists SET activate_enable = 'False' WHERE promo_code = ?"
            self.cursor.execute(query, (promocode_id,))
            self.connection.commit()

    def get_all_promocodes(self):
        self.cursor.execute("SELECT * FROM promo_exists WHERE activate_enable = '1'")
        promocodes = self.cursor.fetchall()
        return promocodes

    def __del__(self):
        self.connection.close()



if DATABASE_TYPE == 'mysql':
    db = MySQLDatabase()
elif DATABASE_TYPE == 'sqlite3':
    db = SQLiteDatabase()
else:
    pass
