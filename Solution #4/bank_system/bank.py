"""
bank.py
Core bank class that manages accounts and transactions
"""
import random
from transaction import Transaction
from accounts.base import BankAccount
from accounts.types import OverdraftAccount


class Bank:
    """Main bank class that manages accounts and transactions"""
    
    def __init__(self):
        self.__accounts = []
        self.__transactions = []
        self.__used_account_numbers = set()

    def _generate_unique_account_number(self):
        """Generate unique account number"""
        while True:
            account_number = random.randint(10000000, 99999999)
            if account_number not in self.__used_account_numbers:
                self.__used_account_numbers.add(account_number)
                return account_number

    def add_transaction(self, account_number, username, account_type, amount, transaction_type):
        """Add transaction to bank's transaction history"""
        transaction = Transaction(account_number, username, account_type, amount, transaction_type)
        self.__transactions.append(transaction)
        return transaction

    def create_account(self, account):
        """Add account to bank"""
        if not isinstance(account, BankAccount):
            raise ValueError("Invalid account type")
        
        # Set account number and bank reference
        account_number = self._generate_unique_account_number()
        account.set_account_number(account_number)
        account.set_bank(self)
        
        self.__accounts.append(account)
        return account

    def get_account_by_number(self, account_number):
        """Get account by account number"""
        for acc in self.__accounts:
            if acc.get_account_number() == account_number:
                return acc
        return None

    def get_transactions_by_account(self, account_number):
        """Get all transactions for specific account"""
        return [t for t in self.__transactions if t.get_account_number() == account_number]

    def get_transactions_by_username(self, username):
        """Get all transactions for specific username"""
        return [t for t in self.__transactions if t.get_username() == username]

    def get_total_balance(self):
        """Calculate total balance in bank"""
        return sum(acc.get_balance() for acc in self.__accounts)

    def get_total_overdraft(self):
        """Calculate total overdraft limit"""
        total = 0
        for acc in self.__accounts:
            if isinstance(acc, OverdraftAccount):
                total += acc._OverdraftAccount__overdraft_limit
        return total

    def remove_account(self, account):
        """Remove account from bank"""
        if account in self.__accounts:
            self.__accounts.remove(account)

    def get_all_accounts(self):
        """Get all accounts"""
        return self.__accounts.copy()

    def get_all_transactions(self):
        """Get all transactions"""
        return self.__transactions.copy()

    def show_all_accounts(self):
        """Display all accounts information"""
        print("\n=== All Accounts in Bank ===")
        for acc in self.__accounts:
            acc.show_account_info()
            print("--------------------------")
        print(f"Total amount in bank: {self.get_total_balance()}")
        print(f"Max overdraft allowed: {self.get_total_overdraft()}")

    def show_all_transactions(self):
        """Display all transactions"""
        if not self.__transactions:
            print("No transactions found.")
            return
        
        print("\n=== All Transactions ===")
        # Group by username
        usernames = set(t.get_username() for t in self.__transactions)
        
        for username in sorted(usernames):
            print(f"\n--- {username} ---")
            user_transactions = self.get_transactions_by_username(username)
            for i, transaction in enumerate(user_transactions, 1):
                print(f"{i}. {transaction.get_transaction_type()}: {transaction.get_amount()} at {transaction.get_transaction_date()}")
                print(f"   Account: {transaction.get_account_type()} - {transaction.get_account_number()}")