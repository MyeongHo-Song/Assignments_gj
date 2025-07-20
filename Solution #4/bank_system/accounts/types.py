"""
File Name: accounts/types.py
Created Date: 2025-07-19
Programmer: Kwanju Eun
Description: Specific account type implementations
"""
from datetime import datetime, timedelta
from accounts.base import BankAccount, ContractAccount
from exceptions import InvalidPasswordError, InvalidAmountError, ContractValueError


class SavingAccount(ContractAccount):
    """Saving account with monthly deposits and contract period"""
    
    def __init__(self, username, password, interest_rate, monthly_amount, contract_months):
        super().__init__(username, password, interest_rate)
        self.__monthly_amount = monthly_amount
        self.__contract_months = contract_months
        self._contract_end_date = self._created_date + timedelta(days=contract_months * 30)
        self.__total_deposited = 0

    def deposit(self, amount):
        """Deposit monthly amount only"""
        try:
            if amount != self.__monthly_amount:
                raise InvalidAmountError(f"SavingAccount: Only monthly amount ({self.__monthly_amount}) is allowed.")
            self._check_contract_status()
            
            self.__total_deposited += self.__monthly_amount
            return super().deposit(self.__monthly_amount)
        except (InvalidAmountError, ContractValueError) as e:
            self._handle_exception(e)
            return False

    def withdraw(self, amount, password):
        """Terminate saving account"""
        try:
            self._validate_password(password)
            self._check_contract_status()
            
            if datetime.now() < self._contract_end_date:
                # Early termination
                interest = self._calculate_interest(self.__total_deposited, self._interest_rate * 0.1, self.__contract_months / 12)
                total_amount = self.__total_deposited + interest
                self._is_terminated = True
                print("Contract terminated early.")
            else:
                # Maturity
                interest = self._calculate_interest(self.__total_deposited, self._interest_rate, self.__contract_months / 12)
                total_amount = self.__total_deposited + interest
                self._is_matured = True
                print("Contract matured successfully!")
            
            print(f"Total deposited: {self.__total_deposited}")
            print(f"Interest earned: {interest}")
            print(f"Total amount available: {total_amount}")
            
            # Process withdrawal through parent class
            self._balance = total_amount  # Set balance for withdrawal
            return super().withdraw(total_amount, password)
            
        except (InvalidPasswordError, ContractValueError) as e:
            self._handle_exception(e)
            return False

    def show_account_info(self):
        """Display saving account information"""
        super().show_account_info()
        print(f"Monthly deposit amount: {self.__monthly_amount}")
        print(f"Contract period: {self.__contract_months} months")
        print(f"Contract end date: {self._contract_end_date}")
        print(f"Total deposited: {self.__total_deposited}")


class TimeDepositAccount(ContractAccount):
    """Time deposit account with one-time deposit and fixed period"""
    
    def __init__(self, username, password, interest_rate, deposit_period=365):
        super().__init__(username, password, interest_rate)
        self.__deposit_period = deposit_period
        self._contract_end_date = self._created_date + timedelta(days=deposit_period)
        self.__initial_deposit = 0

    def deposit(self, amount):
        """Allow only one-time deposit"""
        try:
            if self._balance > 0:
                raise InvalidAmountError("TimeDepositAccount: Only one-time deposit allowed.")
            self.__initial_deposit = amount
            return super().deposit(amount)
        except InvalidAmountError as e:
            self._handle_exception(e)
            return False

    def withdraw(self, amount, password):
        """Terminate time deposit account"""
        try:
            self._validate_password(password)
            self._check_contract_status()
            
            if datetime.now() < self._contract_end_date:
                # Early termination
                interest = self._calculate_interest(self.__initial_deposit, self._interest_rate * 0.1, self.__deposit_period / 365)
                total_amount = self.__initial_deposit + interest
                self._is_terminated = True
                print("Contract terminated early.")
            else:
                # Maturity
                interest = self._calculate_interest(self.__initial_deposit, self._interest_rate, self.__deposit_period / 365)
                total_amount = self.__initial_deposit + interest
                self._is_matured = True
                print("Contract matured successfully!")
            
            print(f"Original deposit: {self.__initial_deposit}")
            print(f"Interest earned: {interest}")
            print(f"Total amount available: {total_amount}")
            
            # Process withdrawal through parent class
            self._balance = total_amount  # Set balance for withdrawal
            return super().withdraw(total_amount, password)
            
        except (InvalidPasswordError, ContractValueError) as e:
            self._handle_exception(e)
            return False

    def show_account_info(self):
        """Display time deposit account information"""
        super().show_account_info()
        print(f"Deposit period: {self.__deposit_period} days")
        print(f"Contract end date: {self._contract_end_date}")


class OverdraftAccount(BankAccount):
    """Account that allows overdraft up to a specified limit"""
    
    def __init__(self, username, password, interest_rate, overdraft_limit=500000):
        super().__init__(username, password, interest_rate)
        self.__overdraft_limit = overdraft_limit

    def _check_withdrawal_allowed(self, amount):
        """Override to allow overdraft up to limit"""
        if self._balance - amount < -self.__overdraft_limit:
            raise InvalidAmountError(f"Exceeded limit. Maximum negative limit: {self.__overdraft_limit}")

    def withdraw(self, amount, password):
        """Withdraw with overdraft capability"""
        return super().withdraw(amount, password)

    def show_account_info(self):
        """Display overdraft account information"""
        super().show_account_info()
        print(f"Overdraft limit: {self.__overdraft_limit}")
        print(f"Available overdraft: {self.__overdraft_limit + self._balance}")