from kivy.lang import Builder
from kivymd.uix.screen import MDScreen

from fire import Fire, Database
from lab import create_event

Builder.load_file("./login_screen/login_screen.kv")

ak = "AIzaSyAvOrMZxvQyHAtn70prSGJbIcyRUTgBgy8"
idd = "treize-13"


class LoginScreen(MDScreen):
    def on_kv_post(self, base_widget):
        self.ids["email"].focused = True

    def send(self, email, password):
        print(email, password)
        self.manager.current = "AppScreen"
