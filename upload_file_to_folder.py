from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.client import OAuth2Credentials
import json
import sys

FOLDER_ID='--your-folder-id--'
FILE_NAME='file-name.ext'

def load_saved_credentials():
    with open('token.json','r') as cred_file:
        creds = json.load(cred_file)
    creds['access_token'] = creds['token']
    creds['token_expiry'] = creds['expiry']
    creds['user_agent'] = 'nil'
    creds['invalid'] = 'nil'
    return json.dumps(creds)

def upload_file_to_folder(folder_id=FOLDER_ID,file_name=FILE_NAME):
    gauth = GoogleAuth()
    gauth.credentials = OAuth2Credentials.from_json(load_saved_credentials())
    drive = GoogleDrive(gauth)

    file = drive.CreateFile({'parents': [{'id': folder_id}]})
    file.SetContentFile(file_name)
    file.Upload()
    print('Created file %s in Drive with mimeType %s' % (file['title'], file['mimeType']))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        upload_file_to_folder()
    elif len(sys.argv) == 3:
        upload_file_to_folder(folder_id=sys.argv[1], file_name=sys.argv[2])
    else:
        print('Wrong number of arguments')
        print('Usage -> python upload_file_to_folder.py <folder_id> <file_name>')
