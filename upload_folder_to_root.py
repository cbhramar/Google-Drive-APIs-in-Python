from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.client import OAuth2Credentials
import json
import sys
import os

LOCAL_FOLDER_NAME='h5downloads'

def load_saved_credentials():
    with open('token.json','r') as cred_file:
        creds = json.load(cred_file)
    creds['access_token'] = creds['token']
    creds['token_expiry'] = creds['expiry']
    creds['user_agent'] = 'nil'
    creds['invalid'] = 'nil'
    return json.dumps(creds)

def get_authenticated_service():
    gauth = GoogleAuth()
    gauth.credentials = OAuth2Credentials.from_json(load_saved_credentials())
    drive = GoogleDrive(gauth)
    return drive

def upload_folder_to_root(local_folder=LOCAL_FOLDER_NAME):
    drive = get_authenticated_service()
    empty_folder = drive.CreateFile({'title': local_folder, 
        'mimeType': 'application/vnd.google-apps.folder'})
    empty_folder.Upload()

    os.chdir(os.getcwd()+'/'+local_folder)
    for filename in os.listdir(os.getcwd()):
        file = drive.CreateFile({'parents': [{'id': empty_folder['id']}]})
        file.SetContentFile(filename)
        file.Upload()
        print('Uploaded ' + filename)

    print('Created folder %s in Drive' % (local_folder))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        upload_folder_to_root()
    elif len(sys.argv) == 2:
        upload_folder_to_root(local_folder=sys.argv[1])
    else:
        print('Wrong number of arguments')
        print('Usage -> python upload_folder_to_root.py <local_folder>')
