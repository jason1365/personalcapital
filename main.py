from __future__ import print_function
from personalcapital import PersonalCapital, RequireTwoFactorException, TwoFactorVerificationModeEnum
import getpass
import io
import json
import logging
import os
from datetime import datetime, timedelta

class PewCapital(PersonalCapital):
    """
    Extends PersonalCapital to save and load session
    So that it doesn't require 2-factor auth every time
    """
    def __init__(self):
        PersonalCapital.__init__(self)
        self.__session_file = 'session.json'

    def load_session(self):
        try:
            with open(self.__session_file) as data_file:    
                cookies = {}
                try:
                    cookies = json.load(data_file)
                except ValueError as err:
                    logging.error(err)
                self.set_session(cookies)
        except IOError as err:
            logging.error(err)

    def save_session(self):
        with open(self.__session_file, 'w') as data_file:
            data_file.write(json.dumps(self.get_session()))

def get_email():
    email = os.getenv('PEW_EMAIL')
    if not email:
        print('You can set the environment variables for PEW_EMAIL and PEW_PASSWORD so the prompts don\'t come up every time')
        return raw_input('Enter email:')
    return email

def get_password():
    password = os.getenv('PEW_PASSWORD')
    if not password:
        return getpass.getpass('Enter password:')
    return password

def main():
    email, password = get_email(), get_password()
    pc = PewCapital()
    pc.load_session()

    try:
        pc.login(email, password)
    except RequireTwoFactorException:
        pc.two_factor_challenge(TwoFactorVerificationModeEnum.SMS)
        pc.two_factor_authenticate(TwoFactorVerificationModeEnum.SMS, raw_input('code: '))
        pc.authenticate_password(password)

    accounts_response = pc.fetch('/newaccount/getAccounts')
    
    now = datetime.now()
    date_format = '%Y-%m-%d'
    days = 30
    start_date = (now - (timedelta(days=days+1))).strftime(date_format)
    end_date = (now - (timedelta(days=1))).strftime(date_format)
    transactions_response = pc.fetch('/transaction/getUserTransactions', {
        'sort_cols': 'transactionTime',
        'sort_rev': 'true',
        'page': '0',
        'rows_per_page': '100',
        'startDate': start_date,
        'endDate': end_date,
        'component': 'DATAGRID'
    })
    pc.save_session()





    accounts = accounts_response.json()['spData']
    print('Networth: {0}'.format(accounts['networth']))
    for i in accounts['accounts']:
        if i['currentBalance'] > 0:
            print((i['name']),'   ',i['currentBalance'])

    transactions = transactions_response.json()['spData']
    print('Number of transactions between {0} and {1}: {2}'.format(transactions['startDate'], transactions['endDate'], len(transactions['transactions'])))

    with io.open('alldata.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(transactions_response.json(), indent=4, separators=(',', ': '), ensure_ascii=False))
    
    with io.open('transactions.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(transactions, indent=4, separators=(',', ': '), ensure_ascii=False))

    with io.open('accounts_response.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(accounts, indent=4, separators=(',', ': '), ensure_ascii=False))

if __name__ == '__main__':
    main()
