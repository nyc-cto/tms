import json
import pickle
import os.path
from time import sleep
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from git import Repo

SCOPE_DRIVE = ['https://www.googleapis.com/auth/drive']
SCOPE_DOCS = ['https://www.googleapis.com/auth/documents']

ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
GIT_REPO_PATH = f'{ROOT_PATH}/.git'
COMMIT_MESSAGE = 'Update shared repository'

def git_push():
    repo = Repo(GIT_REPO_PATH)
    t = repo.head.commit.tree
    repo.index.add(["shared_directory"])
    if repo.git.diff(t):
        repo.index.commit(COMMIT_MESSAGE)
        print("Pushing files to shared repository")
        repo.git.push('origin', 'master')
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

def generate_secrets(token_pickle_path, credentials_path, scope):
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
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, scope)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_pickle_path, 'wb') as token:
            pickle.dump(creds, token)
    if scope == SCOPE_DRIVE:
        service = build('drive', 'v3', credentials=creds)
    elif scope == SCOPE_DOCS:
        service = build('docs', 'v1', credentials=creds)
    else:
        service = None
    return service


def run():
    # Generate secrets, if not already generated
    service_drive = generate_secrets(
        'secrets/credentials_drive.pickle',
        'secrets/credentials_drive.json',
        SCOPE_DRIVE
        )
    service_docs = generate_secrets(
        'secrets/credentials_docs.pickle',
        'secrets/credentials_docs.json',
        SCOPE_DOCS
        )


    # Find ids of all Google docs in the raw Serge folder
    print("Finding documents")
    file_ids = []
    page_token = None
    while True:
        response = service_drive.files().list(q="name contains 'Raw_Document'",
                                              spaces='drive',
                                              fields='nextPageToken, files(id, name)',
                                              pageToken=page_token).execute()
        for file_content in response.get('files', []):
            # Process change
            file_id = file_content.get('id')
            file_ids.append(file_id)
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break 

    print("Obtaining document contents")
    # For each file, get contents
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

    # Push shared repository to Git if any files changed  
    git_push()

def main():
    while True:
        run()
        sleep(10)

if __name__ == "__main__":
    main()