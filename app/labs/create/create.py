import os.path

import kivymd
from kivy.clock import Clock
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDSeparator
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.picker import MDDatePicker, MDTimePicker
from kivymd.uix.screen import MDScreen
from plyer import filechooser

from components.ticket_banner.ticket_banner import TicketBanner
from lab import create_event
from static import COLOR, correct_date, CATEGORY, convert, hasher, make_event

Builder.load_file("app/labs/create/create.kv")


class Create(MDScreen):
    def on_kv_post(self, base_widget):
        self.one = One()
        self.two = None
        self.ids.base.add_widget(self.one)


class One(MDBoxLayout):
    def __init__(self, **kwargs):
        self.color_menu = None
        self.category_menu = None
        self.data = None
        super().__init__(**kwargs)

    def choose(self):

        file = filechooser.open_file()

        try:
            path = file[0]

            if not os.path.getsize(path) <= 50000:

                try:
                    convert(path, "./temp/event.jpeg")
                    self.ids.image.source = "./temp/event.jpeg"

                except OSError:
                    toast("invalid image file")

            else:
                self.ids.image.source = path

        except TypeError:
            pass

    def on_save_date(self, instance, value, date_range):
        self.ids["date"].text = correct_date(value)

    def on_save_time(self, instance, value):
        self.ids["time"].text = str(value)[:~2]

    def date(self):
        date_picker = MDDatePicker()
        date_picker.bind(on_save=self.on_save_date)
        date_picker.open()

    def time(self):
        time_picker = MDTimePicker(hour="8", minute="31")
        time_picker.bind(on_save=self.on_save_time)
        time_picker.open()

    def menu_callback(self, actual, name):
        if name == "color":
            self.ids.color.text = actual
            self.color_menu.dismiss()
        else:
            self.ids.category.text = actual
            self.category_menu.dismiss()

    def color(self):

        color_items = [
            {
                "text": i.capitalize(),
                "viewclass": "OneLineListItem",
                "height": 35,
                "on_release": lambda x=f"{i} >".capitalize(): self.menu_callback(x, "color"),
            } for i in COLOR
        ]

        self.color_menu = MDDropdownMenu(
            caller=self.ids.color,
            items=color_items,
            width_mult=2,
        )

        self.color_menu.open()

    def category(self):

        category_items = [
            {
                "text": i.capitalize(),
                "viewclass": "OneLineListItem",
                "height": 35,
                "on_release": lambda x=f"{i} >".capitalize(): self.menu_callback(x, "category"),
            } for i in CATEGORY
        ]

        self.category_menu = MDDropdownMenu(
            caller=self.ids.category,
            items=category_items,
            width_mult=2,
        )

        self.category_menu.open()

    def validate(self, name, image, color, category, about, location, date, time):
        infos = [name, image, color, category, about, location, date, time]
        data = create_event([i.text for i in infos])

        # correct color and category values

        data["color"] = data["color"][:~1].lower()
        data["category"] = data["category"][:~1].lower()

        self.data = data

        one = self.parent.parent.parent.one
        two = Two(self.data)
        # two.data = self.data

        frame = one.parent
        frame.remove_widget(one)

        make_event(data)

        with open("temp/count.txt", "w+") as file:
            file.write("0")

        frame.add_widget(two)
        frame.children[1].icon = "backburger"


class Two(MDBoxLayout):
    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.dialog = MDDialog(
            title="Add a ticket",
            type="custom",
            content_cls=Content()
        )
        self.data = data
        self.ticket_id = hasher(self.data)[~12:].upper()
        print(self.ticket_id, self.data)

        self.ids.ticket_id.text = self.ticket_id

        self.ids.table.add_widget(MDSeparator())
        self.ids.table.add_widget(TicketBanner("Qty", "Name", "Price", "blank"))
        # self.ids.table.add_widget(MDSeparator())

    def open(self):

        with open("temp/count.txt", "r+") as file:
            file.seek(0)
            a = file.readlines()
            a = int(a[0])

            if a < 5:
                self.dialog.open()

            else:
                toast("No more than 5 tickets per event")

    def validate(self):
        print(self.ids.table.children)


class Content(MDBoxLayout):
    @staticmethod
    def magnify(field, text):
        if field.text == text and field.focused:
            field.text = ""

        elif field.text == "" and not field.focused:
            field.text = text

    def add_ticket(self, qty, name, price, advantage):
        print(qty, name, price, advantage)

        ticket = dict()

        ticket["quantity"] = int(qty)
        ticket["name"] = name
        ticket["price"] = price
        ticket["advantage"] = advantage

        print(ticket)

        app = MDApp.get_running_app()
        frame = app.root.ids.main.ids.second_manager.children[1].children[0].children[0].children[0].children[0].\
            children[0].children[0].children[0].children[0].children[0].children[2].children[0]

        frame.add_widget(TicketBanner(qty, name, price))

        with open("temp/count.txt", "r+") as file:
            file.seek(0)
            a = file.readlines()
            a = int(a[0])

        with open("temp/count.txt", "w+") as file:
            file.write(f"{a + 1}")

        self.parent.parent.parent.dismiss()
