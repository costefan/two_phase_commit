from .transaction_manager import TransactionManager


class Account:

    _engine = None

    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

    def set_engines(self, engine1, engine2, engine3):
        self._engine1 = engine1
        self._engine2 = engine2
        self._engine3 = engine3

    def book_flight(self):
        transaction_manager = TransactionManager(
            self._engine1,
            self._engine2,
            self._engine3,
        )

        transaction_manager.run()
