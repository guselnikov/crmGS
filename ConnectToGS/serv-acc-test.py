import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
path_json = 'credentials-serv-acc.json'

creds_auth = ServiceAccountCredentials\
    .from_json_keyfile_name(path_json, ['https://www.googleapis.com/auth/spreadsheets',
                                        'https://www.googleapis.com''/auth/drive'])\
    .authorize(httplib2.Http())

service = build('sheets', 'v4', http=creds_auth)

sheet_id = '1k40lGVdZNvytbByH2Ap45ojFGJfjLrG-MIQEBIUVIJY'

sss = service.spreadsheets()

r = sss.values().get(spreadsheetId=sheet_id, range='A2:E').execute()
print(r)
