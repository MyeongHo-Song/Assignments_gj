"""
File Name: main.py
Created Date: 2025-07-19
Programmer: Kwanju Eun
Description: Main entry point for the bank system application
"""
from bank import Bank
from accounts.types import SavingAccount, TimeDepositAccount
from ui_helpers import (
    create_account_with_input,
    select_account,
    handle_contract_termination,
    show_main_menu,
    show_account_menu
)


def handle_deposit(account):
    """Handle deposit operation"""
    try:
        amount = int(input("Deposit amount: "))
        account.deposit(amount)
    except Exception as e:
        print(f"[Deposit Error] {e}")


def handle_withdraw(account, bank):
    """Handle withdraw/termination operation"""
    if isinstance(account, (SavingAccount, TimeDepositAccount)):
        # Contract termination
        return handle_contract_termination(account, bank)
    else:
        # Regular withdrawal
        try:
            amount = int(input("Withdrawal amount: "))
            pw = input("Enter password: ")
            account.withdraw(amount, pw)
        except Exception as e:
            print(f"[Withdrawal Error] {e}")
    return None


def show_account_transactions(account, bank):
    """Display transactions for specific account"""
    transactions = bank.get_transactions_by_account(account.get_account_number())
    print(f"\nTransaction History for {account.get_username()}:")
    
    if not transactions:
        print("No transactions found.")
    else:
        for i, trans in enumerate(transactions, 1):
            print(f"{i}. {trans.get_transaction_type()}: {trans.get_amount()} at {trans.get_transaction_date()}")


def main():
    """Main program function"""
    bank = Bank()
    selected_account = None
    
    while True:
        if selected_account is None:
            # Main menu
            show_main_menu()
            choice = input("Choice: ")
            
            if choice == '1':
                create_account_with_input(bank)
            elif choice == '2':
                selected_account = select_account(bank)
                if selected_account:
                    print(f"Selected: {selected_account.get_username()}'s {selected_account.get_account_type()}")
            elif choice == '3':
                bank.show_all_accounts()
            elif choice == '4':
                bank.show_all_transactions()
            elif choice == '0':
                print("Exiting. Thank you!")
                break
            else:
                print("Invalid choice.")
        else:
            # Account menu
            show_account_menu(selected_account)
            choice = input("Choice: ")
            
            if choice == '1':
                handle_deposit(selected_account)
            elif choice == '2':
                new_account = handle_withdraw(selected_account, bank)
                if new_account:
                    selected_account = None  # Go back to main menu
            elif choice == '3':
                selected_account.show_account_info()
            elif choice == '4':
                show_account_transactions(selected_account, bank)
            elif choice == '5':
                selected_account = None
                print("Returned to main menu.")
            elif choice == '0':
                print("Exiting. Thank you!")
                break
            else:
                print("Invalid choice.")


if __name__ == "__main__":
    main()