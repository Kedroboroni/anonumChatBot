import sqlite3 as sq




with sq.connect("chat.db") as con:
        cur = con.cursor()