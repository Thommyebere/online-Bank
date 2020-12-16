import Menu
from database import Database
import string
from random import choice
import datetime

Database.initialize()


class Registration(object):
    def __init__(self):
        self.first_name = input("Enter your First Name ")
        self.last_name = input("Enter your Last Name ")
        self.age = input("Enter your age ")
        self.gender = input("Enter your gender ")
        chars = string.digits
        self.account_number = ''.join(choice(chars) for _ in range(16))
        self.created_date = datetime.datetime.utcnow()
        self.password = input("create your password")
        self.re_password = input("Re-Enter your password")
        self.user = self.registration()
        self.dot = None

    def registration(self):
        while self.password != self.re_password:
            self.password = input("create your password")
            self.re_password = input("Re-Enter your password")
        else:
            if len(self.first_name) and len(self.last_name) >= 2:
                user_sub_1 = self.first_name[0:2]
                user_sub_2 = self.last_name[0:2]
                user_sub = user_sub_1 + user_sub_2
                user_string = 8 - len(user_sub)
                chars = string.digits
                random = ''.join(choice(chars) for _ in range(user_string))
                user_sub1 = user_sub.upper()
                user_namee = random + user_sub1
            elif len(self.first_name) >= 2:
                user_sub_1 = self.first_name[0:2]
                user_sub = user_sub_1 + self.last_name
                user_string = 8 - len(user_sub)
                chars = string.digits
                random = ''.join(choice(chars) for _ in range(user_string))
                user_sub1 = user_sub.upper()
                user_namee = random + user_sub1
            else:
                user_sub_1 = self.last_name[0:2]
                user_sub = user_sub_1 + self.first_name
                user_string = 8 - len(user_sub)
                chars = string.digits
                random = ''.join(choice(chars) for _ in range(user_string))
                user_sub1 = user_sub.upper()
                user_namee = random + user_sub1
            return user_namee

    def save_to_mongo(self):
        Database.insert(collection='details', query=self.json())
        print("Thanks for registering")

    def json(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'created_date': self.created_date,
            'gender': self.gender,
            'user_name': self.user,
            'account_number': self.account_number,
            'password': self.password
        }

    def create_account_history(self):
        return {
            'user_name': self.user,
            'account_number': self.account_number,
            'balance': 0,
            'date': self.created_date
        }

    def save_to_acct_hist(self):
        Database.insert(collection='Transaction', query=self.create_account_history())

    def transaction_history(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'account_number': self.account_number,
            'balance': 0,
            'date': self.created_date,
            'transaction_type': 'account_creation'
        }

    def save_history(self):
        Database.insert(collection='history', query=self.transaction_history())





