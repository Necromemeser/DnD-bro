from dbConnection import connection, DBfinish


try:

    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS charactersheet(
                user_id varchar(50) NOT NULL,
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
        print("[INFO] Successful connection to the characters table")

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




def changeInfoAboutCharacter(userID, characterName, parameter, val):
    """
    Функция меняет данные в листе персонажа
    """
    print("Внутри changeInfoAboutCharacter", characterName)
    with connection.cursor() as cursor:
        if parameter != "name" and parameter != "class" and parameter != "inventory":
            cursor.execute(
                f"""UPDATE charactersheet SET {parameter} = {val} WHERE user_id = '{userID}' AND name = '{characterName}'""")
            return "Данные успешно обновлены!"
        else:
            cursor.execute(
                f"""UPDATE charactersheet SET {parameter} = '{val}' WHERE user_id = '{userID}' AND name = '{characterName}'""")
            return "Данные успешно обновлены!"
