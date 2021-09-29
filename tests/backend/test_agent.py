import requests
import json
from typing import Union


class TestAgent:

    def __init__(self, username=None, password=None, root_url='http://127.0.0.1:8000/api', endpoint='/', headers={'Content-Type': 'application/json'}):
        

        self.root_url = root_url
        self.endpoint = root_url + endpoint

        if username is not None and password is not None:
            granted = requests.post(url=root_url + '/auth/token/', json={"username": username, "password": password}, headers=headers)

            assert granted.status_code <= 299, f'not authorized, code {granted.status_code}'

            self.headers = {**headers, 'Authorization': 'Bearer ' + granted.json()['access']}
        elif username is None and password is None:
            self.headers=headers
        else:
            raise Exception("Please include a username and password for an authenticated agent, otherwise leave both blank")

    def set_endpoint(self, endpoint):
        self.endpoint= self.root_url + endpoint

    def get(self, slug=''):
        return requests.get(url=self.endpoint + slug, headers=self.headers)

    def post(self, slug='', **kwargs):
        print(json.dumps(kwargs))
        return requests.post(url=self.endpoint + slug, json=kwargs, headers=self.headers)

    def patch(self, slug='', **kwargs):
        return requests.patch(url=self.endpoint + slug, json=kwargs, headers=self.headers)

    def delete(self, slug=''):
        return requests.delete(url=self.endpoint + slug, headers=self.headers)
