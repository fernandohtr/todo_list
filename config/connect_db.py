from psycopg2 import connect


def connect_to_db():
    _connection = connect(
        user='postgres',
        password='senha',
        host='127.0.0.1',
        port='5432',
        database='todo',
    )
    return _connection


connection = connect_to_db()
