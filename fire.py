import json
import certifi
import requests

from kivy import Logger
from kivymd.toast import toast

from api_key import key, identifer

ak = key
id = identifer


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

    def upload_event_image(self, local_path, event_id):
        file_type = local_path.split(".")[~0]

        local_file = open(local_path, "rb").read()

        cloud_path = "events/" + event_id + "." + file_type
        cloud_file = cloud_path.replace("/", self.seperator)

        headers = {"Content-Type": f"image/{file_type}"}

        r = requests.post(url=self.url + cloud_file, data=local_file, headers=headers, verify=certifi.where())

        return self.url + cloud_file + "?alt=media"


class Database:
    def __init__(self, FireClass):
        self.id = FireClass.id
        self.url = f"https://{self.id}-default-rtdb.firebaseio.com/"

    def add_event(self, event_id, event):
        url = self.url + "events/" + event_id + ".json"
        data = json.dumps(event)

        try:
            requests.patch(url=url, data=data)

            # add to dates
            date_url = self.url + "dates/" + event["date"].replace("/", "-") + ".json"
            date_data = json.dumps({event_id: True})
            requests.patch(url=date_url, data=date_data)

            # add to sellers
            seller_url = self.url + "sellers/" + event["seller"] + ".json"
            seller_data = json.dumps({event_id: True})
            requests.patch(url=seller_url, data=seller_data)

            # add to categories
            category_url = self.url + "categories/" + event["category"] + ".json"
            category_data = json.dumps({event_id: True})
            requests.patch(url=category_url, data=category_data)

        except requests.exceptions.ConnectionError:
            toast("No connection to the database")
            Logger.warning(f"No connection to the database")

    def read_event(self, event_id):
        url = self.url + "events/" + event_id + ".json"

        try:
            data = requests.get(url=url)
            return data.json()

        except requests.exceptions.ConnectionError:
            toast("No connection to the database")
            Logger.warning(f"No connection to the database")

    def add_tags(self, event_id, tags):
        all_tags = list(tags)

        for i in all_tags:

            url = self.url + "tags/" + i + ".json"
            data = json.dumps({event_id: True})

            try:
                requests.patch(url=url, data=data)

            except requests.exceptions.ConnectionError:
                toast("No connection to the database")
                Logger.warning(f"No connection to the database")

    def get_by_date(self, date):
        url = self.url + "dates/" + date + ".json"

        try:
            data = requests.get(url=url)
            return data.json()

        except requests.exceptions.ConnectionError:
            toast("No connection to the database")
            Logger.warning(f"No connection to the database")

    def get_by_seller(self, seller):
        url = self.url + "sellers/" + seller + ".json"

        try:
            data = requests.get(url=url)
            return data.json()

        except requests.exceptions.ConnectionError:
            toast("No connection to the database")
            Logger.warning(f"No connection to the database")

    def get_by_category(self, category):
        url = self.url + "dates/" + category + ".json"

        try:
            data = requests.get(url=url)
            return data.json()

        except requests.exceptions.ConnectionError:
            toast("No connection to the database")
            Logger.warning(f"No connection to the database")

    def get_by_tags(self, tags):
        score = dict()

        for i in tags:
            url = self.url + "tags/" + i + ".json"

            try:
                data = requests.get(url=url)
                print(data)

                try:
                    values = data.json().keys()

                    for j in values:
                        if j in score.keys():
                            score[j] += 1
                        else:
                            score[j] = 1

                except AttributeError:
                    print("NOOOOOOOO")

            except requests.exceptions.ConnectionError:
                toast("No connection to the database")
                Logger.warning(f"No connection to the database")

        sorted_score = [el[0] for el in sorted(score.items(), key=lambda x: x[1], reverse=True)]

        print(sorted_score)
