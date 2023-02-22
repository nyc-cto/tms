import pickle
import os.path
from httplib2 import Http
from oauth2client import client
from oauth2client import file
from oauth2client import tools
from googleapiclient.discovery import build
from google.auth.transport.requests import Request


SCOPE_READ_DRIVE = ['https://www.googleapis.com/auth/drive']
SCOPE_READ_DOCS = ['https://www.googleapis.com/auth/documents']


def build_service(creds, scope):
    if scope == 'drive':
        service = build('drive', 'v3', credentials=creds)
    elif scope == 'docs':
        service = build('docs', 'v1', credentials=creds)
    else:
        service = None
    return service

def generate_secrets(scope):
    """
    Generate secrets to access Google API, if not already generated, otherwise load in 
    Input: scope of permissions for secrets (currently either drive or docs access)
    Output: a Google service object which can access and execute on the Drive/Docs API
    """
    token_pickle_path = f'secrets/token_read_{scope}.pickle'
    raw_token_path = f'secrets/token_read_{scope}.json'
    credentials_path = f'secrets/credentials_{scope}.json'
    creds = None
    if os.path.exists(token_pickle_path):
        with open(token_pickle_path, 'rb') as token:
            creds = pickle.load(token)
    # If there are no credentials available, let the user log in.
    if not creds:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            scope_to_send = SCOPE_READ_DRIVE if scope == 'drive' else SCOPE_READ_DOCS
            print('im here')
            flow = client.flow_from_clientsecrets(credentials_path, scope=scope_to_send, redirect_uri='http://127.0.0.1:8000')
            print(flow)
            print(flow.redirect_uri)
            print(dir(flow))
            store = file.Storage(raw_token_path)
            class Flag:
                auth_host_name = '127.0.0.1'
                auth_host_port = [8000]
                logging_level = 'INFO'
                noauth_local_webserver = False
            creds = tools.run_flow(flow, store, flags=Flag())
        # Save the credentials for the next run
        with open(token_pickle_path, 'wb') as token:
            pickle.dump(creds, token)
    service = build_service(creds, scope)
    return service