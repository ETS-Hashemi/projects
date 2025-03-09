import pytest
from project import (
    total_cad_cash,
    total_usd_cash,
    total_shares,
    BrokerageAccount,
    ALL_ACCOUNTS
)

def test_total_cad_cash():
    # Clear any existing accounts to ensure a clean test environment
    ALL_ACCOUNTS.clear()

    # Create first account and deposit some CAD
    acc1 = BrokerageAccount("Account1", "123-456", "BrokerA")
    acc1.deposit(500, "CAD")  # deposit CAD 500
    ALL_ACCOUNTS.append(acc1)

    # Create second account and deposit some CAD
    acc2 = BrokerageAccount("Account2", "789-012", "BrokerB")
    acc2.deposit(300, "CAD")  # deposit CAD 300
    ALL_ACCOUNTS.append(acc2)

    # Now, total CAD cash should be 800
    assert total_cad_cash() == 800, f"Expected 800, got {total_cad_cash()}"

def test_total_usd_cash():
    # Clear previous data
    ALL_ACCOUNTS.clear()

    # Create one account with USD deposit
    acc1 = BrokerageAccount("AccountA", "111-222", "BrokerC")
    acc1.deposit(250, "USD")
    ALL_ACCOUNTS.append(acc1)

    # Create another account with USD deposit
    acc2 = BrokerageAccount("AccountB", "333-444", "BrokerD")
    acc2.deposit(750, "USD")
    ALL_ACCOUNTS.append(acc2)

    # total_usd_cash should now be 1000
    assert total_usd_cash() == 1000, f"Expected 1000, got {total_usd_cash()}"

def test_total_shares():
    # Clear previous data
    ALL_ACCOUNTS.clear()

    # Create an account and buy some securities
    acc1 = BrokerageAccount("Holder1", "555-666", "BrokerE")
    acc1.deposit(1000, "CAD")
    acc1.buy_security("ABC", "CAD", 5, 50)  # 5 shares of "ABC"
    ALL_ACCOUNTS.append(acc1)

    # Create another account and buy more securities
    acc2 = BrokerageAccount("Holder2", "777-888", "BrokerF")
    acc2.deposit(2000, "CAD")
    acc2.buy_security("XYZ", "CAD", 10, 100)  # 10 shares of "XYZ"
    ALL_ACCOUNTS.append(acc2)

    # total_shares should be 5 + 10 = 15
    assert total_shares() == 15, f"Expected 15, got {total_shares()}"
