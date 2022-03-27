from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen

Builder.load_file("app/labs/update/update.kv")


class Update(MDScreen):
    def go_back(self):
        if self.ids.back.icon == "close-circle-outline":
            self.manager.current = "Base"

        # else:
        #     one = self.one
        #     two = self.two
        #     three = self.three
        #
        #     if not three:
        #         # switch
        #         self.ids.base.remove_widget(two)
        #         self.ids.base.add_widget(one)
        #
        #         self.ids.back.icon = "close-circle-outline"
        #         self.two = None
        #
        #     else:
        #         # switch
        #         self.ids.base.remove_widget(three)
        #         self.ids.base.add_widget(two)
        #         self.three = None


class Search(MDBoxLayout):
    # field for event research
    pass
