##################################################################################
# Name: Ugyen Lhendup
# Course: First Year B.E in ECE
# Student ID Number: 02230116
##################################################################################
# REFERENCES:
# https://chat.openai.com/
#####################################################################################

#import the os to interact with system especially for now to check the existence of account.txt file.
#random is being imported to generate random account numbers and password and string to access letters
import os
import random
import string
import sys

# Created class Account
class Account:
    # Using constructor, accountNumber, password, accountType and balance are initialized
    def __init__(self, accountHolder, accountNumber, password, accountType, balance=0.0):
        self.accountHolder = accountHolder
        self.accountNumber = accountNumber
        self.password = password
        self.accountType = accountType
        self.balance = balance

    # Deposit method is defined to deposit the money
    def deposit(self, amount):
        self.balance += amount
        print(f"You Deposited {amount}. New balance: {self.balance}")

    # Withdraw method is defined to withdraw the money
    def withdraw(self, amount):
        if amount > self.balance:
            print("You Don't have Insufficient Ammount")
            return False
        self.balance -= amount
        print(f"You Withdrew {amount}. New balance: {self.balance}")
        return True

# The class BusinessAccount is created inheriting the attributes and methods from parent class Account and
# the accountType is set to Business here
class BusinessAccount(Account):
    def __init__(self, accountHolder, accountNumber, password, balance=0.0):
        super().__init__(accountHolder, accountNumber, password, "Business", balance)

# Same as above, the class PersonalAccount is created inheriting the attributes and methods from parent class Account and
# the accountType is set Personal
class PersonalAccount(Account):
    def __init__(self, accountHolder, accountNumber, password, balance=0.0):
        super().__init__(accountHolder, accountNumber, password, "Personal", balance)

# This block of code generates the random account number. All the account numbers will start from 223
def generate_account_number():
    return "2233" + ''.join(random.choices(string.digits, k=1))

# After creating the account, this generates a password
def generate_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=2))

# After creating the account, those data should be saved. Therefore, this block of codes saves the data in account.txt file
def save_account(accounts):
    with open("accounts.txt", "w") as bank_acc_file:
        for account in accounts.values():
            bank_acc_file.write(f"{account.accountHolder},{account.accountNumber},{account.password},{account.accountType},{account.balance}\n")

# Here the code will load the accounts.txt file 
def load_accounts():
    # account variable is declared where it will store accountNumber as key and its properties, password,accountTypes, balance
    # be the values stored in the nested dictionary
    accounts = {}
    # The file is being loaded and data from the file will be extracted. All the data will be stored in the account variable
    # in the form of nested dictionary
    if os.path.exists("accounts.txt"):
        with open("accounts.txt", "r") as bank_acc_file:
            for line in bank_acc_file:
                accountHolder, accountNumber, password, accountType, balance = line.strip().split(",")
                balance = float(balance)
                if accountType == "Business":
                    accounts[accountNumber] = BusinessAccount(accountHolder, accountNumber, password, balance)
                elif accountType == "Personal":
                    accounts[accountNumber] = PersonalAccount(accountHolder, accountNumber, password, balance)
    return accounts

# This function will be used to delete the account
def delete_account(accounts, accountNumber):
    if accountNumber in accounts:
        del accounts[accountNumber]
        save_account(accounts)
        print("Successfully Deleted the Account.")
    else:
        print("Account Not Found.")

# This function is for logging in the account rendering account number and password
def login(accounts):
    accountNumber = input("Enter Account Number: ")
    password = input("Enter Password: ")
    account = accounts.get(accountNumber)
    # This block of conditional statement is very important as it checks whether the account number and password matches or not. If it does, it
    # will show the properties associated to it or it will return invalid statement if input did not match
    if account and account.password == password:
        print(f"\n  Welcome, {account.accountHolder}")
        return account
    else:
        print("Invalid Account Number or Password.")
        return None

# This section is for transferring money from one account to another
def transfer_money(accounts, sender_account):
    recipient_account_num = input("Enter Recipient Account Number: ")
    # The code below checks whether the recipient account exists in bank account listing file
    amount = float(input("Enter Amount To Transfer: "))
    receiver_account = accounts.get(recipient_account_num)
    # If recipient account does not exist, then transfer cannot take place
    if not receiver_account:
        print("Recipient Account Does Not Exist.")
        return
    if sender_account.withdraw(amount):
        receiver_account.deposit(amount)
        save_account(accounts)
        print(f"\n Transfer Successful. {amount} Amount transferred to {receiver_account.accountHolder} ")

# It is the main block where every function and object created above will be used here
def main():
    # Account listed in the file is being loaded
    accounts = load_accounts()
    # The program gets in the loop
    while True:
        print("\nWELCOME TO BANKING APP\n")
        # It gives option for the user to select an option for the program to run
        print("\n1. Open Account\n2. Login\n3. Exit")
        # User will input the selected option here
        user_choice = input("Choose An Option: ")
        # Then conditional statements are used below for program to run as per the input data from the user
        # Here if choice is "1", new account is being created as per the user choice to create business or personal account
        if user_choice == "1":
            accountType = input("Enter Account Type (B fot Business/ P for Personal): ").lower()
            accountHolder = input("Enter Your Name: ")
            accountNumber = generate_account_number()
            password = generate_password()
            if accountType == "b":
                new_account = BusinessAccount(accountHolder, accountNumber, password)
            elif accountType == "p":
                new_account = PersonalAccount(accountHolder, accountNumber, password)
            else:
                # Prints out invalid message if invalid input is given
                print("Invalid Account Type.")
                continue
            accounts[accountNumber] = new_account
            save_account(accounts)
            print(f"Congratulations, Account Successfully Created. Name: {accountHolder}, Account number: {accountNumber}, Password: {password}")

        # If user's input is "2", it is section for the login
        elif user_choice == "2":
            account = login(accounts)
            # If logging in is successful, it will give further options like checking account balance, depositing, withdrawing, transferring and
            # logging out
            if account:
                while True:
                    print("\n1. Check Balance\n2. Deposit\n3. Withdraw\n4. Transfer Money\n5. Delete Account\n6. Logout")
                    action = input("Choose An Action: ")
                    if action == "1":
                        print(f"Balance: {account.balance}")
                    elif action == "2":
                        amount = float(input("Enter Amount To Deposit: "))
                        account.deposit(amount)
                        save_account(accounts)
                    elif action == "3":
                        amount = float(input("Enter Amount To Withdraw: "))
                        account.withdraw(amount)
                        save_account(accounts)
                    elif action == "4":
                        transfer_money(accounts, account)
                    elif action == "5":
                        delete_account(accounts, account.accountNumber)
                        break
                    elif action == "6":
                        print("\nTHANK YOU FOR USING THE APP\n")
                        break
                        sys.exit()
                    else:
                        # Prints error message if given wrong input
                        print("Invalid Option.")

        # For user choice of "3" the program exits
        elif user_choice == "3":
            print("\nTHANK YOU FOR USING THE APP\n")
            break
            sys.exit()
        else:
            # Prints error message for invalid input
            print("Invalid Option.")

# Main function is called for the program to run.
main()
