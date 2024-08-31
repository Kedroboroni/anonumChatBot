import sqlite3 as sq


with sq.connect("chat.db") as con:
        cursor = con.cursor()



def createMainTable(cursor):
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (

                    user_chat_id INTEGER NOT NULL PRIMARY KEY,
                    user_id INTEGER NOT NULL,   
                    user_name TEXT,
                    country TEXT,
                    sex INTEGER 

                        )""")
    cursor.commit()
        

def createCountryTable(cursor):
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS country (

                    country TEXT,
                    distance__from_Moscow INTEGER

                        )""")
    cursor.commit()


def createStatusTable(cursor): 
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS status (

                    user_chat_id INTEGER NOT NULL PRIMARY KEY,
                    status INEGER,
                    time TEXT,
                    date TEXT

                        )""")
    cursor.commit()


def insert(cursor, table, column, values):

        cursor.execute(""" INSERT INTO (?) (?)
                        VALUES (?)
                        """,
                        (table,column, values))
        cursor.commit()


def update(cursor, table, column, values):

        cursor.execute(""" UPDATE (?) SET (?) = (?)""",
                    (table, column, values))
        cursor.commit()

