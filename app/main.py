import asyncio
from aiopg.sa import create_engine

from scripts.management import prepare_database
from .models import tbl, metadata


async def create_tables(engine):
    async with engine.acquire() as conn:
        await conn.execute('DROP TABLE IF EXISTS tbl')
        await conn.execute('''CREATE TABLE tbl (
                                  id serial PRIMARY KEY,
                                  val varchar(255))''')

async def go():
    async with create_engine(user='postgres',
                             database='aiopg',
                             host='127.0.0.1',
                             password='') as engine:

        metadata.create_all(engine)

prepare_database()

loop = asyncio.get_event_loop()
loop.run_until_complete(go())
