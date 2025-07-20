"""
transaction.py
Transaction class for recording banking transactions
"""
from datetime import datetime


class Transaction:
    """Represents a single banking transaction"""
    
    def __init__(self, account_number, username, account_type, amount, transaction_type):
        self.__account_number = account_number
        self.__username = username
        self.__account_type = account_type
        self.__amount = amount
        self.__transaction_type = transaction_type
        self.__transaction_date = datetime.now()
    
    # Getter methods
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
        """Display transaction information"""
        print(f"Transaction type: {self.__transaction_type}")
        print(f"Transaction amount: {self.__amount}")
        print(f"Transaction date: {self.__transaction_date}")
        print(f"Account: {self.__username} ({self.__account_type}) - {self.__account_number}")