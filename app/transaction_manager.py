from .accounts_models import t_user_account
from .flights_models import t_bookings as flight_bookings
from .hotels_models import t_bookings as hotels_bookings
import psycopg2

class TransactionManager:

    QUERIES = {
        'fly_booking': flight_bookings.insert().values(
            booking_id=12,
            client_name='Kostya'
        ),
        'hotels_booking': hotels_bookings.insert().values(
            booking_id=12,
            client_name='Kostya'
        ),
        'account_withdraw': t_user_account.update().values(
            amount=(
                 t_user_account.c.amount - 100
            )
        )
    }

    def __init__(self,
                 engine1,
                 engine2,
                 engine3):
        self.engine1 = engine1
        self.engine2 = engine2
        self.engine3 = engine3

    def run(self):
        print('Started transaction_manager...')
        print('Cursors')
        rollback = False
        prepared_f, prepared_s, prepared_th = False, False, False
        cur1 = self.engine1.cursor(); cur1.execute('BEGIN')
        cur2 = self.engine2.cursor(); cur2.execute("BEGIN")
        cur3 = self.engine3.cursor(); cur3.execute("BEGIN")
        print('Started TWO phase')
        try:
            print('Executing')

            cur1.execute('insert into bookings (booking_id, client_name)'
                         ' values (12, \'Kostya\')')
            cur1.execute("PREPARE TRANSACTION 'foobar1'")
            prepared_f = True

            cur2.execute('insert into bookings (booking_id, client_name)'
                         ' values (12, \'Kostya\')')
            cur2.execute("PREPARE TRANSACTION 'foobar2'")
            prepared_s = True

            cur3.execute('update user_account'
                         ' set ammount = ammount - {}'.format(100))
            cur3.execute("PREPARE TRANSACTION 'foobar3'")
            prepared_th = True

            print('Preparing')
        except (Exception, psycopg2.IntegrityError) as err:
            print('Rollback block')
            print('-------------------------')

            print("cause " + str(err))
            rollback = True

            if prepared_f:
                cur1.execute("ROLLBACK PREPARED 'foobar1'")
            if prepared_s:
                cur2.execute("ROLLBACK PREPARED 'foobar2'")
            if prepared_th:
                cur3.execute("ROLLBACK PREPARED 'foobar3'")
            print('ROLLBacked')

        if not rollback:
            print('Commit prepared')

            cur1.execute("COMMIT PREPARED 'foobar1'")

            cur2.execute("COMMIT PREPARED 'foobar2'")
            cur3.execute("COMMIT PREPARED 'foobar3'")

        # else:
        #     if prepared_f:
        #         cur1.execute("ROLLBACK PREPARED 'foobar1'")
        #     if prepared_s:
        #         cur2.execute("ROLLBACK PREPARED 'foobar2'")
        #     if prepared_th:
        #         cur3.execute("ROLLBACK PREPARED 'foobar3'")
        #     print('ROLLBacked')

        print('Closing connections...')

        self.engine1.close()
        self.engine2.close()
        self.engine3.close()
        print('Closed')
