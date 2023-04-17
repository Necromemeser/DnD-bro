from telebot import types


def mainMarkup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("♂ Dungeon Master ♂")
    item2 = types.KeyboardButton("⚔ Игрок ⚔")
    item3 = types.KeyboardButton("Я здесь за мемами!")

    markup.add(item1, item2, item3)
    return markup


def DMMarkup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Дайсы кинь!")
    item2 = types.KeyboardButton("Случайное Имя")
    item3 = types.KeyboardButton("Случайный Город")
    item4 = types.KeyboardButton("Найти бестию")
    item5 = types.KeyboardButton("Сменить роль")
    markup.add(item1, item2, item3, item4, item5)

    return markup


def PlayerMarkup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Дайсы кинь!")
    item2 = types.KeyboardButton("Листы персонажей")
    item3 = types.KeyboardButton("Сменить роль")
    markup.add(item1, item2, item3)

    return markup


def diceMarkup():
    markup = types.InlineKeyboardMarkup(row_width=3)
    d4 = types.InlineKeyboardButton("4", callback_data='d.4')
    d6 = types.InlineKeyboardButton("6", callback_data='d.6')
    d8 = types.InlineKeyboardButton("8", callback_data='d.8')
    d10 = types.InlineKeyboardButton("10", callback_data='d.10')
    d12 = types.InlineKeyboardButton("12", callback_data='d.12')
    d20 = types.InlineKeyboardButton("20", callback_data='d.20')
    markup.add(d4, d6, d8, d10, d12, d20)

    return markup
