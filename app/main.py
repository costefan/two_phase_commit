import psycopg2

from scripts.management import prepare_database

from .settings import (
    DB_HOST, DB_NAME, DB_PASSWORD, DB_USER,
    FLY_SCHEMA, HOTELS_SCHEMA, ACCOUNT_SCHEMA
)
from .accounts import Account


def go():
    conn1 = psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
                             dbname=FLY_SCHEMA)
    conn2 = psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
                             dbname=HOTELS_SCHEMA)
    conn3 = psycopg2.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
                             dbname=ACCOUNT_SCHEMA)

    account = Account('Kostya', 320)
    account.set_engines(conn1, conn2, conn3)

    account.book_flight()


def main():
    prepare_database(DB_NAME)
    go()
