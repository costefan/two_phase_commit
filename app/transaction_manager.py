from .accounts_models import t_user_account
from .flights_models import t_bookings as flight_bookings
from .hotels_models import t_bookings as hotels_bookings
import psycopg2

class TransactionManager:

    QUERIES = {
        'fly_booking': flight_bookings.insert().values(
                        booking_id=12,
                        client_name='aaa'),
        'hotels_booking': hotels_bookings.insert().values(
                            booking_id=12,
                            client_name='aaa'),
        'account_withdraw': t_user_account.update().values(
            amount=(
                 t_user_account.c.amount - 100)
        )
            # .where(t_user_account.c.name == 'Kostya')
    }

    def __init__(self, engine):
        self.engine = engine

    async def run(self):
        print('Started transaction_manager...')
        conn1 = await self.engine.acquire()
        conn2 = await self.engine.acquire()
        conn3 = await self.engine.acquire()
        print('Getted connections')
        tr1 = await conn1.begin_twophase()
        tr2 = await conn2.begin_twophase()
        tr3 = await conn3.begin_twophase()
        print('Started twophase')
        try:
            print('Executing')
            await conn1.execute(self.QUERIES.get('fly_booking'))
            await tr1.prepare()

            await conn2.execute(self.QUERIES.get('hotels_booking'))
            await tr2.prepare()

            await conn3.execute(self.QUERIES.get('account_withdraw'))
            await tr3.prepare()
        except (Exception, psycopg2.IntegrityError) as err:
            print('Rollback')
            print("cause " + str(err))
            if tr1._is_prepared:
                await conn1.rollback_prepared(tr1.xid)
            if tr2._is_prepared:
                await conn2.rollback_prepared(tr2.xid)
            if tr3._is_prepared:
                await conn3.rollback_prepared(tr3.xid)
            print('Rollbacked')
        else:
            try:
                print('Commit prepared')
                await conn1.commit_prepared(tr1.xid)
                print('Commited 1')
                await conn2.commit_prepared(tr2.xid)
                print('Commited 2')
                await conn3.commit_prepared(tr3.xid)
                print('Commited 3')
            except Exception as err:
                print('Commit err' + str(err))
        finally:
            tr1._is_active = False
            tr2._is_active = False
            tr3._is_active = False
            print('Closing connections...')

            await conn1.close()
            await conn2.close()
            await conn3.close()
            print('Closed')
