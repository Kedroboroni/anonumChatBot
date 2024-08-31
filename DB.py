import sqlite3 as sq



class DB:

    def __init__(self):
        
        with sq.connect("chat.db") as self.con:
            self.cursor = self.con.cursor()

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (

                    user_chat_id INTEGER NOT NULL PRIMARY KEY,
                    user_id INTEGER NOT NULL,   
                    user_name TEXT,
                    country TEXT,
                    sex INTEGER 

                        )""")
        
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS country (

                    country TEXT,
                    distance__from_Moscow INTEGER

                        )""")
        
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS status (

                    user_chat_id INTEGER NOT NULL PRIMARY KEY,
                    status INEGER,
                    time TEXT,
                    date TEXT

                        )""")


    def insert(self, table, column, values):
        
        self.cursor.execute(""" INSERT INTO (?) (?)
                        VALUES (?)
                        """,
                        (table,column, values))
        print("Запись произведена успешно")
        self.con.commit()


    def update(self, table, column, values):

        self.cursor.execute(""" UPDATE (?) SET (?) = (?)""",
                    (table, column, values))
        print("Изменения записаны успешно")
        self.con.commit()