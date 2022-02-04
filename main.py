from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp

Builder.load_file("./main.kv")


class Manager(ScreenManager):
    pass


class Genius(MDApp):
    def build(self):
        manager = Manager()
        Window.size = (350, 600)
        return manager


if __name__ == "__main__":
    Genius().run()
