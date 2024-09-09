import telebot
from telebot import types
import json
from DB import DatabaseManager as DB
import ui


with open("tokenbot.json", "r", encoding = "UTF-8") as file:

    token = json.load(file)["botToken"]



bot = telebot.TeleBot(token)
Types = types()

DateBaseUsers = DB("chat.db")



@bot.message_handler(commands=["start"])
def greeting(message):

    #!!!!Необходимо добавить проверки от долбоебов, чтобы в имена и города не записывались команды, а так же чтобы пользователь мог вводить в начлае, только то, что от него требуется
    if DateBaseUsers.select("users", "user_id", message.from_user.id, "user_id"):
        bot.send_message(message.chat.id, "Рады приветсвовать вас на этой грешной земле") #Если существует польсователь
        bot.register_next_step_handler(message, replayActionSex)

    else:
        bot.send_message(message.chat.id, "Добавим json формат") #!!!Отредактировать файл json для вывода текста!    bot.register_next_step_handler(message, replayActionSex)
        ui.sexButtons(bot, Types, message)
        #markup = types.InlineKeyboardMarkup()
        #sexButtonM = types.InlineKeyboardButton('мальчик', callback_data = "man")
        #sexButtonW = types.InlineKeyboardButton('девченка', callback_data = "women")
        #markup.add(sexButtonM, sexButtonW)
        #bot.send_message(message.chat.id, "Выберите ваш пол", reply_markup=markup)
        DateBaseUsers.insert("users", "user_chat_id", message.chat.id)
        DateBaseUsers.update("users", "user_id", message.from_user.id, "user_chat_id", message.chat.id)
        #Добавить проверку для того регистрировался данны человек или нет. через БД, что бы при попвторном вызове функции старт он не выбирал пол, но мог перерегистроваться


def replayActionSex(message):
    if DateBaseUsers.select("users", "user_id", message.from_user.id, "sex"):
        #bot.register_next_step_handler(message, replayActionSex)
        ui.sexButtons(bot, Types, message)
        #markup = types.InlineKeyboardMarkup()
        #sexButtonM = types.InlineKeyboardButton('мальчик', callback_data = "man")
        #sexButtonW = types.InlineKeyboardButton('девченка', callback_data = "women")
        #markup.add(sexButtonM, sexButtonW)
        bot.send_message(message.chat.id, "Для посика новых знакомств, вам необходимо указать свой пол, пожалуйста сделайет это", reply_markup=markup)
        
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
    bot.send_message(message.chat.id, f"Поздравляю, вы зарегистрировались как: {info[0]}, \nПроживаете в городе: {info[1]}, \nВаш пол: {info[2]}")#Тут нужно доставть значения з БД, но пока ее нет имитируем ее списком
    markAnswer = types.InlineKeyboardMarkup()
    yesButton = types.InlineKeyboardButton("Да", callback_data = "YES")
    noButton = types.InlineKeyboardButton("Нет", callback_data = "NO")
    renameButton = types.InlineKeyboardButton("Изменить данные о себе", callback_data = "rename")
    markAnswer.add(yesButton, noButton)
    bot.send_message(message.chat.id, "Хотите начать поиск для анонимного общения?", reply_markup = markAnswer)


@bot.callback_query_handler(func = lambda callback: callback.data == "YES")
def  answerYes(callback):

    info = DateBaseUsers.select("users", "user_id", callback.from_user.id, "country")[0]
    bot.send_message(callback.message.chat.id, f"И так, начинаю поиск по городу {info[0]}")


@bot.callback_query_handler(func = lambda callback: callback.data == "rename")
def  renameUsers(callback):

    markup = types.InlineKeyboardMarkup()
    sexButtonM = types.InlineKeyboardButton('мальчик', callback_data = "man")
    sexButtonW = types.InlineKeyboardButton('девченка', callback_data = "women")
    markup.add(sexButtonM, sexButtonW)
    bot.send_message(callback.message.chat.id, "Выберите ваш пол", reply_markup=markup)
    bot.send_message(callback.message.chat.id, "Введите свой псевдоним")
    bot.register_next_step_handler(callback.message.chat.id, stepName)





bot.polling()