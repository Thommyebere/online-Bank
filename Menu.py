from database import Database

import datetime

Database.initialize()


class Transactions(object):
    def __init__(self):
        pass

    @staticmethod
    def check_balance(user):
        users = Database.find_one('Transaction', {'user_name': user})
        print("Your Balance is {}".format(users['balance']))

    @staticmethod
    def deposit(user):
        deposit = int(input("Enter amount to be deposited"))
        users = Database.find_one('Transaction', {'user_name': user})
        users['balance'] = deposit + users['balance']
        transaction_date = datetime.datetime.utcnow()
        Database.DATABASE['Transaction'].update_one({'user_name': users['user_name']}, {'$set': users})
        transaction_date = datetime.datetime.utcnow()
        print("Transaction successful")
        Database.DATABASE['history'].insert(
            {"user_name": users['user_name'], "balance": users['balance'],
             "transaction_type": "deposit", "date": transaction_date, "amount": deposit})

    @staticmethod
    def withdraw(user):
        amount = int(input(" Enter amount to withdraw "))
        users = Database.find_one('Transaction', {'user_name': user})
        if users['balance'] < amount:
            print("Insufficient Funds")
        else:
            users['balance'] = users['balance'] - amount
            Database.DATABASE['Transaction'].update_one({'user_name': users['user_name']}, {'$set': users})
            transaction_date = datetime.datetime.utcnow()
            Database.DATABASE['history'].insert(
                {"balance": users['balance'],
                 "transaction_type": "withdraw", "date": transaction_date, "amount": amount})

    @staticmethod
    def transfer(user):
        transfer_account = input("Enter account to be transferred to ")
        account_details = Database.find_one('Transaction', {'account_number': transfer_account})
        if account_details is not None:
            users = Database.find_one('Transaction', {'user_name': user})
            trans_amount = int(input("Enter the amount you wanna transfer "))
            if users['balance'] < trans_amount:
                print("Account cant be processed ")
            else:
                users['balance'] = users['balance'] - trans_amount
                account_details['balance'] = account_details['balance'] + trans_amount
                Database.DATABASE['Transaction'].update_one({'user_name': users['user_name']}, {'$set': users})
                Database.DATABASE['Transaction'].update_one({'user_name': account_details['user_name']},
                                                            {'$set': account_details})
                transaction_date = datetime.datetime.utcnow()
                Database.DATABASE['history'].insert(
                    {"user_name": users['user_name'], "balance": users['balance'],
                     "transaction_type": "transfer", "date": transaction_date, "amount": trans_amount})
                Database.DATABASE['history'].insert(
                    {"user_name": account_details['user_name'], "balance": account_details['balance'],
                     "transaction_type": "balance", "date": transaction_date, "amount": trans_amount})
                print("Transaction successful")
        else:
            print("Account doesnt exist ")

    @staticmethod
    def transaction_history(user):
        data = Database.find('history', {'user_name': user})
        for dat in data:
            print("balance: {} transaction-type: {} transacted-amount: {} date:{} ".format(dat['balance'],
                                                                                           dat['transaction_type'],
                                                                                           dat['amount'],
                                                                                           dat['date']))



