import base64
import json
import os.path
import os
import requests
from requests.auth import HTTPBasicAuth
from git import Repo

import json

ROOT_PATH = "/var/tms-data"

sample_json = """{
   "content" : {
      "protected" : false,
      "rendered" : "\n<p>Texto regular<\/p>\n\n\n\n<p><strong>Texto en negrita<\/strong><\/p>\n\n\n\n<p>Imagen de abajo:<\/p>\n\n\n\n<figure class=\"wp-block-image size-large is-style-default\"><img loading=\"lazy\" width=\"374\" height=\"238\" src=\"http:\/\/ctoassetsstg.wpengine.com\/wp-content\/uploads\/2020\/10\/Screen-Shot-2020-10-01-at-12.14.07-PM.png\" alt=\"\" class=\"wp-image-25\" srcset=\"https:\/\/ctoassetsstg.wpengine.com\/wp-content\/uploads\/2020\/10\/Screen-Shot-2020-10-01-at-12.14.07-PM.png 374w, https:\/\/ctoassetsstg.wpengine.com\/wp-content\/uploads\/2020\/10\/Screen-Shot-2020-10-01-at-12.14.07-PM-300x191.png 300w\" sizes=\"(max-width: 374px) 100vw, 374px\" \/><\/figure>\n\n\n\n<p>Este texto está debajo de la imagen del Empire State Building.<\/p>\n\n\n\n<p>Aquí hay una lista con dos viñetas:<\/p>\n\n\n\n<ul><li>Bala 1<\/li><li>Bala 2<\/li><\/ul>\n"
   },
   "id" : 24,
   "link" : "https:\/\/ctoassetsstg.wpengine.com\/2020\/10\/01\/second-post\/",
   "modified_gmt" : "2020-10-01T11:15:22",
   "wptitle" : {
      "rendered" : "Segunda publicación"
   }
}
"""


SOURCE_PATH = 'source_files/en'
GIT_BRANCH = f"{os.environ.get('DEVELOPER_USERNAME')}/{os.environ.get('ENV')}/local"
ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../tms-data'))
GIT_REPO_PATH = f'{ROOT_PATH}/.git'
COMMIT_MESSAGE = 'Update shared repository'

SOURCE_DIRECTORY = 'source_files'
SOURCE_LANGUAGE = 'en'

def export_wordpress():
  try:
    # Get the latest commit?
    repo = Repo(GIT_REPO_PATH)
    commits_list = list(repo.iter_commits())

    a_commit = commits_list[0]
    b_commit = commits_list[-1]

    diffs = a_commit.diff(b_commit)
    files = [f.a_path for f in diffs]

    for f in files:
      if f.startswith(f"{SOURCE_DIRECTORY}"):
        if not f.startswith(f"{SOURCE_PATH}"):
          target = f"{ROOT_PATH}/{f}"
          basename = os.path.basename(target)
          if basename.startswith("wp"):
            # print(target)
            with open(target, "rb") as json_file:
              filename, file_extension = os.path.splitext(basename)

              data = json.load(json_file)
              id = data["id"]
              title = data["wptitle"]["rendered"]
              content = data["content"]["rendered"]
              lang =  file_extension[1:]

              if title is not None and title != '':
                update_wordpress(id, lang, title, content)
  except Exception as error:
    print(f"ErrorExportToWordpress - Unable to add translated posts back into WP: {error}")

def update_wordpress(id, language, title, content, excerpt=""):
  export_url = os.environ.get('WP_EXPORT_URL')
  message = {
      "content": content,
      "title": title,
      "excerpt": excerpt,
      "status": "published"
  }
  url = f"{export_url}/wp-json/elsa/v1/translate/{id}/{language}"
  user = os.environ.get('WP_EXPORT_USER')
  password = os.environ.get('WP_EXPORT_PASSWORD')

  response = requests.post(url, headers={"Content-Type": "application/json", 'User-Agent': ""}, auth=HTTPBasicAuth(user, password), json=message)

  if not response.status_code == 201:
    raise Exception(f"Update wordpress failed- {response.json()}")

  print(f'Successfully updated post with ID: {id} Title: {title} Language: {language}')

  return {"status": "success"}


if __name__ == "__main__":
  # Warning: When debug mode is unsafe. Attackers can use it to run arbitrary python code.
  export_wordpress()
