import telebot
from telebot import types
import json


with open("tokenbot.json", "r", encoding = "UTF-8") as file:

    token = json.load(file)["botToken"]



bot = telebot.TeleBot(token)


@bot.message_handler(commands=["start"])
def greeting(message):


    bot.send_message(message.chat.id, "Добавим json формат") #!!!Отредактировать файл json для вывода текста!
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    sexButtonM = types.KeyboardButton('мальчик')
    sexButtonW = types.KeyboardButton('девченка')
    markup.add(sexButtonM, sexButtonW)
    bot.send_message(message.chat.id, "Выберите опцию в меню.", reply_markup=markup)
    bot.register_next_step_handler(message, handle_option_choice)
#Добавить проверку для того регистрировался данны человек или нет. через БД, что бы при попвторном вызове функции старт он не выбирал пол, но мог перерегистроваться


def handle_option_choice(message):

    if message.text in ['мальчик', 'девченка']:

        # Обработка выбора опции
        bot.send_message(message.chat.id, f"Вы выбрали: {message.text}, сохраняю ваш выбор в совбю БД", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, nextStepForRegister)
        
    else:

        # Повторное предложение опций
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        sexButtonM = types.KeyboardButton('мальчик')
        sexButtonW = types.KeyboardButton('девченка')
        markup.add(sexButtonM, sexButtonW)
        bot.send_message(message.chat.id, "Выберите опцию в меню.", reply_markup=markup)
        bot.register_next_step_handler(message, handle_option_choice)

def  nextStepForRegister(message):

    markup = types.InlineKeyboardMarkup()



bot.polling()