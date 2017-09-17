from __future__ import print_function
import httplib2
import json
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = './credentials/client_secret_sheets_api.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    filename = 'data/transactions.json'

    with open(filename) as json_file:
        data = json.load(json_file)


    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1-7mEUS7tmeE6s_X3-WGDLLBc6U4TT0MH9zkk7AqEPL8'
    rangeName = 'Automated Expenses'
    
    values = [];
    
    """ A typical transaction, with reverse engineering comments
    "transactions": [
        {
            "userTransactionId": 3457310036,                                Unique ID            
            "cusipNumber": "",                                              ???
            "isEditable": true,                                             Can the user update the transaction
            "isCredit": false,                                              ???
            "hasViewed": false,                                             ???
            "transactionDate": "2017-05-28",                                Date
            "memo": "",                                                     User associated data
            "currency": "USD",                                              Currency 
            "merchantId": "WZ8zZ8GmQF5jloIurEzsg5R29hOdRzWhi8EJiemomb0",    ???
            "accountId": "5533673_8557423_14658696",                        Unique accountId ??
            "isIncome": false,                                              True if income ?
            "isNew": false,                                                 ???
            "isInterest": false,                                            ???
            "holdingType": "",                                              ???
            "accountName": "Credit Card - Ending in 9970",                  Name of related account
            "resultType": "aggregated",                                     ???
            "isSpending": true,                                             True if an expense ?
            "originalAmount": 14.6,                                         Amount of the expense
            "userAccountId": 14658696,                                      ???
            "price": 0.0,                                                   ???
            "transactionType": "Debit",                                     ???
            "merchant": "",                                                 ???
            "description": "Amazon.com",                                    Transaction description
            "symbol": "",                                                   ???
            "lotHandling": "",                                              ???
            "isCashOut": true,                                              Money was removed ?
            "isCashIn": false,                                              Money was added?
            "originalDescription": "Amazon.com",                            Transaction description (original?)
            "status": "posted",                                             Not pending anymore if "posted"
            "runningBalance": 0.0,                                          ???
            "netCost": 0.0,                                                 ???
            "checkNumber": "",                                              ???
            "isCost": false,                                                ???
            "categoryId": 13,                                               Related category id = getTransactionCategories
            "amount": 14.6,                                                 Amount (same as originalAmount?)
            "includeInCashManager": true,                                   ???
            "simpleDescription": "Amazon.com",                              Yet another description
            "isDuplicate": false                                            ???
        },
       // more entries
    """
    for entry in data["transactions"]:
        aPrice = entry["originalAmount"]
        aDate = entry["transactionDate"]
        aDescription = entry["originalDescription"]
        values.append([aDate, aPrice, aDescription])
    
    body = {
        'values': values
    }
    
    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheetId, range=rangeName, valueInputOption="USER_ENTERED", body=body).execute()

if __name__ == '__main__':
    main()
