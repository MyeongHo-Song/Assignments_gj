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
    pass
class InvalidAmountError(Exception):
    pass
class ContractValueError(Exception):
    pass

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
        return transaction

    def deposit(self, amount):
        try:
            if amount <= 0:
                raise InvalidAmountError("Deposit amount must be greater than 0.")
            self.__balance += amount
            self.add_transaction(amount, "Deposit")
            print(f"Deposit successful! Current balance: {self.__balance}")
        except InvalidAmountError as e:
            print(f"[Deposit Error] {e}")
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
            print(f"[Withdrawal Error] {e}")
        finally:
            print("[Withdrawal Process Finished]")

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
        try:
            if password != self.get_password():
                raise InvalidPasswordError("Incorrect password.")
            if self.__is_terminated or self.__is_matured:
                raise ContractValueError("Contract is terminated or matured. Cannot deposit.")
            current_date = datetime.now()
            if current_date > self.__contract_end_date:
                raise ContractValueError("Contract period has ended. Cannot deposit.")
            self.__total_deposited += self.__monthly_amount
            return super().deposit(self.__monthly_amount)
        except (InvalidPasswordError, ContractValueError) as e:
            print(f"[Monthly Deposit Error] {e}")
            return False
        finally:
            print("[Monthly Deposit Process Finished]")

    def withdraw(self, amount, password):
        print("Saving accounts do not support direct withdrawal. Use terminate_contract() or check_maturity().")
        return False

    def terminate_contract(self, password):
        try:
            if password != self.get_password():
                raise InvalidPasswordError("Incorrect password.")
            if self.__is_terminated or self.__is_matured:
                raise ContractValueError("Contract is already terminated or matured.")
            current_date = datetime.now()
            if current_date >= self.__contract_end_date:
                raise ContractValueError("Contract period has already ended. Please use maturity check.")
            reduced_rate = self.get_interest_rate() * 0.1
            interest = self.__total_deposited * reduced_rate * (self.__contract_months / 12)
            total_amount = self.__total_deposited + interest
            self.__is_terminated = True
            print(f"Total deposited: {self.__total_deposited}")
            print(f"Interest earned (reduced rate): {interest}")
            print(f"Total amount available: {total_amount}")
            return total_amount
        except (InvalidPasswordError, ContractValueError) as e:
            print(f"[Terminate Contract Error] {e}")
            return False
        finally:
            print("[Terminate Contract Process Finished]")

    def check_maturity(self, password):
        try:
            if password != self.get_password():
                raise InvalidPasswordError("Incorrect password.")
            if self.__is_terminated or self.__is_matured:
                raise ContractValueError("Contract is already terminated or matured.")
            current_date = datetime.now()
            if current_date < self.__contract_end_date:
                remaining_days = (self.__contract_end_date - current_date).days
                raise ContractValueError(f"Contract is not matured yet. {remaining_days} days remaining.")
            interest = self.__total_deposited * self.get_interest_rate() * (self.__contract_months / 12)
            total_amount = self.__total_deposited + interest
            self.__is_matured = True
            print("Contract matured successfully!")
            print(f"Total deposited: {self.__total_deposited}")
            print(f"Interest earned (full rate): {interest}")
            print(f"Total amount available: {total_amount}")
            return total_amount
        except (InvalidPasswordError, ContractValueError) as e:
            print(f"[Maturity Check Error] {e}")
            return False
        finally:
            print("[Maturity Check Process Finished]")

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
            if self.get_balance() > 0:
                raise InvalidAmountError("TimeDepositAccount: Only one-time deposit allowed.")
            return super().deposit(amount)
        except InvalidAmountError as e:
            print(f"[Deposit Error] {e}")
            return False
        finally:
            print("[Deposit Process Finished]")

    def withdraw(self, amount, password):
        print("Time deposit accounts do not support direct withdrawal. Use terminate_contract() or check_maturity().")
        return False

    def terminate_contract(self, password):
        try:
            if password != self.get_password():
                raise InvalidPasswordError("Incorrect password.")
            if self.__is_terminated or self.__is_matured:
                raise ContractValueError("Contract is already terminated or matured.")
            current_date = datetime.now()
            if current_date >= self.__contract_end_date:
                raise ContractValueError("Contract period has already ended. Please use maturity check.")
            reduced_rate = self.get_interest_rate() * 0.1
            interest = self.get_balance() * reduced_rate * (self.__deposit_period / 365)
            total_amount = self.get_balance() + interest
            self.__is_terminated = True
            print("Contract terminated early.")
            print(f"Original deposit: {self.get_balance()}")
            print(f"Interest earned (reduced rate): {interest}")
            print(f"Total amount available: {total_amount}")
            return total_amount
        except (InvalidPasswordError, ContractValueError) as e:
            print(f"[Terminate Contract Error] {e}")
            return False
        finally:
            print("[Terminate Contract Process Finished]")

    def check_maturity(self, password):
        try:
            if password != self.get_password():
                raise InvalidPasswordError("Incorrect password.")
            if self.__is_terminated or self.__is_matured:
                raise ContractValueError("Contract is already terminated or matured.")
            current_date = datetime.now()
            if current_date < self.__contract_end_date:
                remaining_days = (self.__contract_end_date - current_date).days
                raise ContractValueError(f"Contract is not matured yet. {remaining_days} days remaining.")
            interest = self.get_balance() * self.get_interest_rate() * (self.__deposit_period / 365)
            total_amount = self.get_balance() + interest
            self.__is_matured = True
            print("Contract matured successfully!")
            print(f"Original deposit: {self.get_balance()}")
            print(f"Interest earned (full rate): {interest}")
            print(f"Total amount available: {total_amount}")
            return total_amount
        except (InvalidPasswordError, ContractValueError) as e:
            print(f"[Maturity Check Error] {e}")
            return False
        finally:
            print("[Maturity Check Process Finished]")

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
            if self.get_balance() - amount < -self.__overdraft_limit:
                raise InvalidAmountError(f"Exceeded limit. Maximum negative limit: {self.__overdraft_limit}")
            self._BankAccount__balance -= amount
            self.add_transaction(amount, "Withdrawal")
            print(f"Withdraw {amount} success. Current balance: {self.get_balance()}")
            return True
        except (InvalidPasswordError, InvalidAmountError) as e:
            print(f"[Withdraw Error] {e}")
            return False
        finally:
            print("[Withdraw Process Finished]")

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
# NormalAccount
# ----------------------
class NormalAccount(BankAccount):
    def check_maturity(self, password):
        print("Normal account does not support maturity check.")
        return False
    def terminate_contract(self, password):
        print("Normal account does not support contract termination.")
        return False

# ----------------------
# Bank Class
# ----------------------
class Bank:
    def __init__(self):
        self.accounts = []
        self.account_numbers = set()
        self.total_amount = 0
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
            self.accounts.append(acc)
            print("Account created successfully!")
            acc.show_account_info()
            return acc
        except Exception as e:
            print(f"[Account Creation Error] {e}")
            return None

    def show_all_accounts(self):
        print("\n=== All Accounts in Bank ===")
        for acc in self.accounts:
            acc.show_account_info()
            print("--------------------------")
        print(f"Total amount in bank: {self.total_amount}")
        print(f"Max overdraft allowed: {self.max_overdraft}")
        
# ----------------------
# Menu function for each account type
# ----------------------
def run_account_menu(acc):
    while True:
        print("\n1. Deposit  2. Withdraw  3. Account Info  4. Maturity/Terminate  5. Transaction History  0. Exit")
        sel = input("Choice: ")
        if sel == '1':
            if hasattr(acc, 'monthly_deposit'):
                pw = input("Enter password: ")
                acc.monthly_deposit(pw)
            else:
                try:
                    amount = int(input("Deposit amount: "))
                    acc.deposit(amount)
                except Exception as e:
                    print(f"[Deposit Error] {e}")
        elif sel == '2':
            try:
                amount = int(input("Withdrawal amount: "))
                pw = input("Enter password: ")
                acc.withdraw(amount, pw)
            except Exception as e:
                print(f"[Withdrawal Error] {e}")
        elif sel == '3':
            acc.show_account_info()
        elif sel == '4':
            if hasattr(acc, 'terminate_contract') or hasattr(acc, 'check_maturity'):
                pw = input("Enter password: ")
                if hasattr(acc, 'terminate_contract'):
                    print("- Try early termination:")
                    acc.terminate_contract(pw)
                if hasattr(acc, 'check_maturity'):
                    print("- Try maturity check:")
                    acc.check_maturity(pw)
            else:
                print("[Info] Normal account has no maturity/terminate function.")
        elif sel == '5':
            if hasattr(acc, 'show_transaction_history'):
                acc.show_transaction_history()
            else:
                print("No transaction history available.")
        elif sel == '0':
            print("Exiting.")
            break
        else:
            print("Invalid choice.")

# Main loop
if __name__ == "__main__":
    bank = Bank()
    while True:
        print("\n1. Create Account  2. Show Bank Info  0. Exit")
        sel = input("Choice: ")
        if sel == '1':
            acc = bank.create_account_with_input()
            if acc:
                run_account_menu(acc)
        elif sel == '2':
            bank.show_all_accounts()
        elif sel == '0':
            print("Exiting.")
            break
        else:
            print("Invalid choice.")