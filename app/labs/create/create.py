from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.picker import MDDatePicker, MDTimePicker
from kivymd.uix.screen import MDScreen
from lollypop.menu_header import MenuHeader

from static import COLOR

Builder.load_file("app/labs/create/create.kv")


class Create(MDScreen):

    def next(self):
        one = self.ids.one
        two = self.ids.two

        one.remove_widget(two)

    def on_kv_post(self, base_widget):

        self.menu_items = [
            {
                "text": i.capitalize(),
                "viewclass": "OneLineListItem",
                "height": 55,
                "on_release": lambda x=f"Item {i}": self.menu_callback(x),
            } for i in COLOR
        ]

        self.menu = MDDropdownMenu(
            caller=self.ids.caller,
            items=self.menu_items,
            width_mult=4,
        )

    def menu_callback(self, actual):
        print(actual)
        self.ids.caller.text = actual
        self.menu.dismiss()

    def on_save(self, instance, value, date_range):
        print(instance.year, value, date_range)
        self.ids["date_value"].text = str(value)

    def date(self):
        date_picker = MDDatePicker(year=2022, month=2, day=25)
        date_picker.bind(on_save=self.on_save)
        date_picker.open()

    def time(self):
        time_picker = MDTimePicker(hour="8", minute="31")
        time_picker.open()


class One(MDBoxLayout):
    pass
