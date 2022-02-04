import json

import certifi
import requests
from kivy import Logger
from kivymd.toast import toast

from lab import create_event

ak = "AIzaSyAvOrMZxvQyHAtn70prSGJbIcyRUTgBgy8"
id = "treize-13"


class Fire:
    def __init__(self, api_key, id):
        self.api_key = api_key
        self.id = id

        self.requester = requests.session()
        self.requester.verify = certifi.where()


class Auth:
    def __init__(self, FireClass):
        self.api_key = FireClass.api_key
        self.requester = FireClass.requester

        self.url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.api_key}"
        self.arl = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.api_key}"

    def sign_up(self, phone):
        data = json.dumps({"email": phone + "@treize.ml", "password": phone, "returnSecureToken": True})
        headers = {"Content-Type": "application/json"}

        response = self.requester.post(url=self.url, data=data, headers=headers)

        print(response.text)
        return response.text

    def sign_in(self, phone):
        data = json.dumps({"email": phone + "@treize.ml", "password": phone, "returnSecureToken": True})
        headers = {"content-type": "application/json"}

        response = self.requester.post(url=self.arl, data=data, headers=headers)

        print(response.text)
        return response.text


class Storage:
    def __init__(self):
        self.seperator = "%2F"
        self.id = "treize-13"
        self.url = f"https://firebasestorage.googleapis.com/v0/b/{self.id}.appspot.com/o/"

    def upload(self, local_path, cloud_path, content_type):
        local_file = open(local_path, "rb").read()
        cloud_file = cloud_path.replace("/", self.seperator)

        headers = {"Content-Type": content_type}

        r = requests.post(url=self.url+cloud_file, data=local_file, headers=headers, verify=certifi.where())

        print(self.url+cloud_file+"?alt=media")


class Database:
    def __init__(self, FireClass):
        self.id = FireClass.id
        self.url = f"https://{self.id}-default-rtdb.firebaseio.com/"

    def add_event(self, event_id, event):
        url = self.url + "events/" + event_id + ".json"
        data = json.dumps(event)

        try:
            requests.patch(url=url, data=data)

        except requests.exceptions.ConnectionError:
            toast("No connection to the database")
            Logger.warning(f"No connection to the database")
