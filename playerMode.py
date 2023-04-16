import psycopg2

from config import host, user, password, db_name

def DBfinish(connection):
    """
    Функция завершает работу с базой данных
    """
    if connection:
        connection.close()
        print("[INFO] PostgreSQL connection closed")

try:
    # Подключение к базе данных
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS charactersheet(
                user_id int NOT NULL,
                id serial PRIMARY KEY,
                name varchar(50) NOT NULL,
                class varchar(50),
                level int NOT NULL,
                strength int DEFAULT -1, 
                dexterity int DEFAULT -1, 
                stamina int DEFAULT -1, 
                intellect int DEFAULT -1, 
                wisdom int DEFAULT -1, 
                charisma int DEFAULT -1,
                hp int DEFAULT -1,
                armor_class int DEFAULT -1,
                inventory varchar(600));"""
        )
        print("[INFO] Successful connection to the table")


except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
    DBfinish(connection)


def createCharacter(character):
    """
    Функция добавляет в таблицу нового персонажа
    """
    with connection.cursor() as cursor:
        cursor.execute(
            """INSERT INTO charactersheet(user_id, name, class, level, strength, dexterity, 
                    stamina, intellect, wisdom, charisma, hp, armor_class) VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", character)


def getListCharacters(userID):
    """
    Функция возвращает список персонажей, которые доступны пользователю
    """
    with connection.cursor() as cursor:
        select_all_rows = f"""SELECT * FROM charactersheet WHERE user_id = {userID}"""
        cursor.execute(select_all_rows)
        rows = cursor.fetchall()
        if rows is not None:
            listCharacters = "[ №: Имя - Класс ]\n"
            i = 1
            for row in rows:
                listCharacters += str(i) + ": " + row[2] + " - " + row[3] + "\n"
                i += 1
            return listCharacters
        else:
            return "У вас еще нет персонажей"


def getIinfoAboutCharacter(userID, name):
    """
    Функция возвращает информацию о конкретном персонаже
    """
    with connection.cursor() as cursor:
        select_all_rows = f"""SELECT * FROM charactersheet WHERE user_id = {userID} AND name = '{name}'"""
        cursor.execute(select_all_rows)
        character = cursor.fetchone()
        if character is not None:
            info = ""
            info += "<b>Имя</b>: " + character[2] + "\n"
            info += "<b>Класс</b>: " + character[3] + "\n"
            info += "<b>Уровень</b>: " + str(character[4]) + "\n\n"
            info += "<b><i>Сила</i></b>: " + str(character[5]) + "\n"
            info += "<b><i>Ловкость</i></b>: " + str(character[6]) + "\n"
            info += "<b><i>Выносливость</i></b>: " + str(character[7]) + "\n"
            info += "<b><i>Интеллект</i></b>: " + str(character[8]) + "\n"
            info += "<b><i>Мудрость</i></b>: " + str(character[9]) + "\n"
            info += "<b><i>Харизма</i></b>: " + str(character[10]) + "\n\n"
            info += "<b>Максимальное ХП</b>: " + str(character[11]) + "\n"
            info += "<b>Класс брони</b>: " + str(character[12]) + "\n\n"
            if character[13] is None:
                info += "<b><i>Инвентарь</i></b>:\n[ ПУСТО ]"
            else:
                info += "<b><i>Инвентарь</i></b>:\n" + character[13]
            return info
        else:
            return "У вас нет персонажа с таким именем"


def changeInfoAboutCharacter(userID, characterName, parameter, val):
    """
    Функция меняет данные в листе персонажа
    """
    print("Внутри changeInfoAboutCharacter", characterName)
    with connection.cursor() as cursor:
        if parameter != "name" and parameter != "class" and parameter != "inventory":
            cursor.execute(
                f"""UPDATE charactersheet SET {parameter} = {val} WHERE user_id = {userID} AND name = '{characterName}'""")
            return "Данные успешно обновлены!"
        else:
            cursor.execute(
                f"""UPDATE charactersheet SET {parameter} = '{val}' WHERE user_id = {userID} AND name = '{characterName}'""")
            return "Данные успешно обновлены!"