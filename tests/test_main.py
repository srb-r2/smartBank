"""Tests for the SmartBank command-line interface.
"""

from BankAccount import CurrentAccount, SavingAccount
from Client import Client
from Bank import Bank
import main as cli
from pathlib import Path
from decimal import Decimal
import builtins
import pytest


def enter(monkeypatch, *answers):
    """Simulate successive calls to input()."""
    responses = iter(answers)
    monkeypatch.setattr(builtins, "input", lambda _prompt="": next(responses))


@pytest.fixture
def bank():
    bank = Bank()
    alice = Client(1, "Asma", "Roujaina")
    bob = Client(2, "Sarah", "Martin")
    alice.add_account(CurrentAccount(101, "1000.00"))
    bob.add_account(SavingAccount(202, "300.00", "0.05"))
    bank.add_client(alice)
    bank.add_client(bob)
    return bank


# Input validation
@pytest.mark.parametrize("answer", ["abc", "0", "-5"])
def test_read_id_rejects_invalid_input(monkeypatch, capsys, answer):
    enter(monkeypatch, answer)
    assert cli.read_id("ID: ") is None
    assert "positive integer" in capsys.readouterr().out


def test_read_amount_rejects_nan(monkeypatch):
    enter(monkeypatch, "NaN")
    assert cli.read_amount("Amount: ") is None


def test_read_amount_accepts_decimal(monkeypatch):
    enter(monkeypatch, "150.75")
    assert cli.read_amount("Amount: ") == Decimal("150.75")


# Clients

def test_create_client(monkeypatch):
    bank = Bank()
    enter(monkeypatch, "3", "John", "Smith")
    cli.create_client(bank)
    client = bank.find_client(3)
    assert client is not None
    assert client.first_name == "John"
    assert client.last_name == "Smith"


def test_create_client_duplicate(monkeypatch, bank, capsys):
    enter(monkeypatch, "1")
    cli.create_client(bank)
    assert "already exists" in capsys.readouterr().out
    assert bank.find_client(1).first_name == "Asma"


def test_create_client_empty_name(monkeypatch, capsys):
    bank = Bank()
    enter(monkeypatch, "3", "   ", "Smith")
    cli.create_client(bank)
    assert bank.find_client(3) is None
    assert "required" in capsys.readouterr().out


# Accounts

def test_create_current_account(monkeypatch, bank):
    enter(monkeypatch, "1", "303", "1", "250.50")
    cli.create_account(bank)
    account = bank.find_account(303)
    assert isinstance(account, CurrentAccount)
    assert account.Solde == Decimal("250.50")


def test_create_savings_account(monkeypatch, bank):
    enter(monkeypatch, "2", "404", "2", "500", "5")
    cli.create_account(bank)
    account = bank.find_account(404)
    assert isinstance(account, SavingAccount)
    assert account.Interest_rate == Decimal("0.05")


def test_create_account_rejects_duplicate(monkeypatch, bank, capsys):
    enter(monkeypatch, "1", "202")
    cli.create_account(bank)
    assert "already exists" in capsys.readouterr().out


def test_create_account_rejects_unknown_client(monkeypatch, bank, capsys):
    enter(monkeypatch, "999")
    cli.create_account(bank)
    assert "not found" in capsys.readouterr().out


# Transactions

def test_deposit_money(monkeypatch, bank):
    enter(monkeypatch, "101", "125.50")
    cli.deposit_money(bank)
    assert bank.find_account(101).Solde == Decimal("1125.50")


def test_withdraw_money(monkeypatch, bank):
    enter(monkeypatch, "101", "100")
    cli.withdraw_money(bank)
    assert bank.find_account(101).Solde == Decimal("900.00")


def test_withdraw_money_insufficient_funds(monkeypatch, bank, capsys):
    enter(monkeypatch, "101", "5000")
    cli.withdraw_money(bank)
    assert bank.find_account(101).Solde == Decimal("1000.00")
    assert "Error:" in capsys.readouterr().out


def test_transfer_money(monkeypatch, bank):
    enter(monkeypatch, "101", "202", "150")
    cli.transfer_money(bank)
    assert bank.find_account(101).Solde == Decimal("850.00")
    assert bank.find_account(202).Solde == Decimal("450.00")


def test_apply_savings_interest(monkeypatch, bank):
    enter(monkeypatch, "202")
    cli.apply_savings_interest(bank)
    assert bank.find_account(202).Solde == Decimal("315.00")


def test_reject_interest_on_current_account(monkeypatch, bank, capsys):
    enter(monkeypatch, "101")
    cli.apply_savings_interest(bank)
    assert "not a savings account" in capsys.readouterr().out


def test_transaction_history(monkeypatch, bank, capsys):
    bank.find_account(101).deposit("12.00")
    enter(monkeypatch, "101")
    cli.view_transaction_history(bank)
    output = capsys.readouterr().out
    assert "deposit" in output
    assert "12.00" in output


def test_show_client_accounts(monkeypatch, bank, capsys):
    enter(monkeypatch, "1")
    cli.show_client_accounts(bank)
    output = capsys.readouterr().out
    assert "Asma" in output
    assert "101" in output


# Entire main loop

def test_main_creates_client_and_exits(monkeypatch, capsys):
    enter(monkeypatch, "1", "7", "Alex", "Doe", "0")
    cli.main()
    output = capsys.readouterr().out
    assert "Client created successfully!" in output
    assert "Goodbye!" in output


def test_main_rejects_unknown_choice_and_exits(monkeypatch, capsys):
    enter(monkeypatch, "99", "0")
    cli.main()
    output = capsys.readouterr().out
    assert "Invalid option" in output
    assert "Goodbye!" in output
