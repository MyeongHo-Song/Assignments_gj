"""
File Name: assignment_2.py
Created Date: 2025-06-24
Programmer: Kwanju Eun
Description: Create various types of bank accounts (savings, deposit/withdrawal accounts, overdraft accounts) using Python classes, 
and implement deposit and withdrawal functions. A unique ID is automatically assigned to each account,
and the account type is considered when depositing and withdrawing.
"""
# Make a class for a bank account. The class contains the following attributes
from datetime import datetime, timedelta
import random

class BankAccount:
    # Class variable to track used account numbers
    used_account_numbers = set()
    
    def __init__(self, username, password, interest_rate):
        self.__username = username
        self.__password = password
        self.__bank_account_number = self.__generate_unique_account_number()
        self.__interest_rate = interest_rate
        self.__balance = 0
        self.__created_date = datetime.now()
        
    def __generate_unique_account_number(self):
        """Generate a unique 8-digit account number"""
        while True:
            account_number = random.randint(10000000, 99999999)
            if account_number not in BankAccount.used_account_numbers:
                BankAccount.used_account_numbers.add(account_number)
                return account_number
        
    def __del__(self):
        """Finalizer to be called when an account object is destroyed."""
        print(f"Account for {self.__username} (Account #: {self.__bank_account_number}) is being closed.")
        
    def deposit(self, amount):
        """Deposits a specified amount into the account."""
        if amount <= 0:
            print("Invalid amount")
        else:
            self.__balance += amount
            print(f"Deposit {amount} success. Current balance: {self.__balance}")
    
    def withdraw(self, amount, password):
        """Basic withdrawal method for D/W account - can be overridden by child classes"""
        if not self._validate_withdrawal(amount, password):
            return
        
        # Basic D/W account logic - only withdraw if sufficient balance
        if self.__balance >= amount:
            self.__balance -= amount
            print(f"Withdraw {amount} success. Current balance: {self.__balance}")
        else:
            print("Insufficient balance")
    
    def _validate_withdrawal(self, amount, password):
        """Common validation for withdrawal operations"""
        if password != self.__password:
            print("Invalid password")
            return False
        
        if amount <= 0:
            print("Invalid amount")
            return False
        
        return True
    
    def show_account_info(self):
        """Displays the account's information."""
        print(f"Username: {self.__username}")
        print(f"Account type: {self.__class__.__name__}")
        print(f"Interest rate: {self.__interest_rate}")
        print(f"Balance: {self.__balance}")
        print(f"Created date: {self.__created_date}")
        print(f"Bank account number: {self.__bank_account_number}")
        
    def get_balance(self):
        return self.__balance
    
    def get_password(self):
        return self.__password
    
    def get_created_date(self):
        return self.__created_date


class Transaction:
    def __init__(self, account, amount, transaction_type):
        self.__account = account
        self.__amount = amount
        self.__transaction_type = transaction_type
        self.__transaction_date = datetime.now()
        
    def show_transaction_info(self):
        print(f"Transaction type: {self.__transaction_type}")
        print(f"Transaction amount: {self.__amount}")
        print(f"Transaction date: {self.__transaction_date}")
        print(f"Account balance: {self.__account.get_balance()}")


class SavingAccount(BankAccount):
    """Installment Savings Account - inherits from BankAccount"""
    def __init__(self, username, password, interest_rate, monthly_amount, contract_months):
        super().__init__(username, password, interest_rate)
        self.__monthly_amount = monthly_amount
        self.__contract_months = contract_months
        self.__contract_end_date = self.get_created_date() + timedelta(days=contract_months * 30)
        self.__total_deposited = 0
        self.__is_terminated = False
        self.__is_matured = False
        
    def monthly_deposit(self, password):
        """Monthly installment deposit"""
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
        
        # Add to total deposited
        self.__total_deposited += self.__monthly_amount
        self.deposit(self.__monthly_amount)  # Use parent's deposit method
        
        print(f"Monthly deposit {self.__monthly_amount} success. Total deposited: {self.__total_deposited}")
        return True
    
    def terminate_contract(self, password):
        """Terminate the contract early with reduced interest"""
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
        
        # Calculate reduced interest
        reduced_rate = self._BankAccount__interest_rate * 0.1
        interest = self.__total_deposited * reduced_rate * (self.__contract_months / 12)
        total_amount = self.__total_deposited + interest
        
        self.__is_terminated = True
        print(f"Contract terminated early.")
        print(f"Total deposited: {self.__total_deposited}")
        print(f"Interest earned (reduced rate): {interest}")
        print(f"Total amount available: {total_amount}")
        return total_amount
    
    def check_maturity(self, password):
        """Check if contract has matured"""
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
        
        # Calculate full interest
        interest = self.__total_deposited * self._BankAccount__interest_rate * (self.__contract_months / 12)
        total_amount = self.__total_deposited + interest
        
        self.__is_matured = True
        print(f"Contract matured successfully!")
        print(f"Total deposited: {self.__total_deposited}")
        print(f"Interest earned (full rate): {interest}")
        print(f"Total amount available: {total_amount}")
        return total_amount
    
    def withdraw(self, amount, password):
        """Saving accounts cannot withdraw directly - use terminate_contract() or check_maturity()"""
        print("Saving accounts do not support direct withdrawal.")
        print("Use terminate_contract() for early termination or check_maturity() when contract ends.")
        return False
    
    def show_account_info(self):
        """Display savings account specific information"""
        super().show_account_info()
        print(f"Monthly deposit amount: {self.__monthly_amount}")
        print(f"Contract period: {self.__contract_months} months")
        print(f"Contract end date: {self.__contract_end_date}")
        print(f"Total deposited: {self.__total_deposited}")
        


class TimeDepositAccount(BankAccount):
    """Time Deposit Account - one-time deposit with maturity or early termination"""
    def __init__(self, username, password, interest_rate, deposit_period=365):
        super().__init__(username, password, interest_rate)
        self.__deposit_period = deposit_period
        self.__contract_end_date = self.get_created_date() + timedelta(days=deposit_period)
        self.__is_terminated = False
        self.__is_matured = False
        
    def terminate_contract(self, password):
        """Terminate the contract early with reduced interest"""
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
        
        # Calculate reduced interest (10% of original rate)
        reduced_rate = self._BankAccount__interest_rate * 0.1
        interest = self.get_balance() * reduced_rate * (self.__deposit_period / 365)
        total_amount = self.get_balance() + interest
        
        self.__is_terminated = True
        print(f"Contract terminated early.")
        print(f"Original deposit: {self.get_balance()}")
        print(f"Interest earned (reduced rate): {interest}")
        print(f"Total amount available: {total_amount}")
        return total_amount
    
    def check_maturity(self, password):
        """Check if contract has matured"""
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
        
        # Calculate full interest
        interest = self.get_balance() * self._BankAccount__interest_rate * (self.__deposit_period / 365)
        total_amount = self.get_balance() + interest
        
        self.__is_matured = True
        print(f"Contract matured successfully!")
        print(f"Original deposit: {self.get_balance()}")
        print(f"Interest earned (full rate): {interest}")
        print(f"Total amount available: {total_amount}")
        return total_amount
    
    def withdraw(self, amount, password):
        """Time deposit accounts cannot withdraw directly - use terminate_contract() or check_maturity()"""
        print("Time deposit accounts do not support direct withdrawal.")
        print("Use terminate_contract() for early termination or check_maturity() when contract ends.")
        return False
    
    def show_account_info(self):
        """Display time deposit account specific information"""
        super().show_account_info()
        print(f"Deposit period: {self.__deposit_period} days")
        print(f"Contract end date: {self.__contract_end_date}")


class OverdraftAccount(BankAccount):
    """Overdraft Account - can withdraw beyond balance up to overdraft limit"""
    def __init__(self, username, password, interest_rate, overdraft_limit=500000):
        super().__init__(username, password, interest_rate)
        self.__overdraft_limit = overdraft_limit
        
    def withdraw(self, amount, password):
        # Use parent class validation
        if not self._validate_withdrawal(amount, password):
            return False
        
        # Check if withdrawal would exceed the overdraft limit
        if self.get_balance() - amount >= -self.__overdraft_limit:
            # Directly update balance to allow negative values
            self._BankAccount__balance -= amount
            print(f"Withdraw {amount} success. Current balance: {self.get_balance()}")
            return True
        else:
            print(f"Insufficient balance. Overdraft limit is {self.__overdraft_limit}")
            return False
    
    def show_account_info(self):
        """Display overdraft account specific information"""
        super().show_account_info()
        print(f"Overdraft limit: {self.__overdraft_limit}")
        print(f"Available overdraft: {self.__overdraft_limit + self.get_balance()}")


if __name__ == "__main__":
    # Test basic BankAccount (D/W functionality)
    print("=== Testing Basic BankAccount (D/W) ===")
    basic_account = BankAccount("John", "123456", 0.02)
    basic_account.deposit(100000)
    basic_account.withdraw(50000, "123456")
    basic_account.show_account_info()
    print("--------------------------------"*2)
    
    # Test Saving Account (Installment Savings)
    print("=== Testing Saving Account (Installment) ===")
    saving_acc = SavingAccount("Alice", "password123", 0.05, 100000, 12)  # 5% interest, 100k monthly, 12 months
    
    # Make monthly deposits
    for i in range(6):  # Only 6 out of 12 months
        saving_acc.monthly_deposit("password123")
    
    saving_acc.show_account_info()
    print("--------------------------------"*2)
    
    # Test early termination of saving account
    print("=== Testing Early Termination of Saving Account ===")
    total_amount = saving_acc.terminate_contract("password123")
    print("--------------------------------"*2)
    
    # Test Time Deposit Account
    print("=== Testing Time Deposit Account ===")
    timed_acc = TimeDepositAccount("Bob", "password456", 0.06, 365)  # 6% interest, 365 days
    timed_acc.deposit(500000)  # One-time deposit
    
    print("Time Deposit Account:")
    timed_acc.show_account_info()
    print("--------------------------------"*2)
    
    # Test early termination of time deposit
    print("=== Testing Early Termination of Time Deposit ===")
    total_amount = timed_acc.terminate_contract("password456")
    print("--------------------------------"*2)
    
    # Test Overdraft Account
    print("=== Testing Overdraft Account ===")
    overdraft_acc = OverdraftAccount("Charlie", "password789", 0.015, 300000)
    overdraft_acc.deposit(100000)
    overdraft_acc.withdraw(350000, "password789")  # Should work with overdraft
    overdraft_acc.show_account_info()
    print("--------------------------------"*2)
    


    