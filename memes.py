import random
import re

from dbConnection import connection, DBfinish

def getMeme():

    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT COUNT(*) FROM memes"""
        )
        print("[INFO] Successfully counted memes")
        results = list(cursor)
        random_id = random.randint(0, int(re.sub("[(,)]", "", str(results[0]))) - 1)
        get_a_meme = f"""SELECT link FROM memes WHERE id = '{random_id}'"""
        cursor.execute(get_a_meme)
        results = list(cursor)
        meme_needed = re.sub("[''(,)]", "", str(results[0]))
        return meme_needed


try:
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS memes(
                id serial PRIMARY KEY,
                link varchar(100) NOT NULL);"""
        )
        print("[INFO] Successful connection to the table")

    getMeme()
    # Блок кода для добавления 10 мемов в БД
    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         """INSERT INTO memes (id, link) VALUES
    #         (0, 'https://i.redd.it/gmy77cewadva1.jpg'),
    #         (1, 'https://i.redd.it/gmy77cewadva1.jpg''),
    #         (2, 'https://i.redd.it/rzje90afedva1.png'),
    #         (3, 'https://i.redd.it/azfniau2pcva1.jpg'),
    #         (4, 'https://i.redd.it/p2rd0rp0icva1.png'),
    #         (5, 'https://i.redd.it/3y45r1hr49va1.jpg'),
    #         (6, 'https://i.redd.it/m2ddfeuvv9va1.png'),
    #         (7, 'https://i.redd.it/l4x87kxwi7va1.jpg'),
    #         (8, 'https://i.redd.it/dgnbv8f9d7va1.jpg'),
    #         (9, 'https://i.redd.it/megyyjjcp5va1.jpg');"""
    #     )
    #     print("[INFO] memes added")

except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
    DBfinish(connection)


