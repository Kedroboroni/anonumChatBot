def sexButtons(bot, types, message, textBeforeChoice):

    markup = types.InlineKeyboardMarkup()
    sexButtonM = types.InlineKeyboardButton('мальчик', callback_data = "man")
    sexButtonW = types.InlineKeyboardButton('девченка', callback_data = "women")
    markup.add(sexButtonM, sexButtonW)
    bot.send_message(message.chat.id, "Выберите ваш пол", reply_markup=markup)#Если работаем с callback, то указываем callback.message
