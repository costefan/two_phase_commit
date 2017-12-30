import asyncio
from aiopg.sa import create_engine

from scripts.management import prepare_database

from .settings import (
    DB_HOST, DB_NAME, DB_PASSWORD, DB_USER
)
from .accounts import Account
from .transaction_manager import TransactionManager


async def go():
    async with create_engine(user=DB_USER,
                             database=DB_NAME,
                             host=DB_HOST,
                             password=DB_PASSWORD) as engine:
        account = Account('Kostya', 320)
        account.set_engine(engine)

        await account.book_flight()


def main():
    prepare_database(DB_NAME)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(go())
    loop.close()
