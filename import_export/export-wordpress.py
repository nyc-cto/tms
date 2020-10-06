import base64
import json
import os.path
import os
import requests

import sys
sys.path.append('../common/src')
import utils

from flask import Flask, has_request_context, request
from flask_restful import Api, Resource, reqparse
from git import Repo

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


def export_wordpress():

  # Get the latest commit?
  export_url = os.environ.get('EXPORT_URL')
  

  repo = Repo(GIT_REPO_PATH)
  t = repo.head.commit.tree
  repo.index.add([SOURCE_PATH])
  if repo.git.diff(t):
      # repo.index.commit(COMMIT_MESSAGE)
      print(f"Pushing files to branch {GIT_BRANCH}")
      # repo.git.push('origin', GIT_BRANCH)
      print("Push successful")
  else:
      print("No changes detected")
  # id = 25
  # lang = "fr"

  # url = f"{export_url}/wp-json/elsa/v1/translate/{id}/{lang}"

  # user = os.environ.get('EXPORT_USER')
  # password = os.environ.get('EXPORT_PASSWORD')
  # credentials = user + ':' + password
  # token = base64.b64encode(credentials.encode())
  # header = {'Authorization': 'Basic ' + token.decode('utf-8')}

  # response = requests.post(url, headers=header, json=sample_json)
  # return {"status": "success"}

if __name__ == "__main__":
  # Warning: When debug mode is unsafe. Attackers can use it to run arbitrary python code.
  export_wordpress()
