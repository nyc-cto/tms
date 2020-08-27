from __future__ import print_function
import json
import pickle
import os.path
from apiclient import discovery
from httplib2 import Http
from oauth2client import client
from oauth2client import file
from oauth2client import tools
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
SCOPES_DOC = ['https://www.googleapis.com/auth/documents.readonly']
DISCOVERY_DOC = ('https://docs.googleapis.com/$discovery/rest?'
                         'version=v1')

def read_paragraph_element(element):
    """Returns the text in the given ParagraphElement.

        Args:
            element: a ParagraphElement from a Google Doc.
    """
    text_run = element.get('textRun')
    if not text_run:
        return ''
    return text_run.get('content')


def read_strucutural_elements(elements):
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
                    text += read_strucutural_elements(cell.get('content'))
        elif 'tableOfContents' in value:
            # The text in the TOC is also in a Structural Element.
            toc = value.get('tableOfContents')
            text += read_strucutural_elements(toc.get('content'))
    return text


store = file.Storage('secrets/token_read.json')
page_token = None   
creds = None
flow = client.flow_from_clientsecrets('secrets/credentials.json', SCOPES)
if os.path.exists('secrets/token_read.pickle'):
    with open('secrets/token_read.pickle', 'rb') as token:
        creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
if not creds or creds.invalid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = client.flow_from_clientsecrets('secrets/credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    # Save the credentials for the next run
    with open('secrets/token_read.pickle', 'wb') as token:
        pickle.dump(creds, token)
service_drive = build('drive', 'v3', credentials=creds)
file_ids = []
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

store = file.Storage('secrets/token.json')
creds_doc = store.get()
if not creds_doc or creds_doc.invalid:
    flow_doc = client.flow_from_clientsecrets('secrets/credentials.json', SCOPES_DOC)
    creds_doc = tools.run_flow(flow_doc, store)
service_docs = discovery.build('docs', 'v1', http=creds_doc.authorize(Http()), discoveryServiceUrl=DISCOVERY_DOC)
for file_id in file_ids:
    result = service_docs.documents().get(documentId=file_id).execute()
    content = read_strucutural_elements(result.get('body').get('content'))
    title = result.get('title')
    root_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
    filename = f"{root_path}/shared_directory/{title}.json"
    with open(filename, 'w') as outfile:
        d = {}
        d['title'] = title
        d['content'] = content
        json.dump(d, outfile)
