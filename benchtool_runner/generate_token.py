import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import codecs
import sys

#https://developers.google.com/sheets/api/quickstart/python

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = None

if len(sys.argv) >= 2 :
    SPREADSHEET_ID = sys.argv[1]
else:
    SPREADSHEET_ID = os.getenv('GOOGLE_SHEET_ID')
    
def main():

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if not os.path.exists('token'):
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        pickled = codecs.encode(pickle.dumps(creds), "base64").decode()
        print("Generated Token KEEP IT SAFE!")
        print(pickled)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    print('DONE!')

if __name__ == '__main__':
    main()