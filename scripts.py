import time
import datetime


def registerAction(DateBaseUsers, userID, unixTime):

    date =  datetime.datetime.utcfromtimestamp(int(unixTime)).date()
    time = datetime.datetime.utcfromtimestamp(int(unixTime)).time()

    DateBaseUsers.insert("status", "time", time)