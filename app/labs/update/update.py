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

        fire = Fire(key, identifer)
        db = Database(fire)

        # Search
        if len(field.text.split(":")) < 1:
            if method == "id":
                event = db.read_event(value)
                print(event)

            elif method == "date":
                events = db.get_by_date(value.replace("/", "-"))
                print(events)

            elif method == "seller":
                events = db.get_by_seller(value)
                print(events)

            elif method == "category":
                events = db.get_by_category(value)
                print(events)

        else:
            events = db.get_by_tags(field.text.split(" "))

            print(events)