from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.client import OAuth2Credentials
import json
import sys
import os

DRIVE_PARENT_ID='1vt2dessm3-rjhFmgAcO0jLdVeue-zkph'
DRIVE_PARENT_NAME='TrialFolder'
ROOT='root'
LOCAL_FOLDER_NAME='files'

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

def get_folder_id(drive_parent_folder=DRIVE_PARENT_NAME):
    drive = get_authenticated_service()
    folder_id = 'nil'
    folders = drive.ListFile({'q': "'{}' in parents and trashed=false".format(ROOT)}).GetList()
    for folder in folders:
        if folder['title'] == drive_parent_folder:
            folder_id = folder['id']
    return folder_id

def upload_folder_to_folder(local_folder=LOCAL_FOLDER_NAME,drive_parent_folder=DRIVE_PARENT_NAME):
    drive = get_authenticated_service()
    parent_id = get_folder_id(drive_parent_folder)
    empty_folder = drive.CreateFile({'title': local_folder, 
        'mimeType': 'application/vnd.google-apps.folder', 'parents': [{'id': parent_id}]})
    empty_folder.Upload()

    os.chdir(os.getcwd()+'/'+local_folder)
    for filename in os.listdir(os.getcwd()):
        file = drive.CreateFile({'parents': [{'id': empty_folder['id']}]})
        file.SetContentFile(filename)
        file.Upload()
        print('Uploaded ' + filename)

    print('Created folder %s in Drive under %s' % (local_folder, drive_parent_folder))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        upload_folder_to_folder()
    elif len(sys.argv) == 3:
        upload_folder_to_folder(local_folder=sys.argv[1], drive_parent_folder=sys.argv[2])
    else:
        print('Wrong number of arguments')
        print('Usage -> python upload_folder_to_folder.py <local_folder> <drive_parent_folder>')
