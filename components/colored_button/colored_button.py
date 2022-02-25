from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.card import MDCard

Builder.load_file("components/colored_button/colored_button.kv")


class ColoredButton(MDCard, ButtonBehavior):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
