import requests
import json
from typing import Union


class TestAgent:
    root_url = 'http://127.0.0.1:8000/api'
    message_endpoint = root_url + '/messages/'
    headers = {'Content-Type': 'application/json'}
    usernames = ['meerkat', 'pangolin', 'badger']

    def _login(self, username):
        granted = requests.post(url=self.root_url + '/auth/token/',
                                data=json.dumps({"username": username, "password": "123456"}),
                                headers=self.headers).json()
        return {**self.headers, 'Authorization': 'Bearer ' + granted['access']}

    def __init__(self):
        self.logins = {usr: self._login(usr) for usr in self.usernames}

    def get(self, username: str, slug: Union[int, str]=0) -> dict:
        """
        Test's the API's GET method. username is mandatory, pass the user who's mailbox you want to see slug is
        optional, pass the id of the message you want to read, or pass a string representing the parts of the mailbox
        you want to see. Tested with: 'all', 'sender', 'recepient', 'read', and 'deleted'
        :param username: str
        :param slug: str or int
        :return: dict
        """

        if slug:
            response = requests.get(url=self.message_endpoint + str(slug), headers=self.logins[username])
            # tested with the message id, as well as the keywords
            # 'all', 'sender', 'recepient', 'read', and 'deleted'

            return response.json()
        else:
            response = requests.get(url=self.message_endpoint, headers=self.logins[username])
            return response.json()

    def loop_read(self, slug: Union[int, str]) -> None:
        """
        Loop through all of this TestAgent's logins and print the mailbox represented by the slug
        :param slug: str, int, or None
        :return: None
        """

        print('reading')
        for username in self.usernames:
            print(f"checking {username}'s mailbox")
            self.get(username, slug)

    def post(self, sender: str, recepient: str, title: str, body: str) -> int:
        """
        Send a message from the sender to the recepient account.
        It returns a the message's id, which can be used as a slug
        :param sender: str
        :param recepient: str
        :param title: str
        :param body: str
        :return: int
        """

        print('sending messages')
        response = requests.post(url=self.message_endpoint,
                                 data=json.dumps({'recepient': recepient,
                                                  'title': title,
                                                  'body': body}),
                                 headers=self.logins[sender])
        print(response.json())
        return int(response.json()['id'])

    def delete(self, username: str, slug: int) -> None:
        """
        Delete a message from the perspective of anyone who can see it.
        :param username: str
        :param slug: int
        :return: None
        """

        print('deleting')
        deleted = requests.delete(url=self.message_endpoint + str(slug), headers=self.logins[username])

        print(deleted.content)
