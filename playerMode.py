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
                """CREATE TABLE CharacterSheet(
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
    cursor.execute(
        f"""INSERT INTO CharacterSheet(name, class, level, strength, dexterity, 
            stamina, intellect, wisdom, charisma, hp, armor_class) VALUES
            ({str(character[0])}, {str(character[1])}, {int(character[2])}, {int(character[3])},
             {int(character[4])}, {int(character[5])}, {int(character[6])}, {int(character[7])},
             {int(character[8])}, {int(character[9])}, {int(character[10])}, {int(character[11])});"""
    )

