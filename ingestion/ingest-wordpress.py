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


ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))

# TODO: Unit testing, end-to-end testing

def write_post(post):
    title = "wp" + str(post['id'])
    filename = f"{ROOT_PATH}/shared_directory/en/{title}.json"
    with open(filename, 'w') as outfile:
        d = {}
        d['id'] = post['id']
        d['wptitle'] = post['title']
        d['content'] = post['content']
        d['link'] = post['link']
        d['modified_gmt'] = post['modified_gmt']
        json.dump(d, outfile)

def get_posts():
    # TODO: change this to point to prod website
    url = "http://localhost:8888/wp-json/wp/v2/posts"
    user = "admin"
    password = "vmaC YpeW CxyA DjNJ k0Rd TPpM"
    credentials = user + ':' + password
    token = base64.b64encode(credentials.encode())
    header = {'Authorization': 'Basic ' + token.decode('utf-8')}
    response = requests.get(url, headers=header )
    return response.json()

def do_work():
    for post in get_posts():
        write_post(post)
    utils.git_push(utils.PROJECT_ROOT_GIT_PATH, commit_message="Update shared repository: wordpress", enable_push=False)


def do_export(id, lang, message):
    """
    This sends the tranlated item
    """
    export_url = os.environ.get('EXPORT_URL')

    url = f"{export_url}/wp-json/elsa/v1/translate/{id}/{lang}"

    user = os.environ.get('EXPORT_USER')
    password = os.environ.get('EXPORT_PASSWORD')
    credentials = user + ':' + password
    token = base64.b64encode(credentials.encode())
    header = {'Authorization': 'Basic ' + token.decode('utf-8')}

    response = requests.post(url, headers=header, json=message)
    return {"status": "success"}


app = Flask(__name__)
api = Api(app)

class WordpressUpdateListener(Resource):
    def get(self):
        do_work()
        return "Get"

    def post(self):
        do_work()
        return "Post"

class WordpressExportListener(Resource):
    """
    `WordpressExportListener` will be the endpoint to be triggered when we want to return something back to a 
    wordpress site. It requires the following body attributes:


    JSON
    {
        "id": ID of the source content, 
        "lang": target language code (ex. "fr"),
        "content": HTML content (ex. "<p>Bonjour le monde! Je suis Rapi Castillo</p>"),
        "title": Title of the translated content (ex. "Bonjour le monde!"),
        "excerpt": Excerpt of the translated content (ex. "Hello this is a french translation xx"),
        "status": "publish"
    }

    This will create/update the translated content.

    """
    def post(self):

        post_data = request.json
        id=post_data.get("id")
        lang=post_data.get("lang")
        message = {
            "content": post_data.get("content"),
            "title": post_data.get("title"),
            "excerpt": post_data.get("excerpt"),
            "status": post_data.get("status")
        }
        
        return do_export(id, lang, message)

api.add_resource(WordpressUpdateListener, "/wp-updates")
api.add_resource(WordpressExportListener, "/wp-export")


if __name__ == "__main__":
    # Warning: When debug mode is unsafe. Attackers can use it to run arbitrary python code.
    app.run(debug=False, host='0.0.0.0')

