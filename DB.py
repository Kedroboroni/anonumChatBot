import sqlite3
from queue import Queue
from threading import Thread

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.queue = Queue()
        self.threadDB = Thread(target=self.processQueue)
        self.threadDB.start()


    def processQueue(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                    user_chat_id INTEGER NOT NULL PRIMARY KEY,
                    user_id INTEGER ,   
                    user_name TEXT,
                    country TEXT,
                    sex INTEGER 
                        )""")
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS country (
                    country TEXT,
                    distance__from_Moscow INTEGER
                        )""")
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS status (
                    user_chat_id INTEGER NOT NULL PRIMARY KEY,
                    status INEGER,
                    time TEXT,
                    date TEXT
                        )""")
        
        while True:
            item = self.queue.get()
            if item is None:
                break
            
            
            query, params = item
            cursor.execute(query, params)
            conn.commit()         
            self.queue.task_done()
        
        conn.close()

    def execute(self, query, params=()):
        self.queue.put((query, params))
        self.queue.join()  # Ожидаем выполнения запроса


    def insert(self, table, column, values):
        self.execute(f"""INSERT INTO {table} ({column}) VALUES ({values})""") #Тут возможна sql инъекция, но избавляться от этого я не буд, потому что проект начальный. Чтобы избавыитьься от sql инъекции можно изспользовать ORM alchemi


    def update(self, table, column, values, columnChoice, userID):
        self.execute(f""" UPDATE [{table}] SET {column} = {values} WHERE {columnChoice} = {userID}""") #Проблема тут, нкжно уточнить, как правлиьно сделать это зпрос.


    def close(self):
        self.queue.put(None)  # Сигнал завершения работы
        self.worker_thread.join()


