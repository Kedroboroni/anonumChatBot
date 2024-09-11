def sexButtons(bot, types, message):
    """Размещение кнопок выбора пола"""
    markup = types.InlineKeyboardMarkup()
    sexButtonM = types.InlineKeyboardButton('мальчик', callback_data = "man")
    sexButtonW = types.InlineKeyboardButton('девченка', callback_data = "women")
    markup.add(sexButtonM, sexButtonW)
    bot.send_message(message.chat.id, "Выберите ваш пол", reply_markup = markup)#Если работаем с callback, то указываем callback.message


def startSerch(bot, types, message, textToButon):

    """Размещение кнпок начала, вывода информации и ренейма.
        Используется при Приветсвии сущесвтующего польщователя
        Используется в Конце регистрации
        А так же в процессе работы с пользователем (но не факт)"""

    markup2 = types.InlineKeyboardMarkup()
    startButton = types.InlineKeyboardButton('Начать поиск', callback_data = "startSerch")
    infoAbotUserButton = types.InlineKeyboardButton('Информация о себе', callback_data = "infoAboutUser")
    infoAboutAllUsersButton =  types.InlineKeyboardButton('Информация о людях в сети', callback_data = "infoAboutAllUsers")
    renameButton = types.InlineKeyboardButton('Изменить данные о себе', callback_data = "rename")
    markup2.row(startButton)
    markup2.row(infoAbotUserButton, infoAboutAllUsersButton)
    markup2.row(renameButton)
    bot.send_message(message.chat.id, textToButon, reply_markup = markup2)
        
