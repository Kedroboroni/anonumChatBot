import sqlite3 as sq


def createMainTable():

    with sq.connect("chat.db") as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users (

                    user_chat_id INTEGER NOT NULL PRIMARY KEY,   
                    user TEXT,
                    country TEXT,
                    sex INTEGER 

                        )""")