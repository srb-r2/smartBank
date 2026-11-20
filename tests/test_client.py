
from decimal import Decimal
from BankAccount import BankAccount, CurrentAccount, SavingAccount
from Client import Client


def test_duplicate_account():
    client = Client(1, "Asma", "Roujaina")

    account1 = CurrentAccount(101, "500.00")
    account2 = SavingAccount(101, "1000.00")

    client.add_account(account1)
    client.add_account(account2)

    assert len(client.Accounts) == 1
    assert client.Accounts[101] is account1


def test_remove_empty_account():
    client = Client(2, "Sarah", "Martin")

    account = CurrentAccount(202, "100.00")
    client.add_account(account)

    account.withdraw("100.00")
    client.remove_account(202)

    assert 202 not in client.Accounts
