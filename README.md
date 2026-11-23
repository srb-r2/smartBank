# SmartBank — Python Banking Simulator

A command-line banking simulator built with **Python**, designed to demonstrate object-oriented programming, financial transaction management, input validation, exception handling, and automated testing.

SmartBank allows users to manage clients, create bank accounts, perform financial operations, calculate savings interest, and review transaction histories through an interactive command-line interface (CLI).

This project was developed as a hands-on learning exercise to strengthen Python software engineering fundamentals and build a maintainable, testable application.

## Features

### Client Management
- Register new clients with unique IDs.
- Prevent duplicate client registrations.
- Search for existing clients.
- Display registered clients and their accounts.
- Support client removal when no accounts remain.

### Bank Account Management
- Create current accounts and savings accounts.
- Associate multiple accounts with a client.
- Prevent duplicate account IDs through the CLI.
- Track balances using Python's `Decimal` module.
- Validate deposits, withdrawals, and initial balances.

### Financial Transactions
- Deposit and withdraw money.
- Transfer funds between bank accounts.
- Reject transfers with insufficient funds.
- Prevent transfers between identical accounts.
- Attempt to compensate the source account if a destination deposit fails.
- Record transactions with timestamps and operation types.

### Savings Accounts
- Configure an annual interest rate.
- Calculate interest without changing the account balance.
- Apply interest to the account balance.
- Record interest payments in the transaction history.

### Interactive CLI
- Menu-driven navigation.
- Input validation and error messages.
- Access to balances and transaction histories.
- Multiple banking operations during a single application session.

## Technologies

| Technology | Purpose |
|---|---|
| Python 3.13 | Application development |
| Python OOP | Classes, inheritance, encapsulation, composition |
| Decimal | Precise decimal calculations |
| datetime | Transaction timestamps |
| zoneinfo / tzdata | Timezone-aware timestamps |
| pytest | Automated unit and CLI testing |
| Git & GitHub | Version control and development workflow |

## Project Architecture

SmartBank follows an object-oriented design that separates banking operations, client management, and user interaction.

### `BankAccount`

The base class responsible for common account functionality.

Responsibilities:
- Store the account identifier and balance.
- Handle deposits and withdrawals.
- Validate financial operations.
- Maintain a transaction history.

### `CurrentAccount`

Inherits from `BankAccount` and provides standard account functionality without duplicating its implementation.

### `SavingAccount`

Inherits from `BankAccount` and introduces savings-specific functionality.

Additional responsibilities:
- Store an interest rate.
- Calculate interest.
- Apply interest to the balance.

### `Client`

Represents an individual bank customer.

Responsibilities:
- Store client information.
- Maintain a collection of associated accounts.
- Add, remove, and display accounts.
- Prevent duplicate account identifiers within the client's account collection.

### `Bank`

Coordinates banking operations across registered clients.

Responsibilities:
- Register, search, and remove clients.
- Locate accounts across clients.
- Validate and execute transfers.
- Handle transfer failures through compensating operations.

### `main.py`

Provides the user-facing command-line interface.

Responsibilities:
- Display the application menu.
- Collect and validate user inputs.
- Call the appropriate domain methods.
- Display operation results and errors.

## Project Structure

```text
smartBank/
├── src/
│   ├── __init__.py
│   ├── Bank.py
│   ├── BankAccount.py
│   ├── Client.py
│   └── main.py
│
├── tests/
│   ├── test_bank.py
│   ├── test_bank_account.py
│   ├── test_client.py
│   └── test_main.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

*The structure above reflects the intended organization of the project.*

## Installation

### Prerequisites

- Python 3.13 or a compatible Python 3 version
- Git
- pip

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/smartbank-python.git
cd smartbank-python
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

Activation is optional. On Windows, the virtual environment's interpreter can also be called directly using `.venv\Scripts\python.exe`.

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

The dependency file should include:

```text
pytest
tzdata
```

`tzdata` provides timezone data for environments that do not have a system timezone database, including some Windows installations.

## Running the Application

From the project root:

```bash
python -m src.main
```

The application displays the following menu:

```text
========== SMARTBANK ==========

1. Create a client
2. Create a bank account
3. Show clients
4. Show client accounts
5. Deposit money
6. Withdraw money
7. Transfer money
8. Apply savings interest
9. View transaction history
0. Exit
```

Select an option and follow the prompts.

## Example Usage

### Create a Client

```text
Choose an option: 1

Client ID: 101
First name: sara
Last name: elle

Client created successfully!
```

### Create a Current Account

```text
Choose an option: 2

Client ID: 101
Account ID: 1001

1. Current Account
2. Savings Account

Choose account type: 1
Initial balance: 1000.00

Account created successfully!
```

### Deposit Money

```text
Choose an option: 5

Account ID: 1001
Amount to deposit: 250.00

Deposit successful!
New balance: 1250.00
```

### Transfer Money

```text
Choose an option: 7

Source account ID: 1001
Destination account ID: 2001
Amount to transfer: 150.00

Transfer completed successfully!
```

The operation updates both account balances and records the corresponding transactions.

## Financial Precision

SmartBank uses Python's `Decimal` module instead of binary floating-point arithmetic for monetary calculations.

Example:

```python
from decimal import Decimal

balance = Decimal("1000.00")
deposit = Decimal("150.75")

new_balance = balance + deposit

print(new_balance)  # 1150.75
```

Using decimal arithmetic avoids common binary floating-point representation issues.

The project is an educational simulation and does not implement all financial precision, concurrency, or regulatory safeguards required by production banking systems.

## Transaction History

Each account maintains an in-memory history of financial operations.

A transaction includes:

- Date
- Time
- Operation type
- Amount

Supported operation types include:

| Operation | Description |
|---|---|
| `deposit` | Money deposited |
| `withdraw` | Money withdrawn |
| `transfer_out` | Outgoing transfer |
| `transfer_in` | Incoming transfer |
| `transfer_refund` | Compensation after a failed transfer |
| `interest` | Savings interest credited |

Transaction timestamps use the `America/Toronto` timezone.

## Automated Testing

SmartBank uses **pytest** to validate banking operations and user interactions.

Tests cover:

- Account initialization and balance validation
- Deposits and withdrawals
- Invalid transaction amounts
- Insufficient funds
- Inheritance and savings interest calculations
- Client registration and duplicate prevention
- Account and client lookup
- Successful and unsuccessful transfers
- Transfer compensation behavior
- CLI input handling and menu navigation

The tests also demonstrate:

- `pytest.fixture` for reusable test data
- `pytest.mark.parametrize` for multiple input scenarios
- `pytest.raises` for exception testing
- `monkeypatch` for simulating user input and operation failures

### Run All Tests

From the project root:

```bash
python -m pytest -v
```

### Run CLI Tests Only

```bash
python -m pytest tests/test_main.py -v
```

All automated tests were passing at the time of the project's final CLI testing.

## Object-Oriented Programming Concepts

This project demonstrates several fundamental OOP principles.

**Encapsulation:** Private attributes protect account balances, identifiers, and internal collections.

**Inheritance:** `CurrentAccount` and `SavingAccount` reuse functionality from the `BankAccount` base class.

**Polymorphism:** Different account subclasses can be handled through the shared `BankAccount` interface.

**Composition:** A `Bank` manages clients, while each `Client` manages a collection of bank accounts.

**Separation of concerns:** Banking logic is implemented in domain classes, while user interaction is handled by the CLI.

## Error Handling

SmartBank validates operations before modifying account balances.

Examples of rejected operations include:

- Negative initial balances
- Zero or negative transaction amounts
- Withdrawals exceeding the available balance
- Transfers involving nonexistent accounts
- Transfers between the same account
- Duplicate client identifiers
- Invalid CLI input

Errors are managed through Python exceptions and user-facing messages.

For transfer failures, the application implements a basic compensating operation that attempts to refund the source account if the destination deposit raises an exception.

This is **not a fully atomic transaction system** and should not be used for real financial operations.

## Limitations

SmartBank is an educational project with the following limitations:

- Data is stored in memory and is lost when the application closes.
- There is no database or persistent transaction storage.
- There is no user authentication or authorization.
- There is no graphical user interface.
- Transfers are not protected by database-level transactions.
- Concurrent financial operations are not supported.
- Account ID uniqueness is enforced by the CLI, not by a centralized account registration service.
- Savings interest is applied manually and does not use an automated accrual schedule.

## Possible Future Improvements

Potential enhancements include:

- SQLite or PostgreSQL integration
- Persistent client and transaction storage
- REST API development with FastAPI
- User authentication
- Automated savings interest accrual
- Improved transaction atomicity
- Docker containerization
- Continuous integration with GitHub Actions

These are potential extensions, not features of the current application.

## Development Workflow

This project was developed using Git and a feature-branch workflow.

The main banking models and unit tests were committed to `main`, while the interactive CLI was developed separately on `feature/cli-menu`.

The project emphasizes incremental development, code review, automated testing, and separation of responsibilities.

## Learning Outcomes

Building SmartBank provided practical experience in:

- Designing relationships between Python classes
- Applying object-oriented principles
- Implementing financial business rules
- Handling errors and validating data
- Writing automated tests
- Organizing a multi-module Python project
- Building command-line interfaces
- Managing development through Git branches and commits

## Disclaimer

**SmartBank is a fictional banking simulator developed exclusively for educational purposes.**

It does not interact with real banks, process real payments, store real customer financial information, or provide production-grade financial security.


**Focus:** Python · Object-Oriented Programming · Software Engineering · Automated Testing