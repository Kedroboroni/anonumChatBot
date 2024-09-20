import time as t
import datetime
import numpy as np



def registerAction(DateBaseUsers, userID, timeUnixAction):

    diferentTime = t.time() - timeUnixAction

    date =  str(datetime.datetime.utcfromtimestamp(int(timeUnixAction)).date())#!!!Далее сделать так, чтобы в БД записывалась дата в формеате даты, а не строки!!!
    time = str(datetime.datetime.utcfromtimestamp(int(timeUnixAction)).time())#!!!Далее сделать так, чтобы в БД записывалась время в формеате времени, а не строки!!!

    DateBaseUsers.insert("status", "user_id", userID)
    DateBaseUsers.update("status", "time", time, "user_id", userID)
    DateBaseUsers.update("status", "date", date, "user_id", userID)
    DateBaseUsers.update("status", "time_UNIX_Action", timeUnixAction, "user_id", userID)#Не круто обращаться к БД несмколько , лучше делать все за один раз. исравить в DB.py!!!!
    DateBaseUsers.update("status", "position", "online", "user_id", userID)
    

def udateColumnDiferent(DateBaseUsers):
    
    while True:
        print("Обновили БД")
        #2. Из всех у кого online и diferent time > 5 минут, меняем статус на offline.
            #2.1 выбирае из всех у кого online и diferent_time > 5 значения колонок id_user
            #2.2 заменяем статус все id_user из нашей таблицы на oflines
        nowUnix = int(t.time())
        result = np.array(DateBaseUsers.select("status", "position", "online", "user_id", "time_UNIX_Action"))
        if result.size > 0:
            print(f"выиграл {result}")
            result[:,1] = nowUnix - result[:,1]
            for obj in result:
                print(obj[0], "    ",obj[1])
                DateBaseUsers.update("status", "diferent_time_UNIX", int(obj[1]), "user_id", int(obj[0]))
        DateBaseUsers.updateMORE("status", "position", "ofline", "user_id", 10)
        t.sleep(5)
   

def calculateOfflineUsers(DateBaseUsers, timeUnixAction):
    
    while True:
        users = DateBaseUsers.select("status", "position", "online", "user_id", "time_UNIX_Action")
        diferentTime = t.time() - timeUnixAction #!!! Нельзя так там [инт] - [кортеж]
        DateBaseUsers.update("status", "diferent_time_UNIX", diferentTime, "status", "online")
        DateBaseUsers.updateMORE("status", "position", "offline", "diferent_time_UNIX", 300)# Обновили пользователей, которые не были активны в течении 5 минут
        print("Обнавили БД")
        t.sleep(5)


def trackTime(DateBaseUsers):

    while True:
        print("Обновили БД")
        #2. Из всех у кого online и diferent time > 5 минут, меняем статус на offline.
            #2.1 выбирае из всех у кого online и diferent_time > 5 значения колонок id_user
            #2.2 заменяем статус все id_user из нашей таблицы на oflines

        nowUnix = int(t.time())
        result = np.array(DateBaseUsers.select("status", "position", "online", "user_id", "time_UNIX_Action"))
        result[:,1] = nowUnix - result[:,1]
        for user_id, diferentTime in result:
            first = t.time()
            DateBaseUsers.update("status", "diferent_time_UNIX", diferentTime, "user_id", user_id)
            second = t.time()
            print(f"Время на изменнеие БД составило: {second-first}")
        t.sleep(5)
   



    