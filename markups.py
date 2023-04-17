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
    item4 = types.KeyboardButton("Сменить роль")
    markup.add(item1, item2, item3, item4)

    return markup


def PlayerMarkup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Дайсы кинь!")
    item2 = types.KeyboardButton("Листы персонажей")
    item3 = types.KeyboardButton("Найти бестию")
    item4 = types.KeyboardButton("Сменить роль")
    markup.add(item1, item2, item3, item4)

    return markup
