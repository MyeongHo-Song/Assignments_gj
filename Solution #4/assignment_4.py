"""
File Name: assignment_4.py
Created Date: 2025-07-07
Programmer: Kwanju Eun
Description: Bank system (Add input function and exception handling)
"""
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import random


# ----------------------
# Custom Exceptions
# ----------------------
class InvalidPasswordError(Exception):
    def __init__(self, message="Incorrect password provided"):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f"Password Error: {self.message}"

class InvalidAmountError(Exception):
    def __init__(self, message="Invalid amount provided"):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f"Amount Error: {self.message}"
    
    def get_error_type(self):
        return "AMOUNT_VALIDATION_ERROR"

class ContractValueError(Exception):
    def __init__(self, message="Contract operation failed"):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f"Contract Error: {self.message}"
    
    def is_contract_related(self):
        return True

# ----------------------
# Abstract BankAccount
# ----------------------
class BankAccount(ABC):
    used_account_numbers = set()

    def __init__(self, username, password, interest_rate):
        self.__username = username
        self.__password = password
        self.__bank_account_number = self.generate_unique_account_number()
        self.__interest_rate = interest_rate
        self.__balance = 0
        self.__created_date = datetime.now()
        self.__transaction_history = []

    def generate_unique_account_number(self):
        while True:
            account_number = random.randint(10000000, 99999999)
            if account_number not in BankAccount.used_account_numbers:
                BankAccount.used_account_numbers.add(account_number)
                return account_number

    def add_transaction(self, amount, transaction_type):
        transaction = Transaction(self, amount, transaction_type)
        self.__transaction_history.append(transaction)
        # Also add to bank's global transaction history if bank reference is available
        if hasattr(self, '_bank_reference') and self._bank_reference:
            self._bank_reference.add_transaction_to_history(transaction)
        return transaction

    def deposit(self, amount):
        try:
            if amount <= 0:
                raise InvalidAmountError("Deposit amount must be greater than 0.")
            self.__balance += amount
            self.add_transaction(amount, "Deposit")
            print(f"Deposit successful! Current balance: {self.__balance}")
        except InvalidAmountError as e:
            print(f"[{e.get_error_type()}] {e}")
        finally:
            print("[Deposit Process Finished]")

    def withdraw(self, amount, password):
        try:
            if password != self.__password:
                raise InvalidPasswordError("Incorrect password.")
            if amount <= 0:
                raise InvalidAmountError("Withdrawal amount must be greater than 0.")
            if self.__balance < amount:
                raise InvalidAmountError("Insufficient balance.")
            self.__balance -= amount
            self.add_transaction(amount, "Withdrawal")
            print(f"Withdrawal successful! Current balance: {self.__balance}")
        except (InvalidPasswordError, InvalidAmountError) as e:
            if isinstance(e, InvalidPasswordError):
                print(f"[PASSWORD_ERROR] {e}")
            elif isinstance(e, InvalidAmountError):
                print(f"[{e.get_error_type()}] {e}")
            else:
                print(f"[Withdrawal Error] {e}")
        finally:
            print("[Withdrawal Process Finished]")


    # Getter methods (strict encapsulation)
    def get_balance(self):
        return self.__balance
    def get_password(self):
        return self.__password
    def get_created_date(self):
        return self.__created_date
    def get_account_type(self):
        return self.__class__.__name__
    def get_username(self):
        return self.__username
    def get_interest_rate(self):
        return self.__interest_rate
    def get_account_number(self):
        return self.__bank_account_number
    def get_transaction_history(self):
        return self.__transaction_history
    def show_transaction_history(self):
        print(f"Transaction History for {self.__username}:")
        if not self.__transaction_history:
            print("No transactions found.")
        else:
            for i, transaction in enumerate(self.__transaction_history, 1):
                print(f"{i}. {transaction.get_transaction_type()}: {transaction.get_amount()} at {transaction.get_transaction_date()}")
        print()
    def show_account_info(self):
        print(f"Name: {self.__username}")
        print(f"Account type: {self.get_account_type()}")
        print(f"Interest rate: {self.__interest_rate}")
        print(f"Balance: {self.__balance}")
        print(f"Created date: {self.__created_date}")
        print(f"Bank account number: {self.__bank_account_number}")

# ----------------------
# Transaction
# ----------------------
class Transaction:
    def __init__(self, account, amount, transaction_type):
        self.__account = account
        self.__amount = amount
        self.__transaction_type = transaction_type
        self.__transaction_date = datetime.now()
        self.__account_number = account.get_account_number()
        self.__username = account.get_username()
        self.__account_type = account.get_account_type()
    
    def get_amount(self):
        return self.__amount
    def get_transaction_type(self):
        return self.__transaction_type
    def get_transaction_date(self):
        return self.__transaction_date
    def get_account_number(self):
        return self.__account_number
    def get_username(self):
        return self.__username
    def get_account_type(self):
        return self.__account_type
    def show_transaction_info(self):
        print(f"Transaction type: {self.__transaction_type}")
        print(f"Transaction amount: {self.__amount}")
        print(f"Transaction date: {self.__transaction_date}")
        print(f"Account: {self.__username} ({self.__account_type}) - {self.__account_number}")
        if hasattr(self.__account, 'get_balance'):
            print(f"Account balance: {self.__account.get_balance()}")

# ----------------------
# SavingAccount
# ----------------------
class SavingAccount(BankAccount):
    def __init__(self, username, password, interest_rate, monthly_amount, contract_months):
        super().__init__(username, password, interest_rate)
        self.__monthly_amount = monthly_amount
        self.__contract_months = contract_months
        self.__contract_end_date = self.get_created_date() + timedelta(days=contract_months * 30)
        self.__total_deposited = 0
        self.__is_terminated = False
        self.__is_matured = False

    def deposit(self, amount):
        try:
            # SavingAccount only allows monthly_amount deposit
            if amount != self.__monthly_amount:
                raise InvalidAmountError(f"SavingAccount: Only monthly amount ({self.__monthly_amount}) is allowed.")
            if self.__is_terminated or self.__is_matured:
                raise ContractValueError("Contract is terminated or matured. Cannot deposit.")
            current_date = datetime.now()
            if current_date > self.__contract_end_date:
                raise ContractValueError("Contract period has ended. Cannot deposit.")
            self.__total_deposited += self.__monthly_amount
            # Use parent class deposit method
            super().deposit(self.__monthly_amount)
            return True
        except (InvalidAmountError, ContractValueError) as e:
            print(f"[{e.get_error_type()}] {e}")
            return False
        finally:
            print("[Deposit Process Finished]")

    def withdraw(self, amount, password):
        try:
            if password != self.get_password():
                raise InvalidPasswordError("Incorrect password.")
            
            # SavingAccount has special withdraw conditions
            if self.__is_terminated or self.__is_matured:
                raise ContractValueError("Contract is already terminated or matured.")
            
            current_date = datetime.now()
            if current_date < self.__contract_end_date:
                # Within contract period: early termination (reduced interest)
                reduced_rate = self.get_interest_rate() * 0.1
                interest = self.__total_deposited * reduced_rate * (self.__contract_months / 12)
                total_amount = self.__total_deposited + interest
                self.__is_terminated = True
                print("Contract terminated early.")
                print(f"Total deposited: {self.__total_deposited}")
                print(f"Interest earned (reduced rate): {interest}")
                print(f"Total amount available: {total_amount}")
                # Use parent class withdraw method
                super().withdraw(total_amount, password)
                return True
            else:
                # Contract expired: maturity termination (full interest)
                interest = self.__total_deposited * self.get_interest_rate() * (self.__contract_months / 12)
                total_amount = self.__total_deposited + interest
                self.__is_matured = True
                print("Contract matured successfully!")
                print(f"Total deposited: {self.__total_deposited}")
                print(f"Interest earned (full rate): {interest}")
                print(f"Total amount available: {total_amount}")
                # Use parent class withdraw method
                super().withdraw(total_amount, password)
                return True
                
        except (InvalidPasswordError, ContractValueError) as e:
            if isinstance(e, InvalidPasswordError):
                print(f"[PASSWORD_ERROR] {e}")
            elif isinstance(e, ContractValueError):
                print(f"[CONTRACT_ERROR] {e}")
            else:
                print(f"[Withdraw Error] {e}")
            return False
        finally:
            print("[Withdraw Process Finished]")

    def show_account_info(self):
        super().show_account_info()
        print(f"Monthly deposit amount: {self.__monthly_amount}")
        print(f"Contract period: {self.__contract_months} months")
        print(f"Contract end date: {self.__contract_end_date}")
        print(f"Total deposited: {self.__total_deposited}")

# ----------------------
# TimeDepositAccount
# ----------------------
class TimeDepositAccount(BankAccount):
    def __init__(self, username, password, interest_rate, deposit_period=365):
        super().__init__(username, password, interest_rate)
        self.__deposit_period = deposit_period
        self.__contract_end_date = self.get_created_date() + timedelta(days=deposit_period)
        self.__is_terminated = False
        self.__is_matured = False

    def deposit(self, amount):
        try:
            # TimeDepositAccount only allows one-time deposit
            if self.get_balance() > 0:
                raise InvalidAmountError("TimeDepositAccount: Only one-time deposit allowed.")
            # Use parent class deposit method
            super().deposit(amount)
            return True
        except InvalidAmountError as e:
            print(f"[{e.get_error_type()}] {e}")
            return False
        finally:
            print("[Deposit Process Finished]")

    def withdraw(self, amount, password):
        try:
            if password != self.get_password():
                raise InvalidPasswordError("Incorrect password.")
            
            # TimeDepositAccount has special withdraw conditions
            if self.__is_terminated or self.__is_matured:
                raise ContractValueError("Contract is already terminated or matured.")
            
            current_date = datetime.now()
            if current_date < self.__contract_end_date:
                # Within contract period: early termination (reduced interest)
                reduced_rate = self.get_interest_rate() * 0.1
                interest = self.get_balance() * reduced_rate * (self.__deposit_period / 365)
                total_amount = self.get_balance() + interest
                self.__is_terminated = True
                print("Contract terminated early.")
                print(f"Original deposit: {self.get_balance()}")
                print(f"Interest earned (reduced rate): {interest}")
                print(f"Total amount available: {total_amount}")
                # Use parent class withdraw method
                super().withdraw(total_amount, password)
                return True
            else:
                # Contract expired: maturity termination (full interest)
                interest = self.get_balance() * self.get_interest_rate() * (self.__deposit_period / 365)
                total_amount = self.get_balance() + interest
                self.__is_matured = True
                print("Contract matured successfully!")
                print(f"Original deposit: {self.get_balance()}")
                print(f"Interest earned (full rate): {interest}")
                print(f"Total amount available: {total_amount}")
                # Use parent class withdraw method
                super().withdraw(total_amount, password)
                return True
                
        except (InvalidPasswordError, ContractValueError) as e:
            if isinstance(e, InvalidPasswordError):
                print(f"[PASSWORD_ERROR] {e}")
            elif isinstance(e, ContractValueError):
                print(f"[CONTRACT_ERROR] {e}")
            else:
                print(f"[Withdraw Error] {e}")
            return False
        finally:
            print("[Withdraw Process Finished]")

    def show_account_info(self):
        super().show_account_info()
        print(f"Deposit period: {self.__deposit_period} days")
        print(f"Contract end date: {self.__contract_end_date}")

# ----------------------
# OverdraftAccount
# ----------------------
class OverdraftAccount(BankAccount):
    def __init__(self, username, password, interest_rate, overdraft_limit=500000):
        super().__init__(username, password, interest_rate)
        self.__overdraft_limit = overdraft_limit

    def withdraw(self, amount, password):
        try:
            if password != self.get_password():
                raise InvalidPasswordError("Incorrect password.")
            if amount <= 0:
                raise InvalidAmountError("Withdrawal amount must be greater than 0.")
            # OverdraftAccount has additional condition: overdraft limit check
            if self.get_balance() - amount < -self.__overdraft_limit:
                raise InvalidAmountError(f"Exceeded limit. Maximum negative limit: {self.__overdraft_limit}")
            # Directly implement withdraw logic (balance update)
            self._BankAccount__balance -= amount
            self.add_transaction(amount, "Withdrawal")
            print(f"Withdraw {amount} success. Current balance: {self.get_balance()}")
            return True
        except (InvalidPasswordError, InvalidAmountError) as e:
            if isinstance(e, InvalidPasswordError):
                print(f"[PASSWORD_ERROR] {e}")
            elif isinstance(e, InvalidAmountError):
                print(f"[{e.get_error_type()}] {e}")
            else:
                print(f"[Withdraw Error] {e}")
            return False
        finally:
            print("[Withdraw Process Finished]")

    def show_account_info(self):
        super().show_account_info()
        print(f"Overdraft limit: {self.__overdraft_limit}")
        print(f"Available overdraft: {self.__overdraft_limit + self.get_balance()}")

# ----------------------
# NormalAccount
# ----------------------
class NormalAccount(BankAccount):
    # NormalAccount uses all methods from parent class directly
    pass

# ----------------------
# Bank Class
# ----------------------
class Bank:
    def __init__(self):
        self.accounts = []
        self.account_numbers = set()
        self.total_amount = 0
        self.max_overdraft = 0
        self.all_transactions = []  # Store all transactions from all accounts

    def add_transaction_to_history(self, transaction):
        """Add transaction to bank's global transaction history"""
        self.all_transactions.append(transaction)

    def get_transactions_by_account_number(self, account_number):
        """Get all transactions for a specific account number"""
        return [t for t in self.all_transactions if t.get_account_number() == account_number]

    def get_transactions_by_username(self, username):
        """Get all transactions for a specific username"""
        return [t for t in self.all_transactions if t.get_username() == username]

    def update_total_amount(self):
        """Update total amount in bank by summing all account balances"""
        self.total_amount = sum(acc.get_balance() for acc in self.accounts)

    def update_max_overdraft(self):
        """Update maximum overdraft amount"""
        overdraft_accounts = [acc for acc in self.accounts if isinstance(acc, OverdraftAccount)]
        if overdraft_accounts:
            self.max_overdraft = sum(acc._OverdraftAccount__overdraft_limit for acc in overdraft_accounts)
        else:
            self.max_overdraft = 0

    def create_account_with_input(self):
        print("Select account type: 1. Normal 2. Saving 3. TimeDeposit 4. Overdraft")
        acc_type = input("Choice: ")
        username = input("Enter name: ")
        pw1 = input("Enter password: ")
        pw2 = input("Re-enter password: ")
        if pw1 != pw2:
            print("[Account Creation Error] Passwords do not match.")
            return None
        try:
            ir = float(input("Enter interest rate (e.g., 0.05): "))
            if acc_type == '1':
                acc = NormalAccount(username, pw1, ir)
            elif acc_type == '2':
                monthly = int(input("Monthly deposit amount: "))
                months = int(input("Saving period (months): "))
                acc = SavingAccount(username, pw1, ir, monthly, months)
            elif acc_type == '3':
                period = int(input("Deposit period (days): "))
                acc = TimeDepositAccount(username, pw1, ir, period)
            elif acc_type == '4':
                limit = int(input("Overdraft limit: "))
                acc = OverdraftAccount(username, pw1, ir, limit)
            else:
                print("[Account Creation Error] Invalid account type selection.")
                return None
            
            # Set bank reference for transaction tracking
            acc._bank_reference = self
            
            self.accounts.append(acc)
            self.update_total_amount()
            self.update_max_overdraft()
            print("Account created successfully!")
            acc.show_account_info()
            return acc
        except Exception as e:
            print(f"[Account Creation Error] {e}")
            return None

    def show_all_accounts(self):
        self.update_total_amount()
        self.update_max_overdraft()
        print("\n=== All Accounts in Bank ===")
        for acc in self.accounts:
            acc.show_account_info()
            print("--------------------------")
        print(f"Total amount in bank: {self.total_amount}")
        print(f"Max overdraft allowed: {self.max_overdraft}")

# ----------------------
# Helper functions
# ----------------------
def select_account(bank):
    """Helper function to select an account"""
    if not bank.accounts:
        print("No accounts exist. Please create an account first.")
        return None
    
    print("\n=== Select Account ===")
    for i, acc in enumerate(bank.accounts, 1):
        print(f"{i}. {acc.get_username()} - {acc.get_account_type()} (Account: {acc.get_account_number()})")
    
    choice = input("Enter account number or list number: ")
    
    # Try to find by account number first
    for acc in bank.accounts:
        if str(acc.get_account_number()) == choice:
            return acc
    
    # If not found by account number, try list number
    try:
        list_num = int(choice)
        if 1 <= list_num <= len(bank.accounts):
            return bank.accounts[list_num - 1]
    except ValueError:
        pass
    
    print(f"Account not found. Please enter a valid account number or list number (1-{len(bank.accounts)}).")
    return None

def handle_deposit(account, bank):
    """Helper function to handle deposit"""
    try:
        amount = int(input("Deposit amount: "))
        account.deposit(amount)
        bank.update_total_amount()
    except Exception as e:
        print(f"[Deposit Error] {e}")

def handle_withdraw(account, bank):
    """Helper function to handle withdraw/terminate"""
    if hasattr(account, '_SavingAccount__contract_end_date') or hasattr(account, '_TimeDepositAccount__contract_end_date'):
        # Contract-based accounts: terminate/maturity
        try:
            pw = input("Enter password: ")
            print("- Processing contract termination/maturity:")
            
            # Store account info before termination
            username = account.get_username()
            password = account.get_password()
            interest_rate = account.get_interest_rate()
            
            # Process termination/maturity
            result = account.withdraw(0, pw)
            bank.update_total_amount()
            
            if result:
                # Get the withdrawn amount (total amount after termination)
                withdrawn_amount = 0
                if hasattr(account, '_SavingAccount__total_deposited'):
                    # SavingAccount: calculate total amount
                    if account._SavingAccount__is_terminated:
                        reduced_rate = account.get_interest_rate() * 0.1
                        interest = account._SavingAccount__total_deposited * reduced_rate * (account._SavingAccount__contract_months / 12)
                        withdrawn_amount = account._SavingAccount__total_deposited + interest
                    elif account._SavingAccount__is_matured:
                        interest = account._SavingAccount__total_deposited * account.get_interest_rate() * (account._SavingAccount__contract_months / 12)
                        withdrawn_amount = account._SavingAccount__total_deposited + interest
                elif hasattr(account, '_TimeDepositAccount__deposit_period'):
                    # TimeDepositAccount: calculate total amount
                    if account._TimeDepositAccount__is_terminated:
                        reduced_rate = account.get_interest_rate() * 0.1
                        interest = account.get_balance() * reduced_rate * (account._TimeDepositAccount__deposit_period / 365)
                        withdrawn_amount = account.get_balance() + interest
                    elif account._TimeDepositAccount__is_matured:
                        interest = account.get_balance() * account.get_interest_rate() * (account._TimeDepositAccount__deposit_period / 365)
                        withdrawn_amount = account.get_balance() + interest
                
                if withdrawn_amount > 0:
                    # Create new NormalAccount with withdrawn amount
                    new_account = NormalAccount(username, password, interest_rate)
                    new_account._bank_reference = bank  # Set bank reference
                    new_account.deposit(withdrawn_amount)
                    bank.accounts.append(new_account)
                    bank.update_total_amount()
                    
                    # Add contract termination transaction to global history
                    termination_transaction = Transaction(account, withdrawn_amount, "Contract Termination")
                    bank.add_transaction_to_history(termination_transaction)
                    
                    # Remove the old contract account
                    bank.accounts.remove(account)
                    
                    print(f"Contract account closed. New NormalAccount created with {withdrawn_amount}.")
                    print(f"New account number: {new_account.get_account_number()}")
                    print("Transaction history has been preserved.")
                    
                    # Return to main menu to select new account
                    return "new_account_created"
            
        except Exception as e:
            print(f"[Contract Error] {e}")
    else:
        # Normal accounts: regular withdraw
        try:
            amount = int(input("Withdrawal amount: "))
            pw = input("Enter password: ")
            account.withdraw(amount, pw)
            bank.update_total_amount()
        except Exception as e:
            print(f"[Withdrawal Error] {e}")
    
    return None

def show_main_menu():
    """Helper function to show main menu"""
    print("\n1. Create Account  2. Select Account  3. Show Bank Info  4. Show All Transactions  0. Exit")

def show_account_menu(account):
    """Helper function to show account menu"""
    print(f"\n=== {account.get_username()}'s {account.get_account_type()} ===")
    if hasattr(account, '_SavingAccount__contract_end_date') or hasattr(account, '_TimeDepositAccount__contract_end_date'):
        print("1. Deposit  2. Terminate/Maturity  3. Account Info  4. Transaction History  5. Back to Main Menu  0. Exit")
    else:
        print("1. Deposit  2. Withdraw  3. Account Info  4. Transaction History  5. Back to Main Menu  0. Exit")

# Main loop
if __name__ == "__main__":
    bank = Bank()
    selected_acc = None
    
    while True:
        if selected_acc is None:
            # Main menu
            show_main_menu()
            sel = input("Choice: ")
            
            if sel == '1':
                acc = bank.create_account_with_input()
                if acc:
                    print("Account created successfully!")
            elif sel == '2':
                selected_acc = select_account(bank)
                if selected_acc:
                    print(f"Selected: {selected_acc.get_username()}'s {selected_acc.get_account_type()}")
            elif sel == '3':
                bank.show_all_accounts()
            elif sel == '4':
                if not bank.accounts and not bank.all_transactions:
                    print("No accounts or transactions exist. Please create an account first.")
                    continue
                print("\n=== All Transactions ===")
                
                # Show transactions by username (including closed accounts)
                usernames = set()
                for acc in bank.accounts:
                    usernames.add(acc.get_username())
                for transaction in bank.all_transactions:
                    usernames.add(transaction.get_username())
                
                for username in sorted(usernames):
                    print(f"\n--- {username} ---")
                    user_transactions = bank.get_transactions_by_username(username)
                    if user_transactions:
                        for i, transaction in enumerate(user_transactions, 1):
                            print(f"{i}. {transaction.get_transaction_type()}: {transaction.get_amount()} at {transaction.get_transaction_date()}")
                            print(f"   Account: {transaction.get_account_type()} - {transaction.get_account_number()}")
                    else:
                        print("No transactions found.")
            elif sel == '0':
                print("Exiting.")
                break
            else:
                print("Invalid choice.")
        else:
            # Account menu
            show_account_menu(selected_acc)
            sel = input("Choice: ")
            
            if sel == '1':
                handle_deposit(selected_acc, bank)
            elif sel == '2':
                result = handle_withdraw(selected_acc, bank)
                if result == "new_account_created":
                    selected_acc = None  # Return to main menu
                    print("Please select your new account from the main menu.")
            elif sel == '3':
                selected_acc.show_account_info()
            elif sel == '4':
                if hasattr(selected_acc, 'show_transaction_history'):
                    selected_acc.show_transaction_history()
                else:
                    print("No transaction history available.")
            elif sel == '5':
                selected_acc = None
                print("Returned to main menu.")
            elif sel == '0':
                print("Exiting.")
                break
            else:
                print("Invalid choice.")