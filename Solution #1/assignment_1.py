"""
File Name: assignment_1.py
Created Date: 2025-06-17
Programmer: Kwanju Eun
Description: Python class를 활용하여 다양한 유형의 은행 계좌(적금, 입출금통장, 마이너스통장)를 생성하고,
입금과 출금 기능을 구현한다. 계좌마다 고유 ID가 자동으로 부여되며, 입출금 시 계좌 유형을 고려한다.
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
        
    def deposit(self, amount):
        if amount <= 0:
            print("Invalid amount")
        else:
            self.__balance += amount
            return print(f"Deposit {amount} success. Current balance: {self.__balance}")
    
    def withdraw(self, amount, password):
        if password != self.__password:
            print("Invalid password")
        
        if amount <= 0:
            print("Invalid amount")
            return
        
        else:
            if self.__account_type=="D/W_account":
                if self.__balance >= amount:
                    self.__balance -= amount
                    print(f"Withdraw {amount} success. Current balance: {self.__balance}")
                else:
                    print("Insufficient balance")
            elif self.__account_type=="Saving_account":
                    print("Saving_account cannot withdraw before 1 year")
                    
            elif self.__account_type=="minus_account":
                if self.__balance >= -500000:
                    self.__balance -= amount
                    print(f"Withdraw {amount} success. Current balance: {self.__balance}")
                else:
                    print("Insufficient balance")
            else:
                print("Invalid account type")
    
    def show_account_info(self):
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
    account3.withdraw(50000, "123456")
    account3.show_account_info()