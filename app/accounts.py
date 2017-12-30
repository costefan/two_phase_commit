from .accounts_models import t_user_account

from .transaction_manager import TransactionManager


class Account:

    _engine = None

    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

    def set_engine(self, engine):
        self._engine = engine

    async def book_flight(self):
        transaction_manager = TransactionManager(self._engine)

        await transaction_manager.run()
