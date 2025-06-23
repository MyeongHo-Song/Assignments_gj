"""
File Name: assignment_1.py
Created Date: 2025-06-17
Programmer: Kwanju Eun
Description: Create various types of bank accounts (savings, deposit/withdrawal accounts, overdraft accounts) using Python classes, 
and implement deposit and withdrawal functions. A unique ID is automatically assigned to each account,
and the account type is considered when depositing and withdrawing.
"""
# Make a class for a bank account. The class contains the following attributes
from datetime import datetime
class BankAccount:
    Unique_id = 1
    def __init__(self, username, password, account_type, interest_rate):
        self.__username = username
        self.__password = password
        self.__account_type = account_type
        self.__interest_rate = interest_rate
        self.__balance = 0
        self.__created_date = datetime.now()
        self.__id = BankAccount.Unique_id
        BankAccount.Unique_id += 1
        
    def __del__(self):
        """Finalizer to be called when an account object is destroyed."""
        print(f"Account for {self.__username} (ID: {self.__id}) is being closed.")
        
    def deposit(self, amount):
        """Deposits a specified amount into the account."""
        if amount <= 0:
            print("Invalid amount")
        else:
            self.__balance += amount
            print(f"Deposit {amount} success. Current balance: {self.__balance}")
    
    def withdraw(self, amount, password):
        """Withdraws a specified amount from the account after verifying the password and account-specific rules."""
        if password != self.__password:
            print("Invalid password")
            return
        
        if amount <= 0:
            print("Invalid amount")
            return
        
        if self.__account_type=="D/W_account":
            if self.__balance >= amount:
                self.__balance -= amount
                print(f"Withdraw {amount} success. Current balance: {self.__balance}")
            else:
                print("Insufficient balance")
                
        elif self.__account_type=="Saving_account":
            # Check if 1 year has passed since account creation
            current_date = datetime.now()
            time_diff = current_date - self.__created_date
            if time_diff.days >= 365:
                if self.__balance >= amount:
                    self.__balance -= amount
                    print(f"Withdraw {amount} success. Current balance: {self.__balance}")
                else:
                    print("Insufficient balance")
            else:
                print("Saving_account cannot withdraw before 1 year")
                
        elif self.__account_type=="minus_account":
            # Check if withdrawal would exceed the -500,000 limit
            if self.__balance - amount >= -500000:
                self.__balance -= amount
                print(f"Withdraw {amount} success. Current balance: {self.__balance}")
            else:
                print("Insufficient balance")
        else:
            print("Invalid account type")
    
    def show_account_info(self):
        """Displays the account's information."""
        print(f"Account ID: {self.__id}")
        print(f"Username: {self.__username}")
        print(f"Account type: {self.__account_type}")
        print(f"Interest rate: {self.__interest_rate}")
        print(f"Balance: {self.__balance}")
        print(f"Created date: {self.__created_date}")
        
    def get_balance(self):
        return self.__balance

if __name__ == "__main__":
    account1 = BankAccount("John", "123456", "D/W_account", 0.02)
    account1.deposit(100000)
    account1.withdraw(50000, "123456")
    account1.show_account_info()
    print("--------------------------------"*2)
    account2 = BankAccount("Jane", "123456", "Saving_account", 0.05)
    account2.deposit(100000)
    account2.withdraw(50000, "123456")
    account2.show_account_info()
    print("--------------------------------"*2)
    account3 = BankAccount("Jim", "123456", "minus_account", 0.01)
    account3.deposit(100000)
    account3.withdraw(150000, "123456")
    account3.show_account_info()
    print("--------------------------------"*2)
    print(f"Account1 balance: {account1.get_balance()}")
    print(f"Account2 balance: {account2.get_balance()}")
    print(f"Account3 balance: {account3.get_balance()}")
    print("--------------------------------"*2)
