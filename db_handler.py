from sqlite3 import connect

class DataBase():
    def __init__(self, connection):
        self.__conn = connect(connection)

    @property
    def connection(self):
        return self.__conn

    def create_tables(self):
        c = self.__conn.cursor()
        try:
            c.execute("""CREATE TABLE IF NOT EXISTS user(
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        username TEXT UNIQUE,
                        password TEXT
                        )""")
            c.execute("""CREATE TABLE IF NOT EXISTS collection(
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        place TEXT,
                        password TEXT,
                        user_id INTEGER REFERENCES user(id)
                        )""")
        except Exception as e:
            print(e)

    def insert_into_user(self, values):
        c = self.__conn.cursor()
        c.execute("""INSERT INTO user(username, password) VALUES (?,?)""", values)
        self.__conn.commit()

    def insert_into_collection(self, values, user_id):
        c = self.__conn.cursor()
        c.execute("""INSERT INTO collection(place, password, user_id) VALUES (?,?,?)""", values + (user_id, ))
        self.__conn.commit()

    def select_user(self, values):
        c = self.__conn.cursor()
        c.execute("""SELECT * FROM user WHERE username=? and password=?""", values)
        user_from_db = c.fetchone()
        return user_from_db

    def select_password(self, user_id):
        c = self.__conn.cursor()
        c.execute("""SELECT * FROM collection WHERE user_id=?""", (user_id, ))
        passwords_from_db = c.fetchall()
        return passwords_from_db

    def delete_password(self, values, user_id):
        c = self.__conn.cursor()
        c.execute("""DELETE FROM collection WHERE place=? AND password=? AND user_id=?""", values + (user_id, ))
        self.__conn.commit()

    def update_password(self, values, password_id):
        c = self.__conn.cursor()
        c.execute("""UPDATE collection SET place=? AND password=? WHERE id=?""", values + (password_id, ))
        self.__conn.commit()