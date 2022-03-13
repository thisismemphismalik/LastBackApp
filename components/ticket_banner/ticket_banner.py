from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivymd.toast import toast
from kivymd.uix.card import MDCard

Builder.load_file("components/ticket_banner/ticket_banner.kv")


class TicketBanner(MDCard, ButtonBehavior):
    def __init__(self, quantity, type, price, icon=None, advantage=None, **kwargs):
        self.quantity = quantity
        self.type = type
        self.price = price
        self.icon = icon
        self.advantage = advantage

        if self.icon is None:
            self.icon = "close-circle-outline"

        super().__init__(**kwargs)

    def close(self):
        self.parent.remove_widget(self)

        with open("temp/count.txt", "r+") as file:
            file.seek(0)
            a = file.readlines()
            a = int(a[0])

        with open("temp/count.txt", "w+") as file:
            file.write(f"{a - 1}")

    def show(self):
        toast(self.advantage)
