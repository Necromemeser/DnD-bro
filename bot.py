import telebot
import random
import playerMode

from telebot import types
from dotenv import load_dotenv

import config

path = "F:/DnD-bro-token/token.env"
load_dotenv(dotenv_path=path)

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    """
    Функция отвечает на комманду start

    Отправляет приветственные сообщения
    И создает клавиатуру
    """

    bot.send_video(message.chat.id, 'https://tenor.com/ru/view/pepe-pepe-the-frog-wizard-gif-7939266', None, '')
    # Создание клавиатуры
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("♂ Dungeon Master ♂")
    item2 = types.KeyboardButton("⚔ Игрок ⚔")

    markup.add(item1, item2)

    bot.send_message(message.chat.id,
                     "Будь как дома, {0.first_name}!\nЯ ни в чем не откажу...\n\n"
                     "Мои создатели сделали меня с одной целью - облегчить твою фентезийную жизнь\n(надеюсь, можно ведь сразу на ты?)\n\n"
                     "С помощью меня ты можешь:\n\n"
                     "🎲 <b>Роллить дайсы</b> (единственные слова на эльфийском, что я знаю);\n\n"
                     "📝 <b>Ввести учет своих других, более интересных жизней</b>;\n\n"
                     "🧑 <b>Спихнуть ответственность за названия людей и имена городов на бездушный инструмент</b> (эт я, да :3);\n\n"
                     "👉👈 <b>Получить дозу хорошего настроения между партиями</b>;\n\n"
                     "И многое другое! - сказал бы я, было бы что-то еще...\n"
                     "В общем, помогу, чем смогу.\n\n"
                     "<b>Но для начала ответь:\n"
                     "ты ♂ Dungeon Master ♂ или ⚔ Игрок ⚔?</b>".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def role_choice_handler(message):
    """
    Функция отвечает на сообщения пользователя

    Варианты сообщений и ответов на них:
    '♂ Dungeon Master ♂': переводит пользователя в режим ДМ-а;
    '⚔ Игрок ⚔': переводит пользователя в режим игрока;
    'Сменить роль': переводит пользователя в противоположный режим;
    'Дайсы кинь!': выводит случайное число, имитируя бросок дайса;
    'Листы персонажей': работа с листами персонажей (Режим игрока [*Хотя можно было бы впихнуть и в режим ДМ-а, не так ведь сложно...*])
    'Доза': выводит тематический мем
    'Случайное Имя': выводит случайное имя для НПС (Режим ДМ-а)
    'Случайный Город': выводит случайное название для города (Режим ДМ-а)
    """
    if message.chat.type == 'private':
        if message.text == '♂ Dungeon Master ♂':  # Переход в режим ДМ-а
            markup = types.ReplyKeyboardRemove(selective=False)
            bot.send_message(message.chat.id, "Сразу видно - человек серьезный.", reply_markup=markup)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Дайсы кинь!")
            item2 = types.KeyboardButton("Случайное Имя")
            item3 = types.KeyboardButton("Случайный Город")
            item4 = types.KeyboardButton("Доза")
            item5 = types.KeyboardButton("Сменить роль")
            markup.add(item1, item2, item3, item4, item5)

            bot.send_message(message.chat.id, "Чего желаете?", reply_markup=markup)

        elif message.text == '⚔ Игрок ⚔':  # Переход в режим игрока
            markup = types.ReplyKeyboardRemove(selective=False)
            bot.send_message(message.chat.id, "Хорошей игры!", reply_markup=markup)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Дайсы кинь!")
            item2 = types.KeyboardButton("Листы персонажей")
            item3 = types.KeyboardButton("Доза")
            item4 = types.KeyboardButton("Сменить роль")
            markup.add(item1, item2, item3, item4)

            bot.send_message(message.chat.id, "Чего желаете?", reply_markup=markup)

        elif message.text == 'Сменить роль':  # Замена роли на противоположную (Недоделано)
            bot.send_message(message.chat.id, "Прости, эта часть еще недоделана(")

        elif message.text == 'Листы персонажей':  # Работа с листами персонажей (Недоделано)
            markup = types.InlineKeyboardMarkup(row_width=2)
            create = types.InlineKeyboardButton("Создать персонажа", callback_data='cs.create')
            edit = types.InlineKeyboardButton("Редактировать лист", callback_data='cs.edit')

            markup.add(create, edit)

            bot.send_message(message.chat.id, "Выбери опцию", reply_markup=markup)

        elif message.text == 'Доза':  # Вывод тематического мема (Недоделано)
            bot.send_message(message.chat.id, "Прости, эта часть еще недоделана(")

        elif message.text == 'Случайное Имя':  # Вывод случайного имени для НПС (Недоделано)
            bot.send_message(message.chat.id, "Прости, эта часть еще недоделана(")

        elif message.text == 'Случайный Город':  # Вывод случайного названия города (Недоделано)
            bot.send_message(message.chat.id, "Прости, эта часть еще недоделана(")

        elif message.text == 'Дайсы кинь!':  # Бросок дайса
            markup = types.InlineKeyboardMarkup(row_width=3)
            d4 = types.InlineKeyboardButton("4", callback_data='d.4')
            d6 = types.InlineKeyboardButton("6", callback_data='d.6')
            d8 = types.InlineKeyboardButton("8", callback_data='d.8')
            d10 = types.InlineKeyboardButton("10", callback_data='d.10')
            d12 = types.InlineKeyboardButton("12", callback_data='d.12')
            d20 = types.InlineKeyboardButton("20", callback_data='d.20')

            markup.add(d4, d6, d8, d10, d12, d20)

            bot.send_message(message.chat.id, "Сколько нужно граней?", reply_markup=markup)

        else:
            bot.send_message(message.chat.id,
                             'Милсдарь {0.first_name}, извольте! Ничего не понял... Скажите еще раз, по-другому!')


@bot.callback_query_handler(func=lambda call: call.data.startswith('d.'))
def callback_inline(call):
    """
    Функция отвечает на вызовы

    Используется для имитации броска дайсов с различным количеством граней
    Отправляет сообщение со случайным числом и редактирует предыдущее сообщение
    """
    try:
        if call.message:
            if call.data == 'd.4':
                bot.send_message(call.message.chat.id, str(random.randint(1, 4)))
            elif call.data == 'd.6':
                bot.send_message(call.message.chat.id, str(random.randint(1, 6)))
            elif call.data == 'd.8':
                bot.send_message(call.message.chat.id, str(random.randint(1, 8)))
            elif call.data == 'd.10':
                bot.send_message(call.message.chat.id, str(random.randint(1, 10)))
            elif call.data == 'd.12':
                bot.send_message(call.message.chat.id, str(random.randint(1, 12)))
            elif call.data == 'd.20':
                bot.send_message(call.message.chat.id, str(random.randint(1, 20)))

            # Убираем строковые кнопки
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Вашу судьбу определит число:",
                                  reply_markup=None)

    except Exception as e:
        print(repr(e))


@bot.callback_query_handler(func=lambda call: call.data.startswith('cs.'))
def callback_inline(call):
    """
    Функция отвечает на вызовы при выборе инструмента "Листы персонажей"

    Используется для взаимодействия с меню
    Отправляет сообщения с дальнейшими инструкциями
    """

    try:
        if call.message:
            if call.data == 'cs.create':
                character = []

                def step1(msg):
                    character.append(msg)
                    msg = bot.send_message(call.message.chat.id, 'Какой у него класс?')
                    bot.register_next_step_handler(msg, step2(msg))

                def step2(msg):
                    character.append(msg)
                    msg = bot.send_message(call.message.chat.id, 'Какой у него класс?')
                    bot.register_next_step_handler(msg, step3(msg))

                def step3(msg):
                    character.append(msg)
                    msg = bot.send_message(call.message.chat.id, 'Какой у сейчас уровень?')
                    bot.register_next_step_handler(msg, step4(msg))

                def step4(msg):
                    character.append(msg)
                    msg = bot.send_message(call.message.chat.id, 'Какой у него показатель Силы?')
                    bot.register_next_step_handler(msg, step5(msg))

                def step5(msg):
                    character.append(msg)
                    msg = bot.send_message(call.message.chat.id, 'Какой у него показатель Ловкости?')
                    bot.register_next_step_handler(msg, step6(msg))

                def step6(msg):
                    character.append(msg)
                    msg = bot.send_message(call.message.chat.id, 'Какой у него показатель Выносливости?')
                    bot.register_next_step_handler(msg, step7(msg))

                def step7(msg):
                    character.append(msg)
                    msg = bot.send_message(call.message.chat.id, 'Какой у него показатель Интеллекта?')
                    bot.register_next_step_handler(msg, step8(msg))

                def step8(msg):
                    character.append(msg)
                    msg = bot.send_message(call.message.chat.id, 'Какой у него показатель Мудрости?')
                    bot.register_next_step_handler(msg, step9(msg))

                def step9(msg):
                    character.append(msg)
                    msg = bot.send_message(call.message.chat.id, 'Какой у него показатель Харизмы?')
                    bot.register_next_step_handler(msg, step10(msg))

                def step10(msg):
                    character.append(msg)
                    msg = bot.send_message(call.message.chat.id, 'Какой у него максимальный показатель здоровья?')
                    bot.register_next_step_handler(msg, step11(msg))

                def step11(msg):
                    character.append(msg)
                    msg = bot.send_message(call.message.chat.id, 'Какой у него класс брони?')
                    bot.register_next_step_handler(msg, step12(msg))
                    playerMode.createCharacter(character)
                    bot.send_message(call.chat.id, 'Ваш персонаж успешно создан!')

                def step12(msg):
                    character.append(msg)
                    playerMode.createCharacter(character)
                    bot.send_message(call.chat.id, 'Ваш персонаж успешно создан!')


                bot.send_message(call.message.chat.id,
                                 'Отлично! Приступим к созданию очередного героя!\n\n')
                msg = bot.send_message(call.message.chat.id, 'Как зовут персонажа?')
                bot.register_next_step_handler(msg, step1(msg))


            elif call.data == 'cs.edit':
                bot.send_message(call.message.chat.id,
                                 '')
    except Exception as e:
        print(repr(e))


# Запуск!
bot.polling(none_stop=True)
