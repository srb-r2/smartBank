from Client import Client
from decimal import Decimal
from BankAccount import BankAccount, CurrentAccount, SavingAccount


class Bank:
    def __init__(self):
        self.__clients: dict[int, Client] = {}

    def add_client(self, client):
        if not isinstance(client, Client):

            raise TypeError("Expected a Client instance.")

        if self._client_exist(client.Client_id):

            print("client already exist")
            return

        self.__clients[client.Client_id] = client

    def _client_exist(self, client_id):

        return client_id in self.__clients

    def find_client(self, client_id):
        return self.__clients.get(client_id)

    def remove_client(self, client_id):
        if not self._client_exist(client_id):
            print("client does not exist.")
            return

        client = self.__clients[client_id]
        if client.Accounts:
            print("can't remove the client still have accounts")
            return

        del self.__clients[client_id]

    def show_client(self):
        for k, v in self.__clients.items():
            print(f"client_id : {k}")
            print(f"client_name:  {v.first_name}")
            print(f"client last name : {v.last_name}")

    def find_account(self, account_id):
        for client in self.__clients.values():
            if account_id in client.Accounts:
                return client.Accounts[account_id]

        return None

    def transfer(self, source_id, destination_id, amount):
        source: BankAccount | None = self.find_account(source_id)

        destination: BankAccount | None = self.find_account(destination_id)

        if source is None or destination is None:
            raise ValueError("Account don't existe")

        if source_id == destination_id:
            raise ValueError("Account must be diffrent ")

        amount = Decimal(str(amount))
        if not amount.is_finite() or amount <= 0:
            raise ValueError("Transfer amount must be positive.")

        if amount > source.Solde:
            raise ValueError("Insufficient funds from the source.")

        source.withdraw(amount, "transfer_out")
        try:
            destination.deposit(amount, "transfer_in")

        except Exception:
            source.deposit(amount, "transfer_refund")
            raise
