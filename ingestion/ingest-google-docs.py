from __future__ import print_function
import json
import pickle
import os.path
from time import sleep
from apiclient import discovery
from httplib2 import Http
from oauth2client import client
from oauth2client import file
from oauth2client import tools
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from git import Repo

SCOPES_READ_DRIVE = ['https://www.googleapis.com/auth/drive.metadata.readonly']
SCOPES_READ_DOCS = ['https://www.googleapis.com/auth/documents.readonly']
DISCOVERY_DOC = ('https://docs.googleapis.com/$discovery/rest?'
                         'version=v1')

ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
GIT_REPO_PATH = f'{ROOT_PATH}/.git'
COMMIT_MESSAGE = 'Update shared repository'

def git_push():
    repo = Repo(GIT_REPO_PATH)
    repo.index.add(["shared_directory"])
    repo.index.commit(COMMIT_MESSAGE)
    repo.git.push('origin', 'feature_docs_api') 

def read_paragraph_element(element):
    """Returns the text in the given ParagraphElement.

        Args:
            element: a ParagraphElement from a Google Doc.
    """
    text_run = element.get('textRun')
    if not text_run:
        return ''
    return text_run.get('content')


def read_structural_elements(elements):
    """Recurses through a list of Structural Elements to read a document's text where text may be
        in nested elements.

        Args:
            elements: a list of Structural Elements.
    """
    text = ''
    for value in elements:
        if 'paragraph' in value:
            elements = value.get('paragraph').get('elements')
            for elem in elements:
                text += read_paragraph_element(elem)
        elif 'table' in value:
            # The text in table cells are in nested Structural Elements and tables may be
            # nested.
            table = value.get('table')
            for row in table.get('tableRows'):
                cells = row.get('tableCells')
                for cell in cells:
                    text += read_structural_elements(cell.get('content'))
        elif 'tableOfContents' in value:
            # The text in the TOC is also in a Structural Element.
            toc = value.get('tableOfContents')
            text += read_structural_elements(toc.get('content'))
    return text


def run():
    # Generate secrets, if not already generated
    store_read_drive = file.Storage('secrets/token_read_drive.json')
    creds_read_drive = store_read_drive.get()
    page_token = None   
    flow = client.flow_from_clientsecrets('secrets/credentials.json', SCOPES_READ_DRIVE)
    if os.path.exists('secrets/token_read_drive.pickle'):
        with open('secrets/token_read_drive.pickle', 'rb') as token:
            creds_read_drive = pickle.load(token)
            # If there are no (valid) credentials available, let the user log in.
    if not creds_read_drive or creds_read_drive.invalid:
        if creds_read_drive and creds_read_drive.expired and creds_read_drive.refresh_token:
            creds_read_drive.refresh(Request())
        else:
            flow = client.flow_from_clientsecrets('secrets/credentials.json', SCOPES_READ_DRIVE)
            creds_read_drive = tools.run_flow(flow, store)
        # Save the credentials for the next run
        with open('secrets/token_read_drive.pickle', 'wb') as token:
            pickle.dump(creds_read_drive, token)
    service_drive = build('drive', 'v3', credentials=creds_read_drive)
    file_ids = []

    # Enumerate over Google doc ids and fetch content
    creds_read_docs = None
    # if not creds_read_docs or creds_read_docs.invalid:
    #     flow_doc = client.flow_from_clientsecrets('secrets/credentials.json', SCOPES_READ_DOCS)
    #     creds_read_docs = tools.run_flow(flow_doc, store)
    # service_docs = discovery.build('docs', 'v1', http=creds_read_docs.authorize(Http()), discoveryServiceUrl=DISCOVERY_DOC)

    if os.path.exists('secrets/token_read_docs.pickle'):
        with open('secrets/token_read_docs.pickle', 'rb') as token:
            creds_read_docs = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
    if not creds_read_docs or not creds_read_docs.valid:
        if creds_read_docs and creds_read_docs.expired and creds_read_docs.refresh_token:
            creds_read_docs.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'secrets/credentials.json', SCOPES_READ_DOCS)
            creds_read_docs = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('secrets/token_read_docs.pickle', 'wb') as token:
            pickle.dump(creds_read_docs, token)

    service_docs = build('docs', 'v1', credentials=creds_read_docs)

    # Find ids of all Google docs in the raw Serge folder
    while True:
        response = service_drive.files().list(q="name contains 'Raw_Document'",
                                              spaces='drive',
                                              fields='nextPageToken, files(id, name)',
                                              pageToken=page_token).execute()
        for file_content in response.get('files', []):
            # Process change
            file_id = file_content.get('id')
            print('Found file: %s (%s)' % (file_content.get('name'), file_id))
            file_ids.append(file_id)
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break 

    for file_id in file_ids:
        result = service_docs.documents().get(documentId=file_id).execute()
        content = read_structural_elements(result.get('body').get('content'))
        title = result.get('title')
        filename = f"{ROOT_PATH}/shared_directory/en/{title}.json"
        with open(filename, 'w') as outfile:
            d = {}
            d['title'] = title
            d['content'] = content
            json.dump(d, outfile)

    # Push shared repository to Git
    print("Pushing files to shared repository")  
    git_push()

def main():
    while True:
        run()
        sleep(10)

if __name__ == "__main__":
    main()