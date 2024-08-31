import sqlite3 as sq


def createMainTable():

    with sq.connect("chat.db") as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users (

                    user_chat_id INTEGER NOT NULL PRIMARY KEY,
                    user_id INTEGER NOT NULL,   
                    user_name TEXT,
                    country TEXT,
                    sex INTEGER 

                        )""")
        

def createCountreTable():

    with sq.connect("chat.db") as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS country (

                    country TEXT,
                    distance__from_Moscow INTEGER

                        )""")


def createStatusTable(): 

    with sq.connect("chat.db") as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS status (

                    user_chat_id INTEGER NOT NULL PRIMARY KEY,
                    status INEGER,
                    time TEXT,
                    date TEXT

                        )""")