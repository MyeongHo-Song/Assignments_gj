"""
ui_helpers.py
Helper functions for user interface operations
"""
from accounts.base import BankAccount
from accounts.types import SavingAccount, TimeDepositAccount, OverdraftAccount


def create_account_with_input(bank):
    """Create account with user input"""
    print("\nSelect account type:")
    print("1. Normal Account")
    print("2. Saving Account") 
    print("3. Time Deposit Account")
    print("4. Overdraft Account")
    
    acc_type = input("Choice: ")
    username = input("Enter name: ")
    pw1 = input("Enter password: ")
    pw2 = input("Re-enter password: ")
    
    if pw1 != pw2:
        print("[Account Creation Error] Passwords do not match.")
        return None
    
    try:
        interest_rate = float(input("Enter interest rate (e.g., 0.05): "))
        
        if acc_type == '1':
            account = BankAccount(username, pw1, interest_rate)
        elif acc_type == '2':
            monthly = int(input("Monthly deposit amount: "))
            months = int(input("Saving period (months): "))
            account = SavingAccount(username, pw1, interest_rate, monthly, months)
        elif acc_type == '3':
            period = int(input("Deposit period (days): "))
            account = TimeDepositAccount(username, pw1, interest_rate, period)
        elif acc_type == '4':
            limit = int(input("Overdraft limit: "))
            account = OverdraftAccount(username, pw1, interest_rate, limit)
        else:
            print("[Account Creation Error] Invalid account type selection.")
            return None
        
        bank.create_account(account)
        print("Account created successfully!")
        account.show_account_info()
        return account
        
    except Exception as e:
        print(f"[Account Creation Error] {e}")
        return None


def select_account(bank):
    """Select account from bank"""
    accounts = bank.get_all_accounts()
    if not accounts:
        print("No accounts exist. Please create an account first.")
        return None
    
    print("\n=== Select Account ===")
    for i, acc in enumerate(accounts, 1):
        print(f"{i}. {acc.get_username()} - {acc.get_account_type()} (Account: {acc.get_account_number()})")
    
    choice = input("Enter account number or list number: ")
    
    # Try to find by account number
    try:
        acc_num = int(choice)
        account = bank.get_account_by_number(acc_num)
        if account:
            return account
    except ValueError:
        pass
    
    # Try list number
    try:
        list_num = int(choice)
        if 1 <= list_num <= len(accounts):
            return accounts[list_num - 1]
    except ValueError:
        pass
    
    print(f"Account not found.")
    return None


def handle_contract_termination(account, bank):
    """Handle contract account termination"""
    # Store account info
    username = account.get_username()
    password = account.get_password()
    interest_rate = account.get_interest_rate()
    
    # Get balance before termination
    balance_before = account.get_balance()
    
    # Process termination
    pw = input("Enter password: ")
    result = account.withdraw(0, pw)  # Withdraw triggers termination
    
    if result:
        # Calculate withdrawn amount
        withdrawn_amount = balance_before  # After termination, balance should be 0
        
        # Create new BankAccount
        new_account = BankAccount(username, password, interest_rate)
        bank.create_account(new_account)
        
        # Deposit the withdrawn amount
        new_account.deposit(withdrawn_amount)
        
        # Add termination transaction
        bank.add_transaction(
            account.get_account_number(),
            username,
            account.get_account_type(),
            withdrawn_amount,
            "Contract Termination"
        )
        
        # Remove old account
        bank.remove_account(account)
        
        print(f"\nContract account closed.")
        print(f"New BankAccount created with balance: {withdrawn_amount}")
        print(f"New account number: {new_account.get_account_number()}")
        
        return new_account
    
    return None


def show_main_menu():
    """Display main menu"""
    print("\n=== Main Menu ===")
    print("1. Create Account")
    print("2. Select Account")
    print("3. Show Bank Info")
    print("4. Show All Transactions")
    print("0. Exit")


def show_account_menu(account):
    """Display account-specific menu"""
    print(f"\n=== {account.get_username()}'s {account.get_account_type()} ===")
    
    if isinstance(account, (SavingAccount, TimeDepositAccount)):
        print("1. Deposit")
        print("2. Terminate/Maturity")
        print("3. Account Info")
        print("4. Transaction History")
        print("5. Back to Main Menu")
        print("0. Exit")
    else:
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Account Info") 
        print("4. Transaction History")
        print("5. Back to Main Menu")
        print("0. Exit")