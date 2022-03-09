from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.card import MDCard

Builder.load_file("components/ticket_banner/ticket_banner.kv")


class TicketBanner(MDCard, ButtonBehavior):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
