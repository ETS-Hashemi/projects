import npyscreen
import re

# -------------------------
#     DATA MODELS
# -------------------------
class Holding:
    """
    Stores details about a single security, including:
    - security (e.g., AAPL, TSLA)
    - currency ('CAD' or 'USD')
    - shares (number of units held)
    - avg_price (average cost basis)
    - market_price (the most recent price)
    """
    def __init__(self, security, currency, shares, purchase_price):
        self.security = security
        self.currency = currency
        self.shares = shares
        self.avg_price = purchase_price
        self.market_price = purchase_price

    def update_avg_price(self, new_shares, new_price):
        # Calculate a weighted average cost when buying more shares
        total_shares = self.shares + new_shares
        if total_shares == 0:
            self.avg_price = 0.0
        else:
            cost_old = self.shares * self.avg_price
            cost_new = new_shares * new_price
            self.avg_price = (cost_old + cost_new) / total_shares

        self.shares = total_shares
        self.market_price = new_price

    def sell_shares(self, amount_to_sell, sell_price):
        # Ensure we have enough shares to sell
        if amount_to_sell > self.shares:
            raise ValueError("Not enough shares to sell.")
        self.shares -= amount_to_sell
        self.market_price = sell_price


class BrokerageAccount:
    """
    Represents a brokerage account that includes:
    - name: a label for the account
    - account_number: a string containing digits, dashes, and spaces
    - broker: the name of the brokerage
    - cash: a dictionary storing CAD and USD balances
    - holdings: a list of Holding objects
    """
    def __init__(self, name, account_number, broker):
        self.name = self._validate_name(name)
        self.account_number = self._validate_account_number(account_number)
        self.broker = broker
        self.cash = {"CAD": 0.0, "USD": 0.0}
        self.holdings = []

    def _validate_name(self, name):
        if not name.strip():
            raise ValueError("Account name can't be empty.")
        return name

    def _validate_account_number(self, acct_num):
        pattern = r'^[0-9 \-]+$'
        if not re.match(pattern, acct_num):
            raise ValueError("Account number can only have digits, dashes, or spaces.")
        return acct_num

    def deposit(self, amount, currency):
        if amount < 0:
            raise ValueError("Cannot deposit a negative amount.")
        self.cash[currency] += amount

    def withdraw(self, amount, currency):
        if amount < 0:
            raise ValueError("Cannot withdraw a negative amount.")
        if amount > self.cash[currency]:
            raise ValueError(f"Insufficient {currency} funds.")
        self.cash[currency] -= amount

    def _find_holding(self, security, currency):
        for item in self.holdings:
            if item.security == security and item.currency == currency:
                return item
        return None

    def buy_security(self, security, currency, shares, purchase_price):
        if shares <= 0:
            raise ValueError("Number of shares to buy must be positive.")
        total_cost = shares * purchase_price
        if total_cost > self.cash[currency]:
            raise ValueError(f"Not enough {currency} balance for this purchase.")
        self.cash[currency] -= total_cost

        existing_holding = self._find_holding(security, currency)
        if existing_holding:
            existing_holding.update_avg_price(shares, purchase_price)
        else:
            new_holding = Holding(security, currency, shares, purchase_price)
            self.holdings.append(new_holding)

    def sell_security(self, security, currency, shares, sell_price):
        if shares <= 0:
            raise ValueError("Number of shares to sell must be positive.")
        existing_holding = self._find_holding(security, currency)
        if not existing_holding:
            raise ValueError(f"No holding found for {security} in {currency}.")
        existing_holding.sell_shares(shares, sell_price)
        proceeds = shares * sell_price
        self.cash[currency] += proceeds
        # Remove the holding if all shares are sold
        if existing_holding.shares == 0:
            self.holdings.remove(existing_holding)


# -------------------------
#   GLOBAL STORAGE
# -------------------------
ALL_ACCOUNTS = []


# -------------------------
#    HELPER FUNCTIONS
# -------------------------
def total_cad_cash():
    """
    Returns the sum of all CAD balances across every account in ALL_ACCOUNTS.
    """
    total = 0
    for acct in ALL_ACCOUNTS:
        total += acct.cash["CAD"]
    return total


def total_usd_cash():
    """
    Returns the sum of all USD balances across every account in ALL_ACCOUNTS.
    """
    total = 0
    for acct in ALL_ACCOUNTS:
        total += acct.cash["USD"]
    return total


def total_shares():
    """
    Returns the combined number of shares of all securities across all accounts.
    """
    grand_total = 0
    for acct in ALL_ACCOUNTS:
        for h in acct.holdings:
            grand_total += h.shares
    return grand_total


# -------------------------
#       NPYSCREEN FORMS
# -------------------------
class MainMenuForm(npyscreen.FormBaseNew):
    """
    This is the primary menu for the program.
    """
    def create(self):
        max_y, max_x = self.useable_space()

        banner_line_1 = "CS50P Final Project"
        banner_line_2 = "Investment Manager"
        banner_line_3 = "by: Seyed Masoud Hashemi Ahmadi"

        center_x_1 = int((max_x - len(banner_line_1)) / 2)
        center_x_2 = int((max_x - len(banner_line_2)) / 2)
        center_x_3 = int((max_x - len(banner_line_3)) / 2)

        self.add(npyscreen.FixedText, value=banner_line_1, relx=center_x_1, rely=1, editable=False, color='STANDOUT')
        self.add(npyscreen.FixedText, value=banner_line_2, relx=center_x_2, rely=2, editable=False)
        self.add(npyscreen.FixedText, value=banner_line_3, relx=center_x_3, rely=3, editable=False)

        self.nextrely = 5

        self.add(npyscreen.TitleFixedText, name="Main Menu Options", value="")

        # Keyboard shortcut to exit
        self.add_handlers({"^Q": self.exit_app})

        self.btn_add = self.add(npyscreen.ButtonPress, name="Create New Account", when_pressed_function=self.goto_add)
        self.btn_delete = self.add(npyscreen.ButtonPress, name="Delete Existing Account", when_pressed_function=self.goto_delete)
        self.btn_deposit = self.add(npyscreen.ButtonPress, name="Deposit or Withdraw", when_pressed_function=self.goto_deposit_withdraw)
        self.btn_buy = self.add(npyscreen.ButtonPress, name="Buy Securities", when_pressed_function=self.goto_buy)
        self.btn_sell = self.add(npyscreen.ButtonPress, name="Sell Securities", when_pressed_function=self.goto_sell)
        self.btn_report = self.add(npyscreen.ButtonPress, name="View Accounts Report", when_pressed_function=self.goto_report)
        self.btn_exit = self.add(npyscreen.ButtonPress, name="Exit Program", when_pressed_function=self.exit_app)

    def goto_add(self):
        self.parentApp.switchForm("ADD_ACCOUNT")

    def goto_delete(self):
        self.parentApp.switchForm("DELETE_ACCOUNT")

    def goto_deposit_withdraw(self):
        self.parentApp.switchForm("DEPOSIT_WITHDRAW")

    def goto_buy(self):
        self.parentApp.switchForm("BUY_FORM")

    def goto_sell(self):
        self.parentApp.switchForm("SELL_FORM")

    def goto_report(self):
        self.parentApp.switchForm("REPORT_FORM")

    def exit_app(self, *args, **kwargs):
        self.parentApp.setNextForm(None)
        self.parentApp.switchFormNow()


class AddAccountForm(npyscreen.ActionForm):
    """
    Lets the user create a new brokerage account.
    """
    def create(self):
        self.field_name = self.add(npyscreen.TitleText, name="Account Name:")
        self.field_acct_number = self.add(npyscreen.TitleText, name="Account Number:")
        self.field_broker = self.add(npyscreen.TitleText, name="Broker:")

    def on_ok(self):
        try:
            new_acct = BrokerageAccount(
                name=self.field_name.value,
                account_number=self.field_acct_number.value,
                broker=self.field_broker.value
            )
            ALL_ACCOUNTS.append(new_acct)
            npyscreen.notify_confirm("Account created successfully!", title="Success")
            self.parentApp.switchForm("MAIN")
        except ValueError as err:
            npyscreen.notify_confirm(str(err), title="Error")

    def on_cancel(self):
        self.parentApp.switchForm("MAIN")


class DeleteAccountForm(npyscreen.ActionForm):
    """
    Displays a list of accounts and allows deletion of the selected one.
    """
    def create(self):
        self.select_account = self.add(
            npyscreen.TitleSelectOne,
            name="Choose an Account to Remove",
            max_height=5,
            scroll_exit=True
        )

    def beforeEditing(self):
        self.select_account.values = [
            f"{idx} - {acct.name} ({acct.account_number})"
            for idx, acct in enumerate(ALL_ACCOUNTS)
        ]
        self.select_account.value = None

    def on_ok(self):
        if self.select_account.value is not None:
            idx_to_remove = self.select_account.value[0]
            deleted_acct = ALL_ACCOUNTS.pop(idx_to_remove)
            npyscreen.notify_confirm(
                f"Removed: {deleted_acct.name} ({deleted_acct.account_number})",
                title="Account Deleted"
            )
        self.parentApp.switchForm("MAIN")

    def on_cancel(self):
        self.parentApp.switchForm("MAIN")


class DepositWithdrawForm(npyscreen.ActionForm):
    """
    Allows the user to deposit or withdraw funds in a particular currency.
    """
    def create(self):
        self.select_account = self.add(
            npyscreen.TitleSelectOne,
            name="Select an Account",
            max_height=5,
            scroll_exit=True
        )
        self.select_currency = self.add(
            npyscreen.TitleSelectOne,
            name="Currency Type",
            values=["CAD", "USD"],
            max_height=2,
            scroll_exit=True
        )
        self.select_action = self.add(
            npyscreen.TitleSelectOne,
            name="Action",
            values=["Deposit", "Withdraw"],
            max_height=2,
            scroll_exit=True
        )
        self.field_amount = self.add(npyscreen.TitleText, name="Amount:")

    def beforeEditing(self):
        self.select_account.values = [
            f"{idx} - {acct.name} ({acct.account_number})"
            for idx, acct in enumerate(ALL_ACCOUNTS)
        ]
        self.select_account.value = None
        self.select_currency.value = [0]  # default to "CAD"
        self.select_action.value = [0]    # default to "Deposit"
        self.field_amount.value = ""

    def on_ok(self):
        if self.select_account.value is None:
            npyscreen.notify_confirm("Please pick an account first.", title="Error")
            return
        chosen_index = self.select_account.value[0]
        acct = ALL_ACCOUNTS[chosen_index]
        chosen_currency = self.select_currency.values[self.select_currency.value[0]]
        chosen_action = self.select_action.values[self.select_action.value[0]]

        try:
            amt = float(self.field_amount.value)
        except ValueError:
            npyscreen.notify_confirm("Please enter a valid numeric amount.", title="Error")
            return

        try:
            if chosen_action == "Deposit":
                acct.deposit(amt, chosen_currency)
            else:
                acct.withdraw(amt, chosen_currency)
            npyscreen.notify_confirm("Transaction successful!", title="Success")
            self.parentApp.switchForm("MAIN")
        except ValueError as err:
            npyscreen.notify_confirm(str(err), title="Error")

    def on_cancel(self):
        self.parentApp.switchForm("MAIN")


class BuyForm(npyscreen.ActionForm):
    """
    Form to buy shares of a particular security in an account.
    """
    def create(self):
        self.select_account = self.add(
            npyscreen.TitleSelectOne,
            name="Select an Account",
            max_height=5,
            scroll_exit=True
        )
        self.field_security = self.add(npyscreen.TitleText, name="Security:")
        self.select_currency = self.add(
            npyscreen.TitleSelectOne,
            name="Currency",
            values=["CAD", "USD"],
            max_height=2,
            scroll_exit=True
        )
        self.field_shares = self.add(npyscreen.TitleText, name="Number of Shares:")
        self.field_price = self.add(npyscreen.TitleText, name="Purchase Price:")

    def beforeEditing(self):
        self.select_account.values = [
            f"{idx} - {acct.name} ({acct.account_number})"
            for idx, acct in enumerate(ALL_ACCOUNTS)
        ]
        self.select_account.value = None
        self.select_currency.value = [0]
        self.field_security.value = ""
        self.field_shares.value = ""
        self.field_price.value = ""

    def on_ok(self):
        if self.select_account.value is None:
            npyscreen.notify_confirm("Please select an account.", title="Error")
            return
        chosen_index = self.select_account.value[0]
        acct = ALL_ACCOUNTS[chosen_index]

        security_name = self.field_security.value.strip()
        if not security_name:
            npyscreen.notify_confirm("Security cannot be empty.", title="Error")
            return

        try:
            share_count = float(self.field_shares.value)
            buy_price = float(self.field_price.value)
        except ValueError:
            npyscreen.notify_confirm("Shares and Price must be numeric.", title="Error")
            return

        currency_used = self.select_currency.values[self.select_currency.value[0]]

        try:
            acct.buy_security(security_name, currency_used, share_count, buy_price)
            npyscreen.notify_confirm("Purchase completed!", title="Success")
            self.parentApp.switchForm("MAIN")
        except ValueError as err:
            npyscreen.notify_confirm(str(err), title="Error")

    def on_cancel(self):
        self.parentApp.switchForm("MAIN")


class SellForm(npyscreen.ActionForm):
    """
    Form to sell shares of a particular security from an account.
    """
    def create(self):
        self.select_account = self.add(
            npyscreen.TitleSelectOne,
            name="Select an Account",
            max_height=5,
            scroll_exit=True
        )
        self.field_security = self.add(npyscreen.TitleText, name="Security:")
        self.select_currency = self.add(
            npyscreen.TitleSelectOne,
            name="Currency",
            values=["CAD", "USD"],
            max_height=2,
            scroll_exit=True
        )
        self.field_shares = self.add(npyscreen.TitleText, name="Number of Shares:")
        self.field_price = self.add(npyscreen.TitleText, name="Sell Price:")

    def beforeEditing(self):
        self.select_account.values = [
            f"{idx} - {acct.name} ({acct.account_number})"
            for idx, acct in enumerate(ALL_ACCOUNTS)
        ]
        self.select_account.value = None
        self.select_currency.value = [0]
        self.field_security.value = ""
        self.field_shares.value = ""
        self.field_price.value = ""

    def on_ok(self):
        if self.select_account.value is None:
            npyscreen.notify_confirm("Please choose an account.", title="Error")
            return
        chosen_index = self.select_account.value[0]
        acct = ALL_ACCOUNTS[chosen_index]

        security_name = self.field_security.value.strip()
        if not security_name:
            npyscreen.notify_confirm("Security cannot be empty.", title="Error")
            return

        try:
            share_count = float(self.field_shares.value)
            sell_price = float(self.field_price.value)
        except ValueError:
            npyscreen.notify_confirm("Shares and Price must be numeric.", title="Error")
            return

        currency_used = self.select_currency.values[self.select_currency.value[0]]

        try:
            acct.sell_security(security_name, currency_used, share_count, sell_price)
            npyscreen.notify_confirm("Sale completed!", title="Success")
            self.parentApp.switchForm("MAIN")
        except ValueError as err:
            npyscreen.notify_confirm(str(err), title="Error")

    def on_cancel(self):
        self.parentApp.switchForm("MAIN")


class ReportForm(npyscreen.ActionForm):
    """
    Displays a summary of all accounts and their holdings.
    """
    def create(self):
        self.report_area = self.add(npyscreen.Pager, name="Accounts Overview", max_height=18)

    def beforeEditing(self):
        lines = ["=== Overall Accounts Report ===\n"]
        if not ALL_ACCOUNTS:
            lines.append("No accounts have been created yet.\n")
        else:
            for idx, acct in enumerate(ALL_ACCOUNTS, start=1):
                lines.append(f"Account {idx}: {acct.name} ({acct.account_number}) - Broker: {acct.broker}")
                lines.append(f"  CAD Cash: {acct.cash['CAD']:.2f}")
                lines.append(f"  USD Cash: {acct.cash['USD']:.2f}")

                cad_positions = [h for h in acct.holdings if h.currency == "CAD"]
                usd_positions = [h for h in acct.holdings if h.currency == "USD"]

                if cad_positions:
                    lines.append("  -- CAD Holdings --")
                    for h in cad_positions:
                        lines.append(f"     {h.security}: {h.shares} shares (avg {h.avg_price:.2f}, current {h.market_price:.2f})")
                if usd_positions:
                    lines.append("  -- USD Holdings --")
                    for h in usd_positions:
                        lines.append(f"     {h.security}: {h.shares} shares (avg {h.avg_price:.2f}, current {h.market_price:.2f})")

                lines.append("")  # extra line for readability
        self.report_area.values = lines

    def on_ok(self):
        self.parentApp.switchForm("MAIN")

    def on_cancel(self):
        self.parentApp.switchForm("MAIN")


# -------------------------
#       APP & MAIN
# -------------------------
class InvestmentApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", MainMenuForm, name="Main Menu")
        self.addForm("ADD_ACCOUNT", AddAccountForm, name="Add a New Account")
        self.addForm("DELETE_ACCOUNT", DeleteAccountForm, name="Remove an Account")
        self.addForm("DEPOSIT_WITHDRAW", DepositWithdrawForm, name="Deposit/Withdraw")
        self.addForm("BUY_FORM", BuyForm, name="Buy Securities")
        self.addForm("SELL_FORM", SellForm, name="Sell Securities")
        self.addForm("REPORT_FORM", ReportForm, name="Accounts Summary")


def main():
    """
    Main function to launch the text-based interface.
    """
    app = InvestmentApp()
    app.run()


if __name__ == "__main__":
    main()
