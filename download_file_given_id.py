from __future__ import print_function
import os.path
import io
import sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseDownload

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SAMPLE_ID = '1Q00HQCnAyKnbhcIlAjRleD89lwI7NaFG'

def authenticate():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
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
    return creds

def download_file_given_file_id(file_id):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    file_name = service.files().get(fileId=file_id).execute()['name']
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(file_name, mode='wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        download_file_given_file_id(file_id=SAMPLE_ID)
    elif len(sys.argv) == 2:
        download_file_given_file_id(file_id=sys.argv[1])
    else:
        print('Wrong number of arguments')
        print('Usage -> python download_file_give_id.py <drive_file_id>')
