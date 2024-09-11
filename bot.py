import telebot
from telebot import types
import json
from DB import DatabaseManager as DB
import ui


with open("parametrs.json", "r", encoding = "UTF-8") as file:

    token = json.load(file)["botToken"]



bot = telebot.TeleBot(token)

DateBaseUsers = DB("chat.db")


@bot.message_handler(commands=["start"])
def greeting(message):

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

    bot.send_message(callback.message.chat.id, f"Записал вас как {callback.data}. \nВведите свой псевдоним") #Добавить жирный тект на месте дата + Большие буквы
    if callback.data == "man":
        DateBaseUsers.update("users", "sex", "мальчик", "user_id", callback.from_user.id)
    else:
        DateBaseUsers.update("users", "sex", "девочка", "user_id", callback.from_user.id)
    bot.register_next_step_handler(callback.message, stepName)
    #bot.send_message(callback.message.chat.id, "Введите свой псевдоним")


def stepName(message):

    DateBaseUsers.update("users", "user_name", message.text, "user_id", message.from_user.id)
    bot.register_next_step_handler(message, stepCountry)
    bot.send_message(message.chat.id, "Введите название своего города или город в область которого входит ваш населенный пункт")
    

def stepCountry(message):

    DateBaseUsers.update("users", "country", message.text, "user_id", message.from_user.id)
    info = DateBaseUsers.select("users", "user_id", message.from_user.id, "user_name", "country", "sex")[0]
    ui.startSerch(bot, types, message, f"Поздравляю, вы зарегистрировались как: {info[0]}, \nПроживаете в городе: {info[1]}, \nВаш пол: {info[2]}. \nХотите начать?")
    

@bot.callback_query_handler(func = lambda callback: callback.data == "startSerch")
def  answerYes(callback):

    info = DateBaseUsers.select("users", "user_id", callback.from_user.id, "country")[0]
    bot.send_message(callback.message.chat.id, f"И так, начинаю поиск по городу {info[0]}")


@bot.callback_query_handler(func = lambda callback: callback.data == "rename")
def  renameUsers(callback):

    ui.sexButtons(bot, types, callback.message)


@bot.message_handler(content_types = ["text", "foto", "video",
                                       "audio", "document", "sticker",
                                        "contact", "location", "inline_query",
                                        "callback_query"
                                        ])
def updateStatus(message):
        print("Зарегестрировано действие пользователя")





bot.polling()