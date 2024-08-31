import telebot
from telebot import types
import json


with open("tokenbot.json", "r", encoding = "UTF-8") as file:

    token = json.load(file)["botToken"]

informationAboutUser = []

bot = telebot.TeleBot(token)



@bot.message_handler(commands=["start"])
def greeting(message):

    bot.send_message(message.chat.id, "Добавим json формат") #!!!Отредактировать файл json для вывода текста!
    markup = types.InlineKeyboardMarkup()
    sexButtonM = types.InlineKeyboardButton('мальчик', callback_data = "man")
    sexButtonW = types.InlineKeyboardButton('девченка', callback_data = "women")
    markup.add(sexButtonM, sexButtonW)
    bot.send_message(message.chat.id, "Выберите ваш пол", reply_markup=markup)
    userID = message.from_user.id #Достали ид юзера при старте бота
    print(f" Ваш ид: {userID}")
    #bot.register_next_step_handler(message, handle_option_choice)
    #Добавить проверку для того регистрировался данны человек или нет. через БД, что бы при попвторном вызове функции старт он не выбирал пол, но мог перерегистроваться



@bot.callback_query_handler(func = lambda callback: (callback.data == "man") or (callback.data == "women"))
def  handlerMan(callback):
    global informationAboutUser

    bot.send_message(callback.message.chat.id, f"Записал вас как {callback.data}") #Добавить жирный тект на месте дата + Большие буквы
    #Добавить обновление БД
    informationAboutUser.append(callback.data)
    bot.register_next_step_handler(callback.message, stepName)
    bot.send_message(callback.message.chat.id, "Введите свой псевдоним")



def stepName(message):

    global informationAboutUser
    #bot.send_message(message.chat.id, "Введите свой псевдоним")
    #Добавить БД
    informationAboutUser.append(message.text)
    bot.register_next_step_handler(message, stepCountry)
    bot.send_message(message.chat.id, "Введите название своего города или город в область которого входит ваш населенный пункт")


def stepCountry(message):

    global informationAboutUser
    #bot.send_message(message.chat.id, "Введите название своего города или город в область которого входит ваш населенный пункт")
    #Добавить БД
    informationAboutUser.append(message.text)
    bot.send_message(message.chat.id, f"Поздравляю, вы зарегистрировались как: {informationAboutUser[1]}, \nПроживаете в городе: {informationAboutUser[2]}, \nВаш пол: {informationAboutUser[0]}")#Тут нужно доставть значения з БД, но пока ее нет имитируем ее списком
    informationAboutUser = []
    markAnswer = types.InlineKeyboardMarkup()
    yesButton = types.InlineKeyboardButton("Да", callback_data = "YES")
    noButton = types.InlineKeyboardButton("Нет", callback_data = "NO")
    markAnswer.add(yesButton, noButton)
    bot.send_message(message.chat.id, "Хотите начать поиск для анонимного общения?", reply_markup = markAnswer)



@bot.callback_query_handler(func = lambda callback: callback.data == "YES")
def  answerYes(callback):

    bot.send_message(callback.message.chat.id, "И так, начинаю поиск по городу {<ЕГО ГОРОД>}")





bot.polling()