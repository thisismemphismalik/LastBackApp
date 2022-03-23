import os.path
from functools import partial

import kivymd
from kivy.clock import Clock

from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDSeparator
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.picker import MDDatePicker, MDTimePicker
from kivymd.uix.screen import MDScreen
from plyer import filechooser

from components.ticket_banner.ticket_banner import TicketBanner
from fire import Storage, Database, Fire
from lab import create_event
from static import COLOR, correct_date, CATEGORY, convert, hasher, make_event, read_event, add_event_key, add_tickets, make_tags

Builder.load_file("app/labs/create/create.kv")


class Create(MDScreen):
    def __init__(self, **kw):
        self.one = None
        self.two = None
        self.three = None
        super().__init__(**kw)

    def on_kv_post(self, base_widget):
        self.one = One()
        self.ids.base.add_widget(self.one)

    def go_back(self):
        if self.ids.back.icon == "close-circle-outline":
            self.manager.current = "Base"

        else:
            one = self.one
            two = self.two
            three = self.three

            if not three:
                # switch
                self.ids.base.remove_widget(two)
                self.ids.base.add_widget(one)

                self.ids.back.icon = "close-circle-outline"
                self.two = None

            else:
                # switch
                self.ids.base.remove_widget(three)
                self.ids.base.add_widget(two)
                self.three = None


class One(MDBoxLayout):
    def __init__(self, **kwargs):
        self.color_menu = None
        self.category_menu = None
        self.data = None

        self.spin = Spin()
        super().__init__(**kwargs)

    def spinner(self, to_do, dt):
        under = self.parent.parent.parent
        spin = self.spin

        if to_do.lower() == "start":
            # start the spinner
            under.add_widget(spin)

        else:
            under.remove_widget(spin)

    def choose(self, dt):

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

        Clock.schedule_once(partial(self.spinner, "stop"), 1)

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

    def validate(self, name, image, color, category, about, location, date, time, seller, dt):
        infos = [name, image, color, category, about, location, date, time, seller]
        data = create_event([i.text for i in infos])
        # correct color and category values

        data["color"] = data["color"][:~1].lower()
        data["category"] = data["category"][:~1].lower()

        # add data to event temp file
        make_event(data)

        # manage create screens
        base = self.parent.parent.parent
        one = self.parent.parent.parent.one
        two = Two()

        frame = one.parent
        frame.remove_widget(one)
        frame.add_widget(two)
        frame.children[1].icon = "backburger"

        base.two = two

        # reset ticket counter
        with open("temp/count.txt", "w+") as file:
            file.write("0")


class Two(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = MDDialog(
            title="Add a ticket",
            type="custom",
            content_cls=Content()
        )

        # hash data and add event key
        data = read_event()
        key = hasher(data)[~12:].upper()

        add_event_key(key)

        self.ids.ticket_id.text = key

        # add table head
        self.ids.table.add_widget(MDSeparator())
        self.ids.table.add_widget(TicketBanner("Qty", "Type", "Price", "blank"))

    def open(self):

        with open("temp/count.txt", "r+") as file:
            file.seek(0)
            a = file.readlines()
            a = int(a[0])

            if a < 5:
                self.dialog.open()

            else:
                toast("No more than 5 tickets per event")

    def validate(self, dt):
        children = [i for i in self.ids.table.children]

        # remove noise
        for i in children:
            if i.__class__ == kivymd.uix.card.MDSeparator:
                children.remove(i)

        if children[~0].quantity.lower() == "qty":
            children.pop(~0)

        # get tickets data
        tickets = []

        for i in children:
            a = dict()
            a["quantity"] = i.quantity
            a["type"] = i.type
            a["price"] = i.price
            a["advantage"] = i.advantage

            tickets.append(a)

        add_tickets(tickets)

        # switch to third part
        base = self.parent.parent.parent
        two = self.parent.parent.parent.two
        three = Three()

        frame = two.parent
        frame.remove_widget(two)
        frame.add_widget(three)

        base.three = three


class Three(MDBoxLayout):
    def __init__(self, **kwargs):
        self.data = read_event()
        self.id = [i for i in self.data.keys()][0]
        self.image = self.data[self.id]["image"]
        self.name = self.data[self.id]["name"]
        self.category = self.data[self.id]["category"]
        self.seller = self.data[self.id]["seller"]
        self.date = self.data[self.id]["date"]
        self.time = self.data[self.id]["time"]
        self.color = self.data[self.id]["color"]
        self.about = self.data[self.id]["about"]
        self.tickets = self.data[self.id]["tickets"]

        self.spin = Spin()
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        for i in self.tickets:
            self.ids.tickets.add_widget(TicketBanner(i["quantity"], i["type"], i["price"], "information-outline",
                                                     i["advantage"]))

    def spinner(self, to_do, dt):
        under = self.parent.parent.parent
        spin = self.spin

        if to_do.lower() == "start":
            # start the spinner
            under.add_widget(spin)

        else:
            under.remove_widget(spin)

    def validate(self, dt):
        event = read_event()
        ids = [i for i in event.keys()][0]

        uploader = Storage()
        url = uploader.upload_event_image(event[ids]["image"], ids)

        event[ids]["image"] = url

        make_event(event)

        # add event to database
        ak = "AIzaSyAvOrMZxvQyHAtn70prSGJbIcyRUTgBgy8"
        p_id = "treize-13"

        fire = Fire(ak, p_id)
        db = Database(fire)

        db.add_event(ids, event[ids])

        # launch the tags on firebase
        tags = make_tags()

        db.add_tags(ids, tags)

        # stop the spinner
        Clock.schedule_once(partial(self.spinner, "stop"), 1)
        Clock.schedule_once(self.switch, 2)

    def switch(self, dt):
        # go to one
        base = self.parent.parent.parent
        base.one = One()

        frame = self.parent
        frame.remove_widget(self)
        frame.add_widget(base.one)


class Spin(MDFloatLayout):

    def on_kv_post(self, base_widget):
        Clock.schedule_interval(self.animation, 1//5)

    def animation(self, dt):
        spin = self
        spin.xx, spin.yy = spin.xx + 5, spin.yy + 5


class Content(MDBoxLayout):

    def add_ticket(self, qty, type, price, advantage):
        q, t, p, a = str(qty.text), str(type.text), str(price.text), str(advantage.text),

        ticket = dict()

        ticket["quantity"] = int(q)
        ticket["type"] = t
        ticket["price"] = p
        ticket["advantage"] = a

        app = MDApp.get_running_app()
        frame = app.root.ids.main.ids.second_manager.children[1].children[0].children[0].children[0].children[0]. \
            children[0].children[0].children[0].children[0].children[0].children[2].children[0]

        frame.add_widget(TicketBanner(q, t, p, advantage=a))

        with open("temp/count.txt", "r+") as file:
            file.seek(0)
            a = file.readlines()
            a = int(a[0])

        with open("temp/count.txt", "w+") as file:
            file.write(f"{a + 1}")

        # clear fields
        qty.text = "Quantity"
        type.text = "Type"
        price.text = "Price"
        advantage.text = "Advantage"

        self.parent.parent.parent.dismiss()
