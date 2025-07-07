"""
File Name: assignment_3.py
Created Date: 2025-07-01
Programmer: Kwanju Eun
Description: Bank system (strict encapsulation, matches class diagram, test for savings, time deposit, and overdraft accounts)
"""
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import random

# ----------------------
# Abstract BankAccount
# ----------------------
class BankAccount(ABC):
    used_account_numbers = set()

    def __init__(self, username, password, interest_rate):
        self.__username = username
        self.__password = password
        self.__bank_account_number = self._generate_unique_account_number()
        self.__interest_rate = interest_rate
        self.__balance = 0
        self.__created_date = datetime.now()
        self.__transaction_history = []

    def _generate_unique_account_number(self):
        while True:
            account_number = random.randint(10000000, 99999999)
            if account_number not in BankAccount.used_account_numbers:
                BankAccount.used_account_numbers.add(account_number)
                return account_number

    def add_transaction(self, amount, transaction_type):
        transaction = Transaction(self, amount, transaction_type)
        self.__transaction_history.append(transaction)
        return transaction

    def deposit(self, amount):
        if amount <= 0:
            print("Invalid amount")
            return False
        self.__balance += amount
        self.add_transaction(amount, "Deposit")
        print(f"Deposit {amount} success. Current balance: {self.__balance}")
        return True

    def withdraw(self, amount, password):
        if password != self.__password:
            print("Invalid password")
            return False
        if amount <= 0:
            print("Invalid amount")
            return False
        if self.__balance >= amount:
            self.__balance -= amount
            self.add_transaction(amount, "Withdrawal")
            print(f"Withdraw {amount} success. Current balance: {self.__balance}")
            return True
        else:
            print("Insufficient balance")
            return False

    @abstractmethod
    def check_maturity(self, password):
        pass

    @abstractmethod
    def terminate_contract(self, password):
        pass

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
        print(f"Username: {self.__username}")
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
    def get_amount(self):
        return self.__amount
    def get_transaction_type(self):
        return self.__transaction_type
    def get_transaction_date(self):
        return self.__transaction_date
    def show_transaction_info(self):
        print(f"Transaction type: {self.__transaction_type}")
        print(f"Transaction amount: {self.__amount}")
        print(f"Transaction date: {self.__transaction_date}")
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
        print("SavingAccount: Use monthly_deposit() instead of direct deposit.")
        return False

    def monthly_deposit(self, password):
        if password != self.get_password():
            print("Invalid password")
            return False
        if self.__is_terminated or self.__is_matured:
            print("Contract has been terminated or matured. Cannot make deposits.")
            return False
        current_date = datetime.now()
        if current_date > self.__contract_end_date:
            print("Contract period has ended. Cannot make monthly deposits.")
            return False
        self.__total_deposited += self.__monthly_amount
        return super().deposit(self.__monthly_amount)

    def withdraw(self, amount, password):
        print("Saving accounts do not support direct withdrawal. Use terminate_contract() or check_maturity().")
        return False

    def terminate_contract(self, password):
        if password != self.get_password():
            print("Invalid password")
            return False
        if self.__is_terminated or self.__is_matured:
            print("Contract is already terminated or matured.")
            return False
        current_date = datetime.now()
        if current_date >= self.__contract_end_date:
            print("Contract period has already ended. Use check_maturity() instead.")
            return False
        reduced_rate = self.get_interest_rate() * 0.1
        interest = self.__total_deposited * reduced_rate * (self.__contract_months / 12)
        total_amount = self.__total_deposited + interest
        self.__is_terminated = True
        print(f"Total deposited: {self.__total_deposited}")
        print(f"Interest earned (reduced rate): {interest}")
        print(f"Total amount available: {total_amount}")
        return total_amount

    def check_maturity(self, password):
        if password != self.get_password():
            print("Invalid password")
            return False
        if self.__is_terminated or self.__is_matured:
            print("Contract is already terminated or matured.")
            return False
        current_date = datetime.now()
        if current_date < self.__contract_end_date:
            remaining_days = (self.__contract_end_date - current_date).days
            print(f"Contract has not matured yet. {remaining_days} days remaining.")
            return False
        interest = self.__total_deposited * self.get_interest_rate() * (self.__contract_months / 12)
        total_amount = self.__total_deposited + interest
        self.__is_matured = True
        print(f"Contract matured successfully!")
        print(f"Total deposited: {self.__total_deposited}")
        print(f"Interest earned (full rate): {interest}")
        print(f"Total amount available: {total_amount}")
        return total_amount

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
        if self.get_balance() > 0:
            print("TimeDepositAccount: Only one-time deposit allowed.")
            return False
        return super().deposit(amount)

    def withdraw(self, amount, password):
        print("Time deposit accounts do not support direct withdrawal. Use terminate_contract() or check_maturity().")
        return False

    def terminate_contract(self, password):
        if password != self.get_password():
            print("Invalid password")
            return False
        if self.__is_terminated or self.__is_matured:
            print("Contract is already terminated or matured.")
            return False
        current_date = datetime.now()
        if current_date >= self.__contract_end_date:
            print("Contract period has already ended. Use check_maturity() instead.")
            return False
        reduced_rate = self.get_interest_rate() * 0.1
        interest = self.get_balance() * reduced_rate * (self.__deposit_period / 365)
        total_amount = self.get_balance() + interest
        self.__is_terminated = True
        print(f"Contract terminated early.")
        print(f"Original deposit: {self.get_balance()}")
        print(f"Interest earned (reduced rate): {interest}")
        print(f"Total amount available: {total_amount}")
        return total_amount

    def check_maturity(self, password):
        if password != self.get_password():
            print("Invalid password")
            return False
        if self.__is_terminated or self.__is_matured:
            print("Contract is already terminated or matured.")
            return False
        current_date = datetime.now()
        if current_date < self.__contract_end_date:
            remaining_days = (self.__contract_end_date - current_date).days
            print(f"Contract has not matured yet. {remaining_days} days remaining.")
            return False
        interest = self.get_balance() * self.get_interest_rate() * (self.__deposit_period / 365)
        total_amount = self.get_balance() + interest
        self.__is_matured = True
        print(f"Contract matured successfully!")
        print(f"Original deposit: {self.get_balance()}")
        print(f"Interest earned (full rate): {interest}")
        print(f"Total amount available: {total_amount}")
        return total_amount

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
        if password != self.get_password():
            print("Invalid password")
            return False
        if amount <= 0:
            print("Invalid amount")
            return False
        if self.get_balance() - amount >= -self.__overdraft_limit:
            # Directly access parent's __balance
            self._BankAccount__balance -= amount
            self.add_transaction(amount, "Withdrawal")
            print(f"Withdraw {amount} success. Current balance: {self.get_balance()}")
            return True
        else:
            print(f"Insufficient balance. Overdraft limit is {self.__overdraft_limit}")
            return False

    def terminate_contract(self, password):
        print("Overdraft accounts do not support contract termination.")
        return False

    def check_maturity(self, password):
        print("Overdraft accounts do not have maturity.")
        return False

    def show_account_info(self):
        super().show_account_info()
        print(f"Overdraft limit: {self.__overdraft_limit}")
        print(f"Available overdraft: {self.__overdraft_limit + self.get_balance()}")

# ----------------------
# Bank Class
# ----------------------
class Bank:
    def __init__(self):
        self.accounts = []
        self.account_numbers = set()
        self.total_amount = 0
        self.max_overdraft = 0

    def register_bank_account(self, username, password, interest_rate, account_type, *args):
        if account_type == 'Saving':
            if len(args) != 2:
                print("SavingAccount requires monthly_amount and contract_months.")
                return None
            acc = SavingAccount(username, password, interest_rate, args[0], args[1])
        elif account_type == 'TimeDeposit':
            if len(args) != 1:
                print("TimeDepositAccount requires deposit_period.")
                return None
            acc = TimeDepositAccount(username, password, interest_rate, args[0])
        elif account_type == 'Overdraft':
            if len(args) != 1:
                print("OverdraftAccount requires overdraft_limit.")
                return None
            acc = OverdraftAccount(username, password, interest_rate, args[0])
            self.max_overdraft += args[0]
        else:
            print("Unknown account type.")
            return None
        if acc.get_account_number() in self.account_numbers:
            print("Account number already exists.")
            return None
        self.accounts.append(acc)
        self.account_numbers.add(acc.get_account_number())
        self.total_amount += acc.get_balance()
        print(f"Account registered: {acc.get_account_type()} #{acc.get_account_number()}")
        return acc

    def show_all_accounts(self):
        print("\n=== All Accounts in Bank ===")
        for acc in self.accounts:
            acc.show_account_info()
            print("--------------------------")
        print(f"Total amount in bank: {self.total_amount}")
        print(f"Max overdraft allowed: {self.max_overdraft}")

# ----------------------
# Example Usage
# ----------------------
if __name__ == "__main__":
    bank = Bank()
    print("\n[Savings Account Test]")
    saving = bank.register_bank_account("Alice", "pw1", 0.05, 'Saving', 100000, 12)
    if saving:
        for i in range(3):
            print(f"- {i+1}th monthly deposit:")
            saving.monthly_deposit("pw1")
        saving.show_account_info()
        print("- Early termination test:")
        saving.terminate_contract("pw1")
        print("- Maturity check test:")
        saving.check_maturity("pw1")
        print("- Direct withdrawal attempt:")
        saving.withdraw(10000, "pw1")
    print("\n[Time Deposit Account Test]")
    timed = bank.register_bank_account("Bob", "pw2", 0.06, 'TimeDeposit', 365)
    if timed:
        print("- Deposit:")
        timed.deposit(500000)
        timed.show_account_info()
        print("- Early termination test:")
        timed.terminate_contract("pw2")
        print("- Maturity check test:")
        timed.check_maturity("pw2")
        print("- Direct withdrawal attempt:")
        timed.withdraw(10000, "pw2")
    print("\n[Overdraft Account Test]")
    overdraft = bank.register_bank_account("Charlie", "pw3", 0.015, 'Overdraft', 300000)
    if overdraft:
        print("- Deposit:")
        overdraft.deposit(100000)
        print("- Withdrawal within limit:")
        overdraft.withdraw(350000, "pw3")
        print("- Withdrawal exceeding limit:")
        overdraft.withdraw(100000, "pw3")
        overdraft.show_account_info()
        print("- Maturity/termination attempt:")
        overdraft.terminate_contract("pw3")
        overdraft.check_maturity("pw3")
    print("\n[All Accounts Information]")
    bank.show_all_accounts()