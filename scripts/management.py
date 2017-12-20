import psycopg2
from sqlalchemy import create_engine

import app.settings as settings


def prepare_database(database_name, delete_existing: bool=True) -> bool:
    """
    (Re)create a fresh database and run migrations.

    :param delete_existing: whether or not to drop an existing database if it exists
    :return: whether or not a database has been (re)created
    """

    conn = psycopg2.connect(
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
    )
    conn.autocommit = True
    cur = conn.cursor()
    db_name = database_name
    cur.execute(
        'SELECT EXISTS (SELECT datname FROM'
        ' pg_catalog.pg_database WHERE datname=%s)', (db_name,)
    )
    already_exists = bool(cur.fetchone()[0])
    if already_exists:
        if not delete_existing:
            print('database "{}" already exists, skipping'.format(db_name))
            return False
        else:
            print('dropping database "{}" as it already exists...'.format(
                db_name))
            cur.execute('DROP DATABASE {}'.format(db_name))
    else:
        print('database "{}" does not yet exist'.format(db_name))

    print('creating database "{}"...'.format(db_name))
    cur.execute('CREATE DATABASE {}'.format(db_name))
    cur.close()
    conn.close()

    return True
