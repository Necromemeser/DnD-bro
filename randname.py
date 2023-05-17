import random
import re

from dbConnection import connection, DBfinish


def getName():
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT COUNT(*) FROM names"""
        )
        print("[INFO] Successfully counted names")
        results = list(cursor)
        random_id = random.randint(0, int(re.sub("[(,)]", "", str(results[0]))) - 1)
        get_a_name = f"""SELECT name FROM names WHERE id = '{random_id}'"""
        cursor.execute(get_a_name)
        results = list(cursor)
        name_needed = re.sub("[''(,)]", "", str(results[0]))
        return name_needed


try:
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS names(
                id serial PRIMARY KEY,
                name varchar(20) NOT NULL);"""
        )
        print("[INFO] Successful connection to the names table")

    # # Блок кода для добавления 10 имен в БД
    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         """INSERT INTO names (id, name) VALUES
    #         (0, 'Тана Шемов'),
    #         (1, 'Григор Стараг'),
    #         (2, 'Катернин Немецк'),
    #         (3, 'Мико Хелниб'),
    #         (4, 'Брентор Рунтроп'),
    #         (5, 'Лют Фолд'),
    #         (6, 'Элли Алгой'),
    #         (7, 'Мейлиль Баша'),
    #         (8, 'Дейман Рейн'),
    #         (9, 'Мейлиль Пашар');"""
    #     )
    #    print("[INFO] names added")
    # getName()

except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
    DBfinish(connection)


def getCity():
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT COUNT(*) FROM cities"""
        )
        print("[INFO] Successfully counted cities")
        results = list(cursor)
        random_id = random.randint(0, int(re.sub("[(,)]", "", str(results[0]))) - 1)
        get_a_city = f"""SELECT city FROM cities WHERE id = '{random_id}'"""
        cursor.execute(get_a_city)
        results = list(cursor)
        city_needed = re.sub("[''(,)]", "", str(results[0]))
        return city_needed


try:
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS cities(
                id serial PRIMARY KEY,
                city varchar(20) NOT NULL);"""
        )
        print("[INFO] Successful connection to the cities table")

    # Блок кода для добавления 10 городов в БД
    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         """INSERT INTO cities (id, city) VALUES
    #         (0, 'Ёфдар'),
    #         (1, 'Изсима'),
    #         (2, 'Ижянь'),
    #         (3, 'Умберг'),
    #         (4, 'Перск'),
    #         (5, 'Ярбург'),
    #         (6, 'Отград'),
    #         (7, 'Эхика'),
    #         (8, 'Первальд'),
    #         (9, 'Инбург');"""
    #     )
    #     print("[INFO] cities added")
    # getCity()

except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
    DBfinish(connection)
