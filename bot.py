import telebot
from telebot import types
import json
from DB import DatabaseManager as DB
import ui


with open("tokenbot.json", "r", encoding = "UTF-8") as file:

    token = json.load(file)["botToken"]



bot = telebot.TeleBot(token)

DateBaseUsers = DB("chat.db")



@bot.message_handler(commands=["start"])
def greeting(message):

    #!!!!Необходимо добавить проверки от долбоебов, чтобы в имена и города не записывались команды, а так же чтобы пользователь мог вводить в начлае, только то, что от него требуется
    if DateBaseUsers.select("users", "user_id", message.from_user.id, "user_id"):
        info = DateBaseUsers.select("users", "user_id", message.from_user.id, "user_name", "country", "sex")[0]
        ui.startSerch(bot, types, message, f"Приветсвую вас - {info[0]}! \nВы проживаете в городе: {info[1]}, \nВаш пол: {info[2]}. \nХотите начать?")
        #№bot.send_message(message.chat.id, ) #Если существует польсователь
        bot.register_next_step_handler(message, repeatStart)

    else:
        bot.send_message(message.chat.id, "Добавим json формат") #!!!Отредактировать файл json для вывода текста!    bot.register_next_step_handler(message, replayActionSex)
        ui.sexButtons(bot, types, message)
        DateBaseUsers.insert("users", "user_chat_id", message.chat.id)
        DateBaseUsers.update("users", "user_id", message.from_user.id, "user_chat_id", message.chat.id)
        #Добавить проверку для того регистрировался данны человек или нет. через БД, что бы при попвторном вызове функции старт он не выбирал пол, но мог перерегистроваться

def repeatStart(message):
    ui.startSerch(bot, types, message, f"Извните, но сейчас вам нужно выбрать действие")
    #bot.send_message(message.chat.id, "Извните, но сейчас вам нужно выбрать действие")

def repeatActionSex(message):
    if DateBaseUsers.select("users", "user_id", message.from_user.id, "sex"):
        #bot.register_next_step_handler(message, replayActionSex)
        bot.send_message(message.chat.id, "Для посика новых знакомств, вам необходимо указать свой пол, пожалуйста сделайет это")
        ui.sexButtons(bot, types, message)
        
    else: 
        return True
    


@bot.callback_query_handler(func = lambda callback: (callback.data == "man") or (callback.data == "women"))
def  handlerMan(callback):

    bot.send_message(callback.message.chat.id, f"Записал вас как {callback.data}") #Добавить жирный тект на месте дата + Большие буквы
    if callback.data == "man":
        DateBaseUsers.update("users", "sex", 1, "user_id", callback.from_user.id)
    else:
        DateBaseUsers.update("users", "sex", 0, "user_id", callback.from_user.id)
    bot.register_next_step_handler(callback.message, stepName)
    bot.send_message(callback.message.chat.id, "Введите свой псевдоним")


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
    bot.register_next_step_handler(callback.message, stepName)
    bot.register_next_step_handler(callback.message, repeatActionSex)





bot.polling()