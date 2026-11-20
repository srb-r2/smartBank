import pytest
from decimal import Decimal

from BankAccount import BankAccount, CurrentAccount, SavingAccount


# TEST 1 — Création d'un compte bancaire
def test_create_account():
    account = BankAccount(101, "500.00")

    assert account.Account_id == 101
    assert account.Solde == Decimal("500.00")
    assert account.Logs == []


# TEST 2 — Dépôt d'argent
def test_deposit():
    account = BankAccount(101, "500.00")

    account.deposit("150.75")

    assert account.Solde == Decimal("650.75")
    assert len(account.Logs) == 1
    assert account.Logs[0]["action"] == "deposit"
    assert account.Logs[0]["amount"] == Decimal("150.75")


# TEST 3 — Retrait d'argent
def test_withdraw():
    account = BankAccount(101, "500.00")

    account.withdraw("100.25")

    assert account.Solde == Decimal("399.75")
    assert account.Logs[0]["action"] == "withdraw"


# TEST 4 — Interdire les dépôts invalides
@pytest.mark.parametrize("amount", [
    "0",
    "-50",
    "NaN",
    "Infinity",
])
def test_invalid_deposit(amount):
    account = BankAccount(101, "500.00")

    with pytest.raises(ValueError):
        account.deposit(amount)

    assert account.Solde == Decimal("500.00")
    assert account.Logs == []


# TEST 5 — Interdire les retraits invalides
@pytest.mark.parametrize("amount", [
    "0",
    "-20",
    "NaN",
    "Infinity",
])
def test_invalid_withdraw(amount):
    account = BankAccount(101, "500.00")

    with pytest.raises(ValueError):
        account.withdraw(amount)

    assert account.Solde == Decimal("500.00")
    assert account.Logs == []


# TEST 6 — Fonds insuffisants
def test_insufficient_funds():
    account = BankAccount(101, "100.00")

    with pytest.raises(ValueError, match="Insufficient funds"):
        account.withdraw("150.00")

    assert account.Solde == Decimal("100.00")
    assert account.Logs == []


# TEST 7 — Solde initial invalide
@pytest.mark.parametrize("balance", [
    "-100",
    "NaN",
    "Infinity",
])
def test_invalid_initial_balance(balance):
    with pytest.raises(ValueError):
        BankAccount(101, balance)


# TEST 8 — Historique chronologique des transactions
def test_transaction_history():
    account = BankAccount(101, "500.00")

    account.deposit("100.00")
    account.withdraw("50.00")

    assert len(account.Logs) == 2
    assert account.Logs[0]["action"] == "deposit"
    assert account.Logs[1]["action"] == "withdraw"

    assert account.Logs[0]["Date"]
    assert account.Logs[0]["time"]


# TEST 9 — Encapsulation du journal
def test_logs_are_protected():
    account = BankAccount(101, "500.00")
    account.deposit("50.00")

    logs_copy = account.Logs
    logs_copy.clear()

    assert len(account.Logs) == 1


# TEST 10 — Héritage du compte courant
def test_current_account_inheritance():
    account = CurrentAccount(201, "500.00")

    assert isinstance(account, BankAccount)

    account.deposit("100.00")
    account.withdraw("50.00")

    assert account.Solde == Decimal("550.00")


# TEST 11 — Calcul des intérêts
def test_savings_interest_calculation():
    account = SavingAccount(301, "1000.00", "0.05")

    interest = account.calculate_interest()

    assert interest == Decimal("50.00")
    assert account.Solde == Decimal("1000.00")
    assert account.Interest_rate == Decimal("0.05")


# TEST 12 — Application des intérêts
def test_apply_interest():
    account = SavingAccount(301, "1000.00", "0.05")

    interest = account.apply_interest()

    assert interest == Decimal("50.00")
    assert account.Solde == Decimal("1050.00")

    assert len(account.Logs) == 1
    assert account.Logs[0]["action"] == "interest"
    assert account.Logs[0]["amount"] == Decimal("50.00")


# TEST 13 — Taux d'intérêt invalide
@pytest.mark.parametrize("rate", [
    "-0.05",
    "1.5",
    "NaN",
    "Infinity",
])
def test_invalid_interest_rate(rate):
    with pytest.raises(ValueError):
        SavingAccount(301, "1000.00", rate)


# TEST 14 — Aucun intérêt sur un solde nul
def test_zero_balance_interest():
    account = SavingAccount(301, "0.00", "0.05")

    interest = account.apply_interest()

    assert interest == Decimal("0.00")
    assert account.Solde == Decimal("0.00")
    assert account.Logs == []
