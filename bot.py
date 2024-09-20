import telebot
from telebot import types
import json
from DB import DatabaseManager as DB
import ui
import scripts as scr
import threading, multiprocessing
import time as t


with open("token.json", "r", encoding = "UTF-8") as file:

    token = json.load(file)["botToken"]


start_time = None

bot = telebot.TeleBot(token)

DateBaseUsers = DB("chat.db")


@bot.message_handler(commands=["start"])
def greeting(message):

    scr.registerAction(DateBaseUsers, message.from_user.id, message.date)
    if DateBaseUsers.select("users", "user_id", message.from_user.id, "user_id"):
        info = DateBaseUsers.select("users", "user_id", message.from_user.id, "user_name", "country", "sex")[0]
        ui.startSerch(bot, types, message, f"Приветсвую вас - {info[0]}! \nВы проживаете в городе: {info[1]}, \nВаш пол: {info[2]}. \nХотите начать?")

    else:
        bot.send_message(message.chat.id, "Добавим json формат") #!!!Отредактировать файл json для вывода текста!
        ui.sexButtons(bot, types, message)
        DateBaseUsers.insert("users", "user_chat_id", message.chat.id)
        DateBaseUsers.update("users", "user_id", message.from_user.id, "user_chat_id", message.chat.id)
    

@bot.callback_query_handler(func = lambda callback: (callback.data == "man") or (callback.data == "women"))
def  handlerMan(callback):

    scr.registerAction(DateBaseUsers, callback.from_user.id, callback.message.date)
    bot.delete_message(callback.message.chat.id, callback.message.id)
    bot.send_message(callback.message.chat.id, f"Записал вас как {callback.data}. \nВведите свой псевдоним") #Добавить жирный тект на месте дата + Большие буквы
    if callback.data == "man":
        DateBaseUsers.update("users", "sex", "мальчик", "user_id", callback.from_user.id)
    else:
        DateBaseUsers.update("users", "sex", "девочка", "user_id", callback.from_user.id)
    bot.register_next_step_handler(callback.message, stepName)


def stepName(message):

    scr.registerAction(DateBaseUsers, message.from_user.id, message.date)
    DateBaseUsers.update("users", "user_name", message.text, "user_id", message.from_user.id)
    bot.register_next_step_handler(message, stepCountry)
    bot.send_message(message.chat.id, "Введите название своего города или город в область которого входит ваш населенный пункт")
    

def stepCountry(message):

    scr.registerAction(DateBaseUsers, message.from_user.id, message.date)
    DateBaseUsers.update("users", "country", message.text, "user_id", message.from_user.id)
    info = DateBaseUsers.select("users", "user_id", message.from_user.id, "user_name", "country", "sex")[0]
    ui.startSerch(bot, types, message, f"Поздравляю, вы зарегистрировались как: {info[0]}, \nПроживаете в городе: {info[1]}, \nВаш пол: {info[2]}. \nХотите начать?")
    

@bot.callback_query_handler(func = lambda callback: callback.data == "startSerch")
def  answerYes(callback):

    scr.registerAction(DateBaseUsers, callback.from_user.id, callback.message.date)
    info = DateBaseUsers.select("users", "user_id", callback.from_user.id, "country")[0]
    bot.send_message(callback.message.chat.id, f"И так, начинаю поиск по городу {info[0]}")


@bot.callback_query_handler(func = lambda callback: callback.data == "rename")
def  renameUsers(callback):
    
    scr.registerAction(DateBaseUsers, callback.from_user.id, callback.message.date)
    ui.sexButtons(bot, types, callback.message)


thr1 = threading.Thread(target = scr.udateColumnDiferent, args = (DateBaseUsers,)).start()



bot.polling()

