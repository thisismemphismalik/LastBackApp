from kivy.lang import Builder
from kivymd.uix.screen import MDScreen

Builder.load_file("./connection/connection.kv")


class Connection(MDScreen):

    def on_kv_post(self, base_widget):
        self.ids["email"].focused = True

    def send(self, email, password):
        # TODO: set connection behavior
        print(email, password)
        self.manager.current = "App"
