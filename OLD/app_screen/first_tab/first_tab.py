from kivy.lang import Builder
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.tab import MDTabsBase

Builder.load_file("./app_screen/first_tab/first_tab.kv")


class FirstTab(MDFloatLayout, MDTabsBase):
    pass
