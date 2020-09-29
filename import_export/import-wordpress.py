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
    # TODO: change this to point to prod website
    import_url = os.environ.get('IMPORT_URL')
    url = f"{import_url}/wp-json/wp/v2/posts"
    user = os.environ.get('IMPORT_USER')
    password = os.environ.get('IMPORT_PASSWORD')
    credentials = user + ':' + password
    token = base64.b64encode(credentials.encode())
    useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    header = {'Authorization': 'Basic ' + token.decode('utf-8'), 'User-Agent': useragent, }
    response = requests.get(url, headers=header )
    print (response.json())
    return response.json()

def do_work():
    for post in get_posts():
        write_post(post)
    utils.git_push(utils.PROJECT_ROOT_GIT_PATH, commit_message="Update shared repository: wordpress", enable_push=True)

app = Flask(__name__)
api = Api(app)

class WordpressUpdateListener(Resource):
    def get(self):
        do_work()
        return "Get"

    def post(self):
        do_work()
        return "Post"

api.add_resource(WordpressUpdateListener, "/wp-updates")

if __name__ == "__main__":
    # Warning: When debug mode is unsafe. Attackers can use it to run arbitrary python code.
    app.run(debug=False, host='0.0.0.0')
