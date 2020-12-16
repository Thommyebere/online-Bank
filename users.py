from database import Database
from Menu import Transactions
from test1 import Registration

Database.initialize()


class Bank(object):
    def __init__(self):
        self.ack_user = None
        self.choice = int(input(""" 1. For Log in 2. For Registration """))
        if self.choice == 1:
            if self.log_in():
                print("what do you want to do today ? ")
                menu=self.display()
                if menu == 1:
                    Transactions.check_balance(self.ack_user)

                elif menu == 2:
                    Transactions.withdraw(self.ack_user)
                elif menu == 3:
                    Transactions.transfer(self.ack_user)

                elif menu == 4:
                    Transactions.deposit(self.ack_user)
                elif menu == 5:
                    Transactions.transaction_history(self.ack_user)
                else:
                    print("Try again ")

            else:
                print("Log in was not successful")

        elif self.choice == 2:
            jame = Registration()
            jame.save_to_mongo()
            jame.create_account_history()
            jame.save_to_acct_hist()
            jame.save_history()
        else:
            print("Invalid option")

    def log_in(self):
        user = input("Enter your username ")
        password = input("Enter a password ")
        user_detail = Database.find_one('details', {'user_name': user})
        if user_detail is not None:
            if user_detail['password'] == password:
                self.ack_user = user_detail['user_name']
                return True
            else:
                print("Your password is incorrect ")
        else:
            print("This user is not found. Check the user details ")
            return False

    def display(self):
        menu = int(input("""
                Press 1 to check balance
                Press 2 to perform withdrawal
                Press 3 for Transfers
                Press 4 Deposit
                Press 5 account History """))
        return menu


