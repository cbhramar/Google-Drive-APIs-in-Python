from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from oauth2client.client import OAuth2Credentials
import json
import sys

FOLDER_NAME='TrialFolder'
DOWNLOAD_FOLDER='folderdownloads'

def load_saved_credentials():
    with open('token.json','r') as cred_file:
        creds = json.load(cred_file)
    creds['access_token'] = creds['token']
    creds['token_expiry'] = creds['expiry']
    creds['user_agent'] = 'nil'
    creds['invalid'] = 'nil'
    return json.dumps(creds)

def download_all_files_in_folder(folder_name=FOLDER_NAME):
    gauth = GoogleAuth()
    gauth.credentials = OAuth2Credentials.from_json(load_saved_credentials())
    drive = GoogleDrive(gauth) 

    folder_id = 'nil'
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for file in file_list:
        if file['title'] == folder_name:
            folder_id = file['id']

    if folder_id == 'nil':
        print('Could not find folder: '+folder_name)
        return

    file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(folder_id)}).GetList()
    for file in file_list:
        if file['mimeType'] == 'application/vnd.google-apps.folder':
            print('Not downloading folder '+file['title'])
        else:
            file.GetContentFile(DOWNLOAD_FOLDER+'/'+file['title'])
            print('Downloaded file '+file['title'])

if __name__ == '__main__':
    ()
    if len(sys.argv) == 1:
        download_all_files_in_folder()
    elif len(sys.argv) == 2:
        download_all_files_in_folder(folder_name=sys.argv[1])
    else:
        print('Wrong number of arguments')
        print('Usage -> python download_all_files_in_folder.py <folder_name>')
