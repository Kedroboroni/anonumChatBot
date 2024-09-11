import time
import datetime


def registerAction(DateBaseUsers, userID, unixTimeAction):

    date =  datetime.datetime.utcfromtimestamp(int(unixTimeAction)).date()
    time = datetime.datetime.utcfromtimestamp(int(unixTimeAction)).time()

    DateBaseUsers.insert("status", "user_id", userID)
    DateBaseUsers.update("status", "time", time, "user_id", userID)
    DateBaseUsers.update("status", "date", date, "user_id", userID)
    DateBaseUsers.update("status", "date", date, "user_id", userID)#Не круто обращаться к БД несмколько , лучше делать все за один раз. исравить в DB.py!!!!
    DateBaseUsers.update("status", "status", "online", "user_id", userID)


def udateColumnDiferent(DateBaseUsers, userID, timeUnixLastAction):
    """Обнавляем разницу времени между последним событием пользователя и настоящим временем в формате Юникс. Раз в 5 минут.
        Эта функция должна находиться в асинхронном методе. Посомтерть как работают асинхронные системы. (для отслеживания 5 минут неактивности пользователя
        и не мешанию ему взаимодействовать с ботом)"""
    diff = int(time.time()) - int(timeUnixLastAction)
    DateBaseUsers.update("status", "diferent_time_UNIX", diff, "status", "online") #Изменили столбец разницы времнеи ЮНИКС (посл.акт. - наст время) у всех у кого статут online
    

def calculateOfflineUsers(DateBaseUsers):
     
    #diff = int(time.time()) - int(unixTimeLastAction)
    results = DateBaseUsers.select("status", "diferent_time_UNIX", 300, "user_id")#По иджеи должен вернуть список, проверить как буелт время, пользователей, у которых время активности меньше 300 сек.
    for i in results:
        DateBaseUsers.update("status", "status", "offline", "user_id", results)# Обновили пользователей, которые не были активны в течении 5 минут
