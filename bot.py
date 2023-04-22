import re
import telebot
import random
import playerMode
import memes
import config
from threading import Thread
import schedule
from time import sleep
from markups import types
import markups
import telebot
import random
import playerMode
import config
from telebot import types
from dotenv import load_dotenv

URL = 'https://ttg.club/bestiary/'


bot = telebot.TeleBot(config.TOKEN)
chat_id = 0



        
@bot.message_handler(commands=['start'])
def welcome(message):
    """
    Функция отвечает на комманду start

    Отправляет приветственные сообщения
    И создает клавиатуру

    Так же запускает поток, чтобы каждую среду отправлять
    культурно значимое изображение
    """

    global chat_id
    chat_id = message.chat.id

    bot.send_video(message.chat.id, 'https://tenor.com/ru/view/pepe-pepe-the-frog-wizard-gif-7939266', None, '')
    # Создание клавиатуры
    markup = markups.mainMarkup()

    bot.send_message(message.chat.id,
                     "Будь как дома, {0.first_name}!\nЯ ни в чем не откажу...\n\n"
                     "Мои создатели сделали меня с одной целью - облегчить твою фентезийную жизнь\n(надеюсь, можно ведь сразу на ты?)\n\n"
                     "С помощью меня ты можешь:\n\n"
                     "🎲 <b>Роллить дайсы</b> (единственные слова на эльфийском, что я знаю);\n\n"
                     "📝 <b>Ввести учет своих других, более интересных жизней</b>;\n\n"
                     "🧑 <b>Спихнуть ответственность за названия людей и имена городов на бездушный инструмент</b> (эт я, да :3);\n\n"
                     "🐗 <b>Находить гадов всех цветов и расцветок по щелчку пальца</b> (признаю, пальцев нет, но всех грязных тварей найду!);\n\n"
                     "👉👈 <b>Получить дозу хорошего настроения между партиями</b>;\n\n"
                     "И многое другое! - сказал бы я, было бы что-то еще...\n"
                     "В общем, помогу, чем смогу.\n\n"
                     "<b>Но для начала ответь:\n"
                     "ты ♂ Dungeon Master ♂ или ⚔ Игрок ⚔?</b>".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)

    def schedule_checker():
        while True:
            schedule.run_pending()
            sleep(30)

    def itsWednesdayMyDudes():
        return bot.send_photo(message.chat.id, "https://i.redd.it/qa90feu2yoh21.png", caption="Хорошей среды, мои чуваки!")

    schedule.every().wednesday.at("09:00").do(itsWednesdayMyDudes)
    Thread(target=schedule_checker).start()


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
    'Найти бестию': возвращает информацию о существе, название которого вводится пользователем
    """
    if message.chat.type == 'private':
        if message.text == '♂ Dungeon Master ♂':  # Переход в режим ДМ-а
            markup = markups.DMMarkup()
            bot.send_message(message.chat.id, "Хорошей Игры!\nЧего желаете?", reply_markup=markup)


        elif message.text == '⚔ Игрок ⚔':  # Переход в режим игрока
            markup = markups.PlayerMarkup()
            bot.send_message(message.chat.id, "Хорошей Игры!\nЧего желаете?", reply_markup=markup)

        elif message.text == 'Сменить роль':  # Замена роли на противоположную (Недоделано)
            markup = markups.mainMarkup()
            bot.send_message(message.chat.id, "Неужели, понадобились мои мемы?", reply_markup=markup)

        elif message.text == 'Листы персонажей':
            markup = types.InlineKeyboardMarkup(row_width=2)
            create = types.InlineKeyboardButton("Создать персонажа", callback_data='cs.create')
            view = types.InlineKeyboardButton("Просмотреть персонажа", callback_data='cs.view')
            edit = types.InlineKeyboardButton("Редактировать лист", callback_data='cs.edit')
            markup.add(create, view,  edit)
            bot.send_message(message.chat.id, "Выбери опцию", reply_markup=markup)

            @bot.callback_query_handler(func=lambda call: call.data.startswith('cs.'))
            def callback_inline(call):
                """
                Функция отвечает на вызовы при выборе инструмента "Листы персонажей"

                Используется для взаимодействия с меню
                """
                try:
                    if call.message:
                        if call.data == 'cs.create':
                            # Убираем строковые кнопки
                            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                  text="Отлично! Приступим к созданию очередного героя!",
                                                  reply_markup=None)
                            create_character(message)

                        elif call.data == 'cs.edit':
                            # Убираем строковые кнопки
                            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                  text="↓ Под вашим контролем следующие персонажи ↓",
                                                  reply_markup=None)
                            ans = bot.send_message(call.message.chat.id, playerMode.getListCharacters(str(message.from_user.id)))
                            if ans.text != "У вас еще нет персонажей":
                                findCharacterForEdit(message)



                        elif call.data == 'cs.view':
                            # Убираем строковые кнопки
                            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                  text="↓ Под вашим контролем следующие персонажи ↓",
                                                  reply_markup=None)
                            ans = bot.send_message(call.message.chat.id, playerMode.getListCharacters(str(message.from_user.id)))
                            if ans.text != "У вас еще нет персонажей":
                                 findCharacterForView(message)

                except Exception as e:
                    print(repr(e))

        elif message.text == 'Я здесь за мемами!':  # Вывод тематического мема (Недоделано)
            bot.send_photo(message.chat.id, memes.getMeme(), caption="Мемы? Их есть у меня!")

        elif message.text == 'Случайное Имя':  # Вывод случайного имени для НПС (Недоделано)
            bot.send_message(message.chat.id, "Прости, эта часть еще недоделана(")

        elif message.text == 'Случайный Город':  # Вывод случайного названия города (Недоделано)
            bot.send_message(message.chat.id, "Прости, эта часть еще недоделана(")

        elif message.text == 'Найти бестию': # Получение ссылки на бестию (Недоделано)
            markup = types.InlineKeyboardMarkup(row_width=1)
            take1 = types.InlineKeyboardButton("Найти бестию по имени", callback_data='take1')
            take2 = types.InlineKeyboardButton("FAQ", callback_data='take2')
            markup.add(take1, take2)
            bot.send_message(message.chat.id, "Нажми кнопку и получишь то, что ты хочешь", reply_markup=markup)
            @bot.callback_query_handler(func=lambda call: call.data.startswith('take'))
            def callback_inline(call):
                """
                Функция отвечает на вызовы при выборе инструмента "Найти бестию"

                Используется для взаимодействия с меню
                """
                try:
                    if call.message:
                        if call.data == 'take1':
                            # Убираем строковые кнопки
                            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                  text="Отлично! Приступим к получению информации о бестии!",
                                                  reply_markup=None)
                            take_bestia(message)
                        elif call.data == 'take2':
                            # Убираем строковые кнопки
                            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                  text="Милсдари и милсдарни часто задают вопросы по этой моей функции.\n"
                                                       "Так вот, уважаемые, чтобы найти в чертогах моего сознания нужную тварь -\n"
                                                       "мне нужно ее эльфийское имя (например, hare или bandit), тогда все будет хорошо. Обещаю.",
                                                  parse_mode='html', reply_markup=markup)
                except Exception as e:
                    print(repr(e))


        elif message.text == 'Дайсы кинь!':  # Бросок дайса
            markup = markups.diceMarkup()

            bot.send_message(message.chat.id, "Сколько нужно граней?", reply_markup=markup)

        # elif message.text == 'Найти бестию':
        #     bot.send_message(message.chat.id, "Прости, эта часть еще недоделана(")

        else:
            bot.send_message(message.chat.id,
                             'Милсдарь {0.first_name}, извольте! Ничего не понял... Скажите еще раз, по-другому!'.format(
                                 message.from_user, bot.get_me()))

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



@bot.message_handler(commands=['create_character'])
def create_character(message):
    """
    Функция для анкетирования

    Используется для создания нового персонажа
    """
    character = []
    character.append(str(message.from_user.id))
    

    def step1(msg):
        """
        Функция для анкетирования: шаг 1
        """
        character.append(msg.text)
        msg = bot.send_message(message.chat.id, 'Какой у него класс?')
        bot.register_next_step_handler(msg, step2)



    def step2(msg):
        """
        Функция для анкетирования: шаг 2
        """
        if msg.text != 'Пожалуйста, вводите число!':
            character.append(msg.text)
        msg = bot.send_message(message.chat.id, 'Какой у него сейчас уровень?')
        bot.register_next_step_handler(msg, step3)

    def step3(msg):
        """
        Функция для анкетирования: шаг 3
        """
        if msg.text.isdigit():
            character.append(msg.text)
            msg = bot.send_message(message.chat.id, 'Какой у него показатель Силы?')
            bot.register_next_step_handler(msg, step4)
        else:
            if msg.text == 'Пожалуйста, вводите число!':
                msg = bot.send_message(message.chat.id, 'Какой у него показатель Силы?')
                bot.register_next_step_handler(msg, step4)
            else:
                msg = bot.send_message(message.chat.id, 'Пожалуйста, вводите число!')
                step2(msg)

    def step4(msg):
        """
        Функция для анкетирования: шаг 4
        """
        if msg.text.isdigit():
            character.append(msg.text)
            msg = bot.send_message(message.chat.id, 'Какой у него показатель Ловкости?')
            bot.register_next_step_handler(msg, step5)
        else:
            if msg.text == 'Пожалуйста, вводите число!':
                msg = bot.send_message(message.chat.id, 'Какой у него показатель Ловкости?')
                bot.register_next_step_handler(msg, step5)
            else:
                msg = bot.send_message(message.chat.id, 'Пожалуйста, вводите число!')
                step3(msg)

    def step5(msg):
        """
        Функция для анкетирования: шаг 5
        """
        if msg.text.isdigit():
            character.append(msg.text)
            msg = bot.send_message(message.chat.id, 'Какой у него показатель Выносливости?')
            bot.register_next_step_handler(msg, step6)
        else:
            if msg.text == 'Пожалуйста, вводите число!':
                msg = bot.send_message(message.chat.id, 'Какой у него показатель Выносливости?')
                bot.register_next_step_handler(msg, step6)
            else:
                msg = bot.send_message(message.chat.id, 'Пожалуйста, вводите число!')
                step4(msg)

    def step6(msg):
        """
        Функция для анкетирования: шаг 6
        """
        if msg.text.isdigit():
            character.append(msg.text)
            msg = bot.send_message(message.chat.id, 'Какой у него показатель Интеллекта?')
            bot.register_next_step_handler(msg, step7)
        else:
            if msg.text == 'Пожалуйста, вводите число!':
                msg = bot.send_message(message.chat.id, 'Какой у него показатель Интеллекта?')
                bot.register_next_step_handler(msg, step7)
            else:
                msg = bot.send_message(message.chat.id, 'Пожалуйста, вводите число!')
                step5(msg)

    def step7(msg):
        """
        Функция для анкетирования: шаг 7
        """
        if msg.text.isdigit():
            character.append(msg.text)
            msg = bot.send_message(message.chat.id, 'Какой у него показатель Мудрости?')
            bot.register_next_step_handler(msg, step8)
        else:
            if msg.text == 'Пожалуйста, вводите число!':
                msg = bot.send_message(message.chat.id, 'Какой у него показатель Мудрости?')
                bot.register_next_step_handler(msg, step8)
            else:
                msg = bot.send_message(message.chat.id, 'Пожалуйста, вводите число!')
                step6(msg)

    def step8(msg):
        """
        Функция для анкетирования: шаг 8
        """
        if msg.text.isdigit():
            character.append(msg.text)
            msg = bot.send_message(message.chat.id, 'Какой у него показатель Харизмы?')
            bot.register_next_step_handler(msg, step9)
        else:
            if msg.text == 'Пожалуйста, вводите число!':
                msg = bot.send_message(message.chat.id, 'Какой у него показатель Харизмы?')
                bot.register_next_step_handler(msg, step9)
            else:
                msg = bot.send_message(message.chat.id, 'Пожалуйста, вводите число!')
                step7(msg)

    def step9(msg):
        """
        Функция для анкетирования: шаг 9
        """
        if msg.text.isdigit():
            character.append(msg.text)
            msg = bot.send_message(message.chat.id, 'Какой у него максимальный показатель здоровья?')
            bot.register_next_step_handler(msg, step10)
        else:
            if msg.text == 'Пожалуйста, вводите число!':
                msg = bot.send_message(message.chat.id, 'Какой у него максимальный показатель здоровья?')
                bot.register_next_step_handler(msg, step10)
            else:
                msg = bot.send_message(message.chat.id, 'Пожалуйста, вводите число!')
                step8(msg)

    def step10(msg):
        """
        Функция для анкетирования: шаг 10
        """
        if msg.text.isdigit():
            character.append(msg.text)
            msg = bot.send_message(message.chat.id, 'Какой у него класс брони?')
            bot.register_next_step_handler(msg, step11)
        else:
            if msg.text == 'Пожалуйста, вводите число!':
                msg = bot.send_message(message.chat.id, 'Какой у него класс брони?')
                bot.register_next_step_handler(msg, step11)
            else:
                msg = bot.send_message(message.chat.id, 'Пожалуйста, вводите число!')
                step9(msg)

    def step11(msg):
        """
        Функция для анкетирования: шаг 11

        Функция завершает анкетирование
        """
        if msg.text.isdigit():
            character.append(msg.text)
            playerMode.createCharacter(character)
            bot.send_message(message.chat.id, 'Ваш персонаж успешно создан!')
        else:
            msg = bot.send_message(message.chat.id, 'Пожалуйста, вводите число!')
            step10(msg)

    msg = bot.send_message(message.chat.id, 'Как зовут персонажа?')
    bot.register_next_step_handler(msg, step1)

@bot.message_handler(commands=['find_character'])
def findCharacterForView(message):
    """
    Функция принимает имя персонажа для поиска в таблице для вывода данных
    """
    def getName(msg):
        """
        Функция используется для вывода информации о персонаже
        """
        info = playerMode.getIinfoAboutCharacter(str(message.from_user.id), msg.text)
        bot.send_message(message.chat.id, info.format(message.from_user, bot.get_me()), parse_mode='html')

    msg = bot.send_message(message.chat.id, 'Введите имя персонажа, данные о котором вам нужны')
    bot.register_next_step_handler(msg, getName)

@bot.message_handler(commands=['find_character_for_edit'])
def findCharacterForEdit(message):
    """
    Функция принимает имя персонажа для поиска в таблице для вывода данных
    """

    def getName(msg):
        """
        Функция используется для вывода информации о персонаже
        """

        characterName = msg.text
        info = playerMode.getIinfoAboutCharacter(str(message.from_user.id), msg.text)

        if info != "У вас нет персонажа с таким именем":
            info = "Ваш персонаж на данный момент имеет следующие данные:\n\n" + info
            bot.send_message(message.chat.id, info.format(message.from_user, bot.get_me()), parse_mode='html')

            name = types.InlineKeyboardButton("Имя", callback_data='ce.name.'+characterName)
            cl = types.InlineKeyboardButton("Класс", callback_data='ce.class.'+characterName)
            lvl = types.InlineKeyboardButton("Уровень", callback_data='ce.level.'+characterName)

            s = types.InlineKeyboardButton("СИЛ", callback_data='ce.strength.'+characterName)
            dex = types.InlineKeyboardButton("ЛОВ", callback_data='ce.dexterity.'+characterName)
            sta = types.InlineKeyboardButton("ВЫН", callback_data='ce.stamina.'+characterName)
            intellect = types.InlineKeyboardButton("ИНТ", callback_data='ce.intellect.'+characterName)
            w = types.InlineKeyboardButton("МУД", callback_data='ce.wisdom.'+characterName)
            ch = types.InlineKeyboardButton("ХАР", callback_data='ce.charisma.'+characterName)

            hp = types.InlineKeyboardButton("Максимальное ХП", callback_data='ce.hp.'+characterName)
            armor = types.InlineKeyboardButton("Класс брони", callback_data='ce.armor_class.'+characterName)

            inventory = types.InlineKeyboardButton("Инвентарь", callback_data='ce.inventory.'+characterName)

            markup = types.InlineKeyboardMarkup([[name, cl, lvl],
                                                 [s, dex, sta, intellect, w, ch],
                                                 [hp, armor],
                                                 [inventory]])
            bot.send_message(message.chat.id, "Что хотите изменить?", reply_markup=markup)

            @bot.callback_query_handler(func=lambda call: call.data.startswith('ce.'))
            def callback_inline(call):
                """
                Функция отвечает на вызовы

                Используется для изменения данных в листах персонажей
                """

                call.data = call.data[3:]
                callData = re.search(r'(.*?)(\.)(.*)', call.data)

                parametr = callData[1]
                characterName = callData[3]

                print("In c_i: ", characterName, call.data, parametr)
                @bot.message_handler(commands=['set_val'])
                def setVal(message):
                    """
                    Функция принимает новые данные для листа персонажа
                    """
                    print("В setVal: ", characterName, parametr)
                    if parametr != "name" and parametr != "class" and parametr != "inventory":
                        if not message.text.isdigit():
                            bot.send_message(message.chat.id, "Вы ввели некорректные данные. Изменения не были внесены.")
                        else:
                            res = playerMode.changeInfoAboutCharacter(str(message.from_user.id), characterName,
                                                                      parametr, message.text)
                            bot.send_message(message.chat.id, res)
                    else:
                        res = playerMode.changeInfoAboutCharacter(str(message.from_user.id), characterName, parametr,
                                                                  message.text)
                        bot.send_message(message.chat.id, res)

                try:
                    if call.message:
                        # Убираем строковые кнопки
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text="↓ Введите новые данные ↓",
                                              reply_markup=None)
                        bot.register_next_step_handler(msg, setVal)

                except Exception as e:
                    print(repr(e))
        else:
            bot.send_message(message.chat.id, info)

    msg = bot.send_message(message.chat.id, 'Введите имя персонажа, данные о котором хотите изменить')
    bot.register_next_step_handler(msg, getName)


def form_url(message):
        """
        Получение ссылки
        """
        name = message.text
        url= URL + name
        message = bot.send_message(message.chat.id, f'Лови описание хомячок: {url}')

@bot.message_handler(commands=['Найти бестию'])
def take_bestia(message):
    """
    Функция для получения бестии
    """

    msg = bot.send_message(message.chat.id, 'Какую бестию вы хотите получить?')
    bot.register_next_step_handler(msg, form_url)

# Запуск!
bot.polling(none_stop=True)


