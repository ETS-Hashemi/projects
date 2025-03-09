```markdown
# CS50P Investment Management System

#### Video Demo: <URL HERE>

#### Description:

I built this project as my final assignment for CS50P to practice Python programming and reinforce what I learned throughout the course. This Investment Management System is a text-based application that lets users create and manage multiple brokerage accounts, deposit or withdraw funds in different currencies, and buy or sell securities. It also generates a summary report of all accounts and their holdings. My goal was to create a project that would be both practical and relatively comprehensive, making use of classes, functions, error handling, and a textual user interface (TUI).

The application runs in the terminal and uses the `npyscreen` library to display menus, forms, and dialogs. I chose `npyscreen` because it provides a structured way to build text-based UIs without having to manage all the cursor movements and user input parsing manually. It also helps keep the application more user-friendly for those who run it directly in the command line.

## Project Files Overview

- **project.py**  
  This is the main file where all the logic resides. It contains several classes:
  1. **Holding**: Represents a single security holding, storing details such as security name, currency, the number of shares, average price, and the most recent market price.
  2. **BrokerageAccount**: Represents a single brokerage account with a name, account number, broker, cash balances in CAD and USD, and a collection of holdings. It supports depositing, withdrawing, buying shares, and selling shares.
  3. **Multiple Forms** (via `npyscreen`): These forms make up the text-based user interface. For instance, the `MainMenuForm` handles menu navigation, `AddAccountForm` creates new accounts, `DeleteAccountForm` removes accounts, `DepositWithdrawForm` manages cash transactions, `BuyForm` handles security purchases, `SellForm` handles security sales, and `ReportForm` displays account summaries.
  
  Within `project.py`, I also defined global lists and helper functions. There’s an `ALL_ACCOUNTS` list that stores every created account. Three helper functions—`total_cad_cash()`, `total_usd_cash()`, and `total_shares()`—accumulate data from all accounts to provide quick statistics if needed. Finally, there’s a `main()` function that initializes and launches the `npyscreen` application.

- **test_project.py**  
  In this file, I wrote tests for some of the core functions and logic. Specifically, I tested the behavior of depositing, withdrawing, buying, and selling. I also tested the helper functions like `total_cad_cash` to confirm they work as expected. Pytest helps automate these tests so I can easily ensure that future changes to the code won’t break existing features.

- **requirements.txt**  
  This file includes the external dependencies needed to run the project. The main dependency is `npyscreen` because that library is central to the text-based interface. If there are any other dependencies, they would also be listed here, ensuring anyone using my code can install them via `pip install -r requirements.txt`.

## Design Choices

1. **Object-Oriented Approach**: I decided to represent key entities (accounts and holdings) as classes. This keeps data organized and makes logic more straightforward to maintain. For instance, each `BrokerageAccount` object has its own methods for deposit, withdraw, and trading, ensuring a clear separation of concerns.

2. **npyscreen for TUI**: Instead of building a command-line-only system with manual prompts, I wanted a slightly richer text interface. `npyscreen` provided a way to create forms, button-based menus, and error popups, which made the application more user-friendly and reduced the risk of input errors or confusion.

3. **Validation**: I included several checks to ensure valid input, such as preventing negative deposits or withdrawals, enforcing non-empty account names, and disallowing the purchase of more shares than the available cash. These checks avoid unexpected states.

4. **Simplicity vs. Flexibility**: One trade-off I faced was whether to allow zero or fractional shares, negative amounts, or other edge cases. I decided to keep things simple, sticking to straightforward rules like “shares must be positive” or “you can’t sell more shares than you own.” That makes the code easier to follow but still covers most real-world scenarios.

## Usage

1. **Install dependencies**: Make sure to install required packages via `pip install -r requirements.txt`.
2. **Run the program**: Execute `python project.py` from your terminal. You’ll see a menu, and you can use arrow keys and the Enter key to make selections.
3. **Create an account**: In the main menu, choose “Create New Account” and enter the necessary information (account name, number, broker).
4. **Deposit or withdraw funds**: Select “Deposit or Withdraw” to manage cash balances in either CAD or USD.
5. **Buy or sell securities**: Use the “Buy Securities” and “Sell Securities” forms to manage holdings. If you try to buy or sell more shares than you can afford or have, the system will display an error popup.
6. **View report**: Check the “View Accounts Report” to see a summary of all your accounts, including their cash balances and holdings.