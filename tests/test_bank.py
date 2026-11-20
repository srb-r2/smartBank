
import pytest
from decimal import Decimal

from Bank import Bank
from Client import Client
from BankAccount import CurrentAccount, SavingAccount


# ==========================================
# FIXTURE : PRÉPARER UNE BANQUE DE TEST
# ==========================================

@pytest.fixture
def bank():
    bank = Bank()

    client1 = Client(1, "Asma", "Roujaina")
    client2 = Client(2, "Sarah", "Martin")

    account1 = CurrentAccount(101, "1000.00")
    account2 = SavingAccount(202, "300.00")

    client1.add_account(account1)
    client2.add_account(account2)

    bank.add_client(client1)
    bank.add_client(client2)

    return bank


# ==========================================
# TESTS : GESTION DES CLIENTS
# ==========================================

def test_add_client(bank):
    assert bank.find_client(1) is not None
    assert bank.find_client(2) is not None


def test_find_nonexistent_client(bank):
    assert bank.find_client(999) is None


def test_reject_invalid_client(bank):
    with pytest.raises(TypeError):
        bank.add_client("Not a client")


def test_duplicate_client(bank):
    duplicate = Client(1, "Other", "Person")

    bank.add_client(duplicate)

    assert bank.find_client(1).first_name == "Asma"


def test_remove_client_without_accounts(bank):
    new_client = Client(3, "John", "Smith")
    bank.add_client(new_client)

    bank.remove_client(3)

    assert bank.find_client(3) is None


def test_refuse_remove_client_with_accounts(bank):
    bank.remove_client(1)

    assert bank.find_client(1) is not None


# ==========================================
# TESTS : RECHERCHE DE COMPTES
# ==========================================

def test_find_account(bank):
    account = bank.find_account(101)

    assert account is not None
    assert account.Account_id == 101
    assert account.Solde == Decimal("1000.00")


def test_find_nonexistent_account(bank):
    assert bank.find_account(999) is None


# ==========================================
# TESTS : VIREMENTS
# ==========================================

def test_successful_transfer(bank):
    bank.transfer(101, 202, "150.00")

    source = bank.find_account(101)
    destination = bank.find_account(202)

    assert source.Solde == Decimal("850.00")
    assert destination.Solde == Decimal("450.00")

    assert source.Logs[-1]["action"] == "transfer_out"
    assert destination.Logs[-1]["action"] == "transfer_in"


@pytest.mark.parametrize(
    "source_id,destination_id",
    [
        (999, 202),
        (101, 999),
        (999, 888),
    ]
)
def test_transfer_nonexistent_accounts(
    bank, source_id, destination_id
):
    with pytest.raises(ValueError):
        bank.transfer(source_id, destination_id, "100.00")

    assert bank.find_account(101).Solde == Decimal("1000.00")
    assert bank.find_account(202).Solde == Decimal("300.00")


def test_transfer_same_account(bank):
    with pytest.raises(ValueError):
        bank.transfer(101, 101, "100.00")

    assert bank.find_account(101).Solde == Decimal("1000.00")


@pytest.mark.parametrize(
    "amount",
    ["0", "-50", "NaN", "Infinity"]
)
def test_invalid_transfer_amount(bank, amount):
    with pytest.raises(ValueError):
        bank.transfer(101, 202, amount)

    assert bank.find_account(101).Solde == Decimal("1000.00")
    assert bank.find_account(202).Solde == Decimal("300.00")


def test_insufficient_funds(bank):
    with pytest.raises(ValueError, match="Insufficient funds"):
        bank.transfer(101, 202, "1500.00")

    assert bank.find_account(101).Solde == Decimal("1000.00")
    assert bank.find_account(202).Solde == Decimal("300.00")


# ==========================================
# TEST : COMPENSATION EN CAS D'ÉCHEC
# ==========================================

def test_transfer_refund_on_deposit_failure(bank, monkeypatch):
    source = bank.find_account(101)
    destination = bank.find_account(202)

    def failing_deposit(amount, transaction_type="deposit"):
        raise RuntimeError("Simulated deposit failure")

    monkeypatch.setattr(destination, "deposit", failing_deposit)

    with pytest.raises(RuntimeError, match="Simulated deposit failure"):
        bank.transfer(101, 202, "150.00")

    # Le retrait doit avoir été compensé.
    assert source.Solde == Decimal("1000.00")
    assert destination.Solde == Decimal("300.00")

    # La compensation doit être enregistrée.
    assert source.Logs[-1]["action"] == "transfer_refund"
    assert source.Logs[-1]["amount"] == Decimal("150.00")
