from kivy.lang import Builder
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.tab import MDTabsBase, MDTabs

Builder.load_file("./app_screen/second_tab/second_tab.kv")


class SecondTab(MDFloatLayout, MDTabsBase):
    pass

