import base64
import json
import os.path
import requests

import sys
sys.path.append('../common/src')
import utils

from flask import Flask, has_request_context, request
from flask_restful import Api, Resource, reqparse
from git import Repo

ROOT_PATH = "/var/tms-data"

# TODO: Unit testing, end-to-end testing

def write_post(post):
    title = "wp" + str(post['id'])
    filename = f"{ROOT_PATH}/source_files/en/{title}.json"
    with open(filename, 'w') as outfile:
        d = {}
        d['id'] = post['id']
        d['wptitle'] = post['title']
        d['content'] = post['content']
        d['link'] = post['link']
        d['modified_gmt'] = post['modified_gmt']
        json.dump(d, outfile)

def get_posts():
    import_url = os.environ.get('WP_IMPORT_URL')
    url = f"{import_url}/wp-json/wp/v2/posts"
    user = os.environ.get('WP_IMPORT_USER')
    password = os.environ.get('WP_IMPORT_PASSWORD')
    credentials = user + ':' + password
    token = base64.b64encode(credentials.encode())

    header = {'Authorization': 'Basic ' + token.decode('utf-8'), 'User-Agent': "", }
    response = requests.get(url, headers=header )
    return response.json()

def do_work():
    for post in get_posts():
        """
        Example wp link: 'https://ctoassetsstg.wpengine.com/es/2020/10/09/aditya-another-test-post/'

        If there is a locale specified like `es` in the above link, then we do not want to import it as it is an already translated post.
        Note: This logic does not support a non-english source language.
        """
        split_link = post['link'].split('/')
        if len(split_link[3]) == 2:
            print(f"Will not import translated post - ID: {post['id']} Title: {post['title']} Link: {post['link']}")
            continue

        write_post(post)
    utils.git_push(utils.PROJECT_ROOT_GIT_PATH, commit_message="Update shared repository: wordpress", enable_push=True, origin='import-wp')

app = Flask(__name__)
api = Api(app)

class WordpressUpdateListener(Resource):
    def get(self):
        try:
            do_work()
            return {"success": True}
        except Exception as error:
            message = f"Something went wrong: {error}"
            return {"success": False, "error_message": message}

    def post(self):
        try:
            do_work()
            return {"success": True}
        except Exception as error:
            message = f"Something went wrong: {error}"
            return {"success": False, "error_message": message}

api.add_resource(WordpressUpdateListener, "/wp-updates")

if __name__ == "__main__":
    # Warning: When debug mode is unsafe. Attackers can use it to run arbitrary python code.
    app.run(debug=False, host='0.0.0.0')
