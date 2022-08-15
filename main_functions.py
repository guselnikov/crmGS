from __future__ import print_function

from pprint import pprint
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient import discovery


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

creds = None

if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())


# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1k40lGVdZNvytbByH2Ap45ojFGJfjLrG-MIQEBIUVIJY'

def get_values(sample_range_name):
    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=sample_range_name).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        print('Data from range:')
        for row in values:
            print(row)
    except HttpError as err:
        print(err)

def new_sheet(title):
    try:
        service = build('sheets', 'v4', credentials=creds)

        spreadsheet = {
            'properties': {
                'title': title
            }
        }
        spreadsheet = service.spreadsheets().create(body=spreadsheet,
                                                    fields='spreadsheetId') \
            .execute()
        print(f"Spreadsheet URL: https://docs.google.com/spreadsheets/d/{(spreadsheet.get('spreadsheetId'))}/edit")
        return spreadsheet.get('spreadsheetId')
    except HttpError as err:
        print(err)

def create_spreadsheet():
    service = discovery.build('sheets', 'v4', credentials=creds)

    spreadsheet_body = {

    }

    request = service.spreadsheets().create(body=spreadsheet_body)
    response = request.execute()

    pprint(response)

def main():
    option = input('Choose option and enter it: {new_sheet}, {get}: ')
    if option == 'new_sheet':
        title = input('Enter title for new sheet: ')
        new_sheet(title)

    if option == 'get':
        range_of_table_get = input('Enter range in A1 notation: ')
        get_values(range_of_table_get)

text = 'ddd'

if __name__ == '__main__':
    main()