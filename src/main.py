
from decimal import Decimal, InvalidOperation

from Bank import Bank
from Client import Client
from BankAccount import CurrentAccount, SavingAccount


def read_id(message):
    try:
        value = int(input(message))
        if value <= 0:
            raise ValueError
        return value
    except ValueError:
        print("ID must be a positive integer.")
        return None


def read_amount(message, allow_zero=False):
    try:
        amount = Decimal(input(message).strip())

        if not amount.is_finite():
            raise ValueError

        if amount < 0 or (amount == 0 and not allow_zero):
            raise ValueError

        return amount

    except (InvalidOperation, ValueError):
        print("Invalid amount.")
        return None


def create_client(bank):
    print("\n--- CREATE CLIENT ---")

    client_id = read_id("Client ID: ")
    if client_id is None:
        return

    if bank.find_client(client_id) is not None:
        print("Client already exists.")
        return

    first_name = input("First name: ").strip()
    last_name = input("Last name: ").strip()

    if not first_name or not last_name:
        print("First name and last name are required.")
        return

    client = Client(client_id, first_name, last_name)
    bank.add_client(client)

    print("Client created successfully!")


def create_account(bank):
    print("\n--- CREATE ACCOUNT ---")

    client_id = read_id("Client ID: ")
    if client_id is None:
        return

    client = bank.find_client(client_id)

    if client is None:
        print("Client not found.")
        return

    account_id = read_id("Account ID: ")
    if account_id is None:
        return

    if bank.find_account(account_id) is not None:
        print("Account ID already exists.")
        return

    print("1. Current Account")
    print("2. Savings Account")

    account_type = input("Choose account type: ").strip()

    if account_type not in ("1", "2"):
        print("Invalid account type.")
        return

    balance = read_amount("Initial balance: ", allow_zero=True)
    if balance is None:
        return

    if account_type == "1":
        account = CurrentAccount(account_id, balance)

    else:
        rate_percent = read_amount(
            "Annual interest rate (%): ",
            allow_zero=True
        )
        if rate_percent is None or rate_percent > 100:
            print("Interest rate must be between 0 and 100%.")
            return

        rate = rate_percent / Decimal("100")
        account = SavingAccount(account_id, balance, str(rate))

    client.add_account(account)
    print("Account created successfully!")


def show_clients(bank):
    print("\n--- CLIENTS ---")
    bank.show_client()


def show_client_accounts(bank):
    print("\n--- CLIENT ACCOUNTS ---")

    client_id = read_id("Client ID: ")
    if client_id is None:
        return

    client = bank.find_client(client_id)

    if client is None:
        print("Client not found.")
        return

    if not client.Accounts:
        print("This client has no accounts.")
        return

    print(f"\nClient: {client.first_name} {client.last_name}")
    client.show_account()


def deposit_money(bank):
    print("\n--- DEPOSIT MONEY ---")

    account_id = read_id("Account ID: ")
    if account_id is None:
        return

    account = bank.find_account(account_id)

    if account is None:
        print("Account not found.")
        return

    amount = read_amount("Amount to deposit: ")
    if amount is None:
        return

    try:
        account.deposit(amount)
        print(f"Deposit successful! New balance: {account.Solde}")
    except ValueError as error:
        print(f"Error: {error}")


def withdraw_money(bank):
    print("\n--- WITHDRAW MONEY ---")

    account_id = read_id("Account ID: ")
    if account_id is None:
        return

    account = bank.find_account(account_id)

    if account is None:
        print("Account not found.")
        return

    amount = read_amount("Amount to withdraw: ")
    if amount is None:
        return

    try:
        account.withdraw(amount)
        print(f"Withdrawal successful! New balance: {account.Solde}")
    except ValueError as error:
        print(f"Error: {error}")


def transfer_money(bank):
    print("\n--- TRANSFER MONEY ---")

    source_id = read_id("Source account ID: ")
    if source_id is None:
        return

    destination_id = read_id("Destination account ID: ")
    if destination_id is None:
        return

    amount = read_amount("Amount to transfer: ")
    if amount is None:
        return

    try:
        bank.transfer(source_id, destination_id, amount)
        print("Transfer completed successfully!")
    except ValueError as error:
        print(f"Transfer failed: {error}")
    except Exception as error:
        print(f"Transfer failed unexpectedly: {error}")


def apply_savings_interest(bank):
    print("\n--- APPLY SAVINGS INTEREST ---")

    account_id = read_id("Savings account ID: ")
    if account_id is None:
        return

    account = bank.find_account(account_id)

    if account is None:
        print("Account not found.")
        return

    if not isinstance(account, SavingAccount):
        print("This is not a savings account.")
        return

    interest = account.apply_interest()

    print(f"Interest applied: {interest}")
    print(f"New balance: {account.Solde}")


def view_transaction_history(bank):
    print("\n--- TRANSACTION HISTORY ---")

    account_id = read_id("Account ID: ")
    if account_id is None:
        return

    account = bank.find_account(account_id)

    if account is None:
        print("Account not found.")
        return

    logs = account.Logs

    if not logs:
        print("No transactions found.")
        return

    for index, transaction in enumerate(logs, start=1):
        print(
            f"{index}. "
            f"{transaction['Date']} "
            f"{transaction['time']} | "
            f"{transaction['action']} | "
            f"{transaction['amount']}"
        )


def display_menu():
    print("\n========== SMARTBANK ==========")
    print("1. Create a client")
    print("2. Create a bank account")
    print("3. Show clients")
    print("4. Show client accounts")
    print("5. Deposit money")
    print("6. Withdraw money")
    print("7. Transfer money")
    print("8. Apply savings interest")
    print("9. View transaction history")
    print("0. Exit")


def main():
    bank = Bank()

    actions = {
        "1": create_client,
        "2": create_account,
        "3": show_clients,
        "4": show_client_accounts,
        "5": deposit_money,
        "6": withdraw_money,
        "7": transfer_money,
        "8": apply_savings_interest,
        "9": view_transaction_history,
    }

    while True:
        display_menu()
        choice = input("\nChoose an option: ").strip()

        if choice == "0":
            print("Thank you for using SmartBank. Goodbye!")
            break

        action = actions.get(choice)

        if action is None:
            print("Invalid option. Please try again.")
            continue

        try:
            action(bank)
        except (ValueError, InvalidOperation) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
