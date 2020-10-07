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
from google_doc_utils import generate_secrets

import sys
sys.path.append('common/src')
import utils

SOURCE_PATH = 'source_files/en'
GIT_BRANCH = os.environ.get('TMS_DATA_BRANCH_NAME')
ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../tms-data'))
GIT_REPO_PATH = f'{ROOT_PATH}/.git'
COMMIT_MESSAGE = 'Update shared repository'


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
 

def main():
    translation_mapping = None
    with open(os.environ.get('GOOGLE_DRIVE_CONFIG')) as f:
        translation_mapping = yaml.load(f)

    # Generate secrets, if not already generated
    service_drive = generate_secrets('drive')
    service_docs = generate_secrets('docs')

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
            if file_parents and translation_mapping['language_folders']['en'] in file_parents:
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
    utils.git_push(utils.PROJECT_ROOT_GIT_PATH, commit_message="Update shared repository: Google docs", enable_push=True)


if __name__ == "__main__":
    main()
