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
        if cursor.execute("""SELECT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME='charactersheet');""") == False:
            cursor.execute(
                """CREATE TABLE charactersheet(
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

            print("[INFO] Table created successfully")
            #DBfinish(connection)

except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
    DBfinish(connection)


def createCharacter(character):
    """
    Функция добавляет в таблицу нового персонажа
    """
    with connection.cursor() as cursor:
        cursor.execute(
            """INSERT INTO charactersheet(name, class, level, strength, dexterity, 
                    stamina, intellect, wisdom, charisma, hp, armor_class) VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", character
        )