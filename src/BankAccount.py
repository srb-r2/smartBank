from datetime import datetime
from zoneinfo import ZoneInfo
from decimal import Decimal


class BankAccount:

    def __init__(self, account_id, solde="0.00"):

        solde = Decimal(str(solde))
        if not solde.is_finite() or solde < 0:
            raise ValueError("Invalid initial balance.")
        self.__account_id = account_id
        self.__solde = solde
        self.__logs = []

    @property
    def Solde(self):
        return self.__solde

    @property
    def Account_id(self):
        return self.__account_id

    @property
    def Logs(self):
        return self.__logs.copy()

    def _datetime_log(self):

        fuseau = ZoneInfo("America/Toronto")

        maintenant = datetime.now(fuseau)

        date_format = maintenant.strftime("%Y-%m-%d")
        time_format = maintenant.strftime("%H:%M")

        return date_format, time_format

    def deposit(self, amount,  transaction_type="deposit"):
        amount = Decimal(str(amount))

        if not amount.is_finite() or amount <= 0:
            raise ValueError("Deposit amount must be positive.")

        else:
            self.__solde += amount
            date, time = self._datetime_log()
            self._update_log(date, time, transaction_type, amount)

    def withdraw(self, amount, transaction_type="withdraw"):
        amount = Decimal(str(amount))
        if not amount.is_finite() or amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")

        if amount > self.__solde:
            raise ValueError("Insufficient funds.")

        self.__solde -= amount

        date, time = self._datetime_log()
        self._update_log(date, time, transaction_type, amount)

    def _update_log(self, date, time, action, amount):
        self.__logs.append({"Date": date, "time": time,
                            "action": action, "amount": amount})


class CurrentAccount(BankAccount):
    pass


class SavingAccount(BankAccount):
    def __init__(self, account_id, solde=0, interest_rate="0.05"):
        super().__init__(account_id, solde)

        interest_rate = Decimal(str(interest_rate))

        if not interest_rate.is_finite() or not 0 <= interest_rate <= 1:
            raise ValueError("Interest rate must be between 0 and 1.")

        self.__interest_rate = interest_rate

    @property
    def Interest_rate(self):
        return self.__interest_rate

    def calculate_interest(self):
        interest = self.Solde * self.__interest_rate

        return interest.quantize(Decimal("0.01"))

    def apply_interest(self):
        interest = self.calculate_interest()

        if interest > 0:
            self.deposit(interest, "interest")

        return interest
