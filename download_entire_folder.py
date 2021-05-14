from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from oauth2client.client import OAuth2Credentials
import json
import sys
import os

FOLDER_NAME='TrialFolder'
PARENT_FOLDER='root'
DOWNLOAD_FOLDER='folderdownloads'

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

def get_folder_id(folder_name=FOLDER_NAME,parent_folder=PARENT_FOLDER):
    drive = get_authenticated_service()
    folder_id = 'nil'
    file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(parent_folder)}).GetList()
    for file in file_list:
        if file['title'] == folder_name:
            folder_id = file['id']
    return folder_id

def download_entire_folder(folder_name=FOLDER_NAME,parent_folder=PARENT_FOLDER):
    folder_id = get_folder_id(folder_name=folder_name,parent_folder=parent_folder)
    drive = get_authenticated_service()

    if folder_id == 'nil':
        print('Could not find folder: '+folder_name)
        return

    file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(folder_id)}).GetList()
    for file in file_list:
        dirpath = './'+DOWNLOAD_FOLDER+'/'
        if not file['mimeType'] == 'application/vnd.google-apps.folder':
            dirpath = dirpath + folder_name
            print('Downloading file ' + file['title'] + ' to ' + dirpath)
            if not os.path.isdir(dirpath):
                os.mkdir(dirpath)
            file.GetContentFile(dirpath+'/'+file['title'])
        else:
            download_entire_folder(folder_name=file['title'],parent_folder=folder_id)
            print('Downloading folder ' + file['title'] + ' to ' + dirpath)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        download_entire_folder()
    elif len(sys.argv) == 2:
        download_entire_folder(folder_name=sys.argv[1])
    else:
        print('Wrong number of arguments')
        print('Usage -> python download_entire_folder.py <folder_name>')
