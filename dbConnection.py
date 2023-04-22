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

except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
    DBfinish(connection)