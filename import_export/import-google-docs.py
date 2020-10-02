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

SCOPE_READ_DRIVE = ['https://www.googleapis.com/auth/drive.metadata.readonly']
SCOPE_READ_DOCS = ['https://www.googleapis.com/auth/documents.readonly']

SOURCE_PATH = 'source_files/en'
GIT_BRANCH = os.environ.get('TMS_DATA_BRANCH_NAME')
ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../tms-data'))
GIT_REPO_PATH = f'{ROOT_PATH}/.git'
COMMIT_MESSAGE = 'Update shared repository'

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


lang_folder_map = {
    "en": "1JTQuEBkzNbceyHUZYi5XeS0Qrf-8l9bh",
    "es": "1GAi6ZQkzsi9Mla4zsKAjYKsZ9AxeIfvu"
}   

def main():
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

    # Find ids of all Google docs in the raw Serge folder
    print("Finding documents")
    file_ids = []
    page_token = None
    while True:
        response = service_drive.files().list(spaces='drive',
                                              fields='nextPageToken, files(id, name, parents)',
                                              pageToken=page_token).execute()
        for file_content in response.get('files', []):
            # Process change
            file_parents = file_content.get('parents')
            if file_parents and lang_folder_map['en'] in file_parents:
                print(f"Found file {file_content.get('name')} with id {file_content.get('id')} and parents {file_content.get('parents')}")
                file_id = file_content.get('id')
                file_ids.append(file_id)
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break 

    print("Obtaining document contents")
    # For each file, get contents
    for file_id in file_ids:
        result = service_docs.documents().get(documentId=file_id).execute()
        result = json.loads(json.dumps(result)
            .replace('\\n', '')
            .replace('\\u2019', "'")
            )
        filename = f"{ROOT_PATH}/{SOURCE_PATH}/{result.get('title')}.json"
        with open(filename, 'w') as outfile:
            json.dump(result, outfile)

    # Push shared repository to Git if any files changed  
    git_push()


if __name__ == "__main__":
    main()
