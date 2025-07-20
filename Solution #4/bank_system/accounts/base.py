"""
File Name: accounts/base.py
Created Date: 2025-07-19
Programmer: Kwanju Eun
Description: Base account classes for the bank system
"""
from datetime import datetime, timedelta
from exceptions import InvalidPasswordError, InvalidAmountError, ContractValueError


class BankAccount:
    """Base bank account class - can be used as a normal account"""
    
    def __init__(self, username, password, interest_rate):
        self._username = username
        self._password = password
        self._bank_account_number = None  # Will be set by Bank
        self._interest_rate = interest_rate
        self._balance = 0
        self._created_date = datetime.now()
        self._bank = None  # Reference to Bank

    def set_bank(self, bank):
        """Set bank reference"""
        self._bank = bank

    def set_account_number(self, account_number):
        """Set account number (called by Bank)"""
        self._bank_account_number = account_number

    def _validate_password(self, password):
        """Validate password"""
        if password != self._password:
            raise InvalidPasswordError("Incorrect password.")

    def _validate_amount(self, amount):
        """Validate amount for basic operations"""
        if amount <= 0:
            raise InvalidAmountError("Amount must be greater than 0.")

    def deposit(self, amount):
        """Deposit money to account"""
        try:
            self._validate_amount(amount)
            self._balance += amount
            if self._bank:
                self._bank.add_transaction(
                    self._bank_account_number, 
                    self._username,
                    self.__class__.__name__,
                    amount, 
                    "Deposit"
                )
            print(f"Deposit successful! Current balance: {self._balance}")
            return True
        except InvalidAmountError as e:
            print(f"[{e.get_error_type()}] {e}")
            return False
        finally:
            print("[Deposit Process Finished]")

    def _check_withdrawal_allowed(self, amount):
        """Check if withdrawal is allowed - can be overridden"""
        if self._balance < amount:
            raise InvalidAmountError("Insufficient balance.")

    def withdraw(self, amount, password):
        """Withdraw money from account"""
        try:
            self._validate_password(password)
            self._validate_amount(amount)
            self._check_withdrawal_allowed(amount)
            self._balance -= amount
            if self._bank:
                self._bank.add_transaction(
                    self._bank_account_number,
                    self._username,
                    self.__class__.__name__,
                    amount,
                    "Withdrawal"
                )
            print(f"Withdrawal successful! Current balance: {self._balance}")
            return True
        except (InvalidPasswordError, InvalidAmountError) as e:
            self._handle_exception(e)
            return False
        finally:
            print("[Withdrawal Process Finished]")

    def _handle_exception(self, e):
        """Handle exceptions uniformly"""
        if isinstance(e, InvalidPasswordError):
            print(f"[PASSWORD_ERROR] {e}")
        elif isinstance(e, InvalidAmountError):
            print(f"[{e.get_error_type()}] {e}")
        elif isinstance(e, ContractValueError):
            print(f"[CONTRACT_ERROR] {e}")
        else:
            print(f"[Error] {e}")

    # Getter methods
    def get_balance(self):
        return self._balance
    
    def get_password(self):
        return self._password
    
    def get_created_date(self):
        return self._created_date
    
    def get_account_type(self):
        return self.__class__.__name__
    
    def get_username(self):
        return self._username
    
    def get_interest_rate(self):
        return self._interest_rate
    
    def get_account_number(self):
        return self._bank_account_number
    
    def show_account_info(self):
        """Display account information"""
        print(f"Name: {self._username}")
        print(f"Account type: {self.get_account_type()}")
        print(f"Interest rate: {self._interest_rate}")
        print(f"Balance: {self._balance}")
        print(f"Created date: {self._created_date}")
        print(f"Bank account number: {self._bank_account_number}")

class ContractAccount(BankAccount):
    """Base class for contract-based accounts (Saving, TimeDeposit)"""
    
    def __init__(self, username, password, interest_rate):
        super().__init__(username, password, interest_rate)
        self._is_terminated = False
        self._is_matured = False
        self._contract_end_date = None

    def _check_contract_status(self):
        """Check if contract is still valid"""
        if self._is_terminated or self._is_matured:
            raise ContractValueError("Contract is terminated or matured.")
        
        if self._contract_end_date and datetime.now() > self._contract_end_date:
            raise ContractValueError("Contract period has ended.")

    def _calculate_interest(self, principal, rate, period_fraction):
        """Calculate interest"""
        return principal * rate * period_fraction
