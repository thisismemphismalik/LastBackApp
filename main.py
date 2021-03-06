from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp

Builder.load_file("./main.kv")


class Manager(ScreenManager):
    pass


class BackApp(MDApp):
    def build(self):
        Window.size = (350, 600)
        manager = Manager()
        return manager


if __name__ == "__main__":
    BackApp().run()
