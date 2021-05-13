from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from oauth2client.client import OAuth2Credentials
import json

def load_saved_credentials():
    with open('token.json','r') as cred_file:
        creds = json.load(cred_file)
    creds['access_token'] = creds['token']
    creds['token_expiry'] = creds['expiry']
    creds['user_agent'] = 'nil'
    creds['invalid'] = 'nil'
    return json.dumps(creds)

def list_files():
    gauth = GoogleAuth()
    gauth.credentials = OAuth2Credentials.from_json(load_saved_credentials())
    drive = GoogleDrive(gauth) 

    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for file in file_list:
        print('title: %s, id: %s' % (file['title'], file['id']))


if __name__ == '__main__':
    list_files()
