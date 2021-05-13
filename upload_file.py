from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.client import OAuth2Credentials
import json
import sys

SAMPLE_FILE='create_file.py'

def load_saved_credentials():
    with open('token.json','r') as cred_file:
        creds = json.load(cred_file)
    creds['access_token'] = creds['token']
    creds['token_expiry'] = creds['expiry']
    creds['user_agent'] = 'nil'
    creds['invalid'] = 'nil'
    return json.dumps(creds)

def upload_file(file_name=SAMPLE_FILE):
    gauth = GoogleAuth()
    gauth.credentials = OAuth2Credentials.from_json(load_saved_credentials())
    drive = GoogleDrive(gauth)

    file = drive.CreateFile()
    file.SetContentFile('create_file.py')
    file.Upload()
    print('Created file %s in Drive with mimeType %s' % (file['title'], file['mimeType']))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        upload_file()
    elif len(sys.argv) == 2:
        upload_file(file_name=sys.argv[1])
    else:
        print('Wrong number of arguments')
        print('Usage -> python upload_file.py <file_name>')
