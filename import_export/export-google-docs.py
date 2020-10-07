from __future__ import print_function
import json
import pickle
import os.path
from time import sleep
from httplib2 import Http
from oauth2client import client
from oauth2client import file
from oauth2client import tools
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from git import Repo
import yaml

import sys
sys.path.append('translation_service/src')
from po_file import PoFile

SCOPE_READ_DRIVE = ['https://www.googleapis.com/auth/drive']
SCOPE_READ_DOCS = ['https://www.googleapis.com/auth/documents']

SOURCE_PATH = 'source_files/en'
GIT_BRANCH = f"{os.environ.get('DEVELOPER_USERNAME')}/{os.environ.get('ENV')}/local"
ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../tms-data'))
GIT_REPO_PATH = f'{ROOT_PATH}/.git'
COMMIT_MESSAGE = 'Update shared repository'

UPDATE_URL_ROOT = 'https://docs.googleapis.com/v1/documents'

def git_push():
    repo = Repo(GIT_REPO_PATH)
    t = repo.head.commit.tree
    repo.index.add([SOURCE_PATH])
    if repo.git.diff(t):
        repo.index.commit(COMMIT_MESSAGE)
        print(f"Pushing files to branch {GIT_BRANCH}")
        repo.git.push('origin', GIT_BRANCH)
        print("Push successful")
    else:
        print("No changes detected")

def read_paragraph_element(element):
    """Returns the text in the given ParagraphElement.

        Args:
            element: a ParagraphElement from a Google Doc.
    """
    text_run = element.get('textRun')
    if not text_run:
        return ''
    return text_run.get('content')



def generate_secrets(token_pickle_path, raw_token_path, credentials_path, scope):
    # Generate secrets to access Google API, if not already generated, otherwise load in 
    creds = None
    if os.path.exists(token_pickle_path):
        with open(token_pickle_path, 'rb') as token:
            creds = pickle.load(token)
    # If there are no credentials available, let the user log in.
    if not creds:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = client.flow_from_clientsecrets(credentials_path, scope)
            store = file.Storage(raw_token_path)
            creds = tools.run_flow(flow, store)
        # Save the credentials for the next run
        with open(token_pickle_path, 'wb') as token:
            pickle.dump(creds, token)
    if scope == SCOPE_READ_DRIVE:
        service = build('drive', 'v3', credentials=creds)
    elif scope == SCOPE_READ_DOCS:
        service = build('docs', 'v1', credentials=creds)
    else:
        service = None
    return service



def translate_doc(service_docs, doc_id, msgid_text, msgid_str):
    payload = {
      "requests": [
        {
          "replaceAllText": {
            "containsText": {
                "matchCase": False,
                "text": msgid_text
            },
            "replaceText": msgid_str
          }
        }
      ]
    }
    request = service_docs.documents().batchUpdate(documentId=doc_id, body=payload)
    response = request.execute()
    return response

def main():
    root_path = '/var/tms/serge/ts'
    translation_mapping = None
    with open(os.environ.get('GOOGLE_DRIVE_CONFIG')) as f:
        translation_mapping = yaml.load(f)
    # Generate secrets, if not already generated
    service_drive = generate_secrets(
        'secrets/token_read_drive.pickle',
        'secrets/token_read_drive.json',
        'secrets/credentials_drive.json',
        SCOPE_READ_DRIVE
        )
    service_docs = generate_secrets(
        'secrets/token_read_docs.pickle',
        'secrets/token_read_docs.json',
        'secrets/credentials_docs.json',
        SCOPE_READ_DOCS
        )

    
    print("Finding documents")
    file_name_id_map = {}
    page_token = None
    while True:
        response = service_drive.files().list(spaces='drive',
                                              fields='nextPageToken, files(id, name, parents)',
                                              pageToken=page_token).execute()
        for file_content in response.get('files', []):
            # Process change
            file_id = file_content.get('id')
            file_name = file_content.get('name')
            file_parents = file_content.get('parents')
            # Delete translated files in Google docs
            if file_parents and translation_mapping['language_folders']['es'] in file_parents:
                print(f"deleting file {file_id}")
                service_drive.files().delete(fileId=file_id).execute()
            if file_parents and translation_mapping['language_folders']['en'] in file_parents:
                file_name_id_map[file_name] = file_id
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break 

    for root, dirs, files in os.walk(f'{root_path}'):
        for f in files:
            if f.endswith('.po') and f != 'sample.json.po':
                full_file_path = os.path.join(root,f)
                path_parts = full_file_path.split('/')
                folder_lang = path_parts[-2]
                file_name = path_parts[-1].split('.json.po')[0]

                # exclude wordpress files (for future developers, make this logic more abstracted)
                if not file_name.startswith('wp'):
                    try:
                        po = PoFile(full_file_path)
                        po.parse_po_file()
                        id_str_mapping = {el.get_msgid_text(): el.get_msgstr_text() for el in po.msg_elements}
                        newfile = {'name': file_name, 'parents' : [translation_mapping['language_folders'][folder_lang]]}
                        print(f"Copying document {file_name} over to {folder_lang} folder")
                        response_copy = service_drive.files().copy(fileId=file_name_id_map[file_name], body=newfile).execute()
                        target_doc_id = response_copy["id"]
                        for msgid_text in id_str_mapping:
                            msgid_str = id_str_mapping[msgid_text]
                            print(f"replacing in doc {target_doc_id} {msgid_text} with {msgid_str}")
                            response_replace = translate_doc(service_docs, target_doc_id, msgid_text, msgid_str)
                    except:
                        pass
if __name__ == "__main__":
    main()
