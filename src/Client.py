from BankAccount import BankAccount, CurrentAccount, SavingAccount


class Client:

    def __init__(self, client_id, first_name, last_name):

        self.__client_id = client_id
        self.first_name = first_name
        self.last_name = last_name
        self.__accounts = {}

    @property
    def Client_id(self):
        return self.__client_id

    @property
    def Accounts(self):
        return self.__accounts.copy()

    def add_account(self, account):

        if not isinstance(account, BankAccount):
            raise TypeError("Expected a BankAccount instance.")

        if self._account_exist(account.Account_id):
            print("This account already exists.")
            return

        self.__accounts[account.Account_id] = account

    def _account_exist(self, account_id):
        return account_id in self.__accounts

    def remove_account(self, account_id):
        if not self._account_exist(account_id):
            print("Account does not exist.")
            return

        account = self.__accounts[account_id]
        if account.Solde != 0:
            print("Cannot remove an account with a non-zero balance.")
            return

        del self.__accounts[account_id]

        print("Account successfully removed.")

    def show_account(self):
        for k, v in self.__accounts.items():
            print(f"Account_id : {k}")
            print(f"Account type:  {type(v).__name__}")
            print(f"Slode : {v.Solde}")
