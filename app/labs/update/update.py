import requests
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen

from fire import Fire, Database
from api_key import key, identifer

Builder.load_file("app/labs/update/update.kv")


class Update(MDScreen):
    def go_back(self):
        if self.ids.back.icon == "close-circle-outline":
            self.manager.current = "Base"


class Search(MDBoxLayout):
    # field for event research
    def search(self, field):

        # get method and value
        method = field.text.split(":")[0].lower()
        value = field.text.split(":")[~0].upper()

        # Search
        if method == "id":

            fire = Fire(key, identifer)
            db = Database(fire)

            event = db.read_event(value)

            print(event)

        elif method == "seller":
            pass
