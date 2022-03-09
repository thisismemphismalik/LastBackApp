from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.card import MDCard

Builder.load_file("components/ticket_banner/ticket_banner.kv")


class TicketBanner(MDCard, ButtonBehavior):
    def __init__(self, quantity, name, price, icon=None, **kwargs):
        self.quantity = quantity
        self.name = name
        self.price = price
        self.icon = icon

        if self.icon is None:
            self.icon = "close-circle-outline"

        super().__init__(**kwargs)

