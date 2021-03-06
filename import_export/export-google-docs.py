import json
import pickle
import os.path
from git import Repo
import yaml
from google_doc_utils import generate_secrets

import sys
sys.path.append('translation_service/src')
sys.path.append('common/src')
from po_file import PoFile
import utils

SCOPE_READ_DRIVE = ['https://www.googleapis.com/auth/drive']
SCOPE_READ_DOCS = ['https://www.googleapis.com/auth/documents']

SOURCE_PATH = 'source_files/en'
GIT_BRANCH = f"{os.environ.get('DEVELOPER_USERNAME')}/{os.environ.get('ENV')}/local"
ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../tms-data'))
GIT_REPO_PATH = f'{ROOT_PATH}/.git'
COMMIT_MESSAGE = 'Update shared repository'

UPDATE_URL_ROOT = 'https://docs.googleapis.com/v1/documents'


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
    non_en_folders = [translation_mapping['language_folders'][lang] for lang in translation_mapping['language_folders'] if lang != 'en']
    
    # Generate secrets, if not already generated
    service_drive = generate_secrets('drive')
    service_docs = generate_secrets('docs')

    # Obtain IDs of Google docs
    # And delete stale translated content 
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
            
            # Delete translated files in Google docs to make space for new translations
            if file_parents and any(folder in non_en_folders for folder in file_parents):
                print(f"deleting file {file_id}")
                service_drive.files().delete(fileId=file_id).execute()
            
            # Map English files' names to Google doc ID
            # So we know which document each .po file corresponds to
            if file_parents and translation_mapping['language_folders']['en'] in file_parents:
                file_name_id_map[file_name] = file_id
        
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break 

    for root, dirs, files in os.walk(f'{root_path}'):
        for f in files:
            # Parse language and file name from .po file path
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
                        # Map each original piece of text to its translated content
                        id_str_mapping = {el.get_msgid_text(): el.get_msgstr_text() for el in po.msg_elements}
                        
                        # Create a new file in the target language folder that's a copy of the English file to translate
                        # And move it to the target language folder
                        newfile = {'name': file_name, 'parents' : [translation_mapping['language_folders'][folder_lang]]}
                        print(f"Copying document {file_name} over to {folder_lang} folder")
                        response_copy = service_drive.files().copy(fileId=file_name_id_map[file_name], body=newfile).execute()
                        target_doc_id = response_copy["id"]
                        
                        # Replace the English content in the copied over file
                        # With the translated content
                        # Iterate through msgid_text values in descending length order
                        # So that individual word translations don't interfere with longer phrases containing the word
                        for msgid_text in sorted(id_str_mapping, key=len, reverse=True):
                            msgid_str = id_str_mapping[msgid_text]
                            print(f"replacing in doc {target_doc_id} {msgid_text} with {msgid_str}")
                            response_replace = translate_doc(service_docs, target_doc_id, msgid_text, msgid_str)
                    except Exception as error:
                        print(f"Error occurred while adding translated files back to language folder. {error}")
                        pass
if __name__ == "__main__":
    main()
