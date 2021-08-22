from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.expansionpanel import MDExpansionPanelThreeLine, MDExpansionPanel
from kivy.metrics import dp

KV = '''

<Content>:
    cols: 1
    adaptive_height: True

    OneLineAvatarIconListItem:
        text: '1111'

    OneLineAvatarIconListItem:
        text: '2222'


<ItemConfirm>:
    cols: 1
    size_hint_y: None
    height: '300dp'

    ScrollView:
        MDBoxLayout:
            size_hint_y: None
            adaptive_height: True
            orientation: 'vertical'

            id: box


MDFloatLayout:

    MDFlatButton:
        text: "ALERT DIALOG"
        pos_hint: {'center_x': .5, 'center_y': .5}
        on_release: app.show_confirmation_dialog()
'''


class ItemConfirm(MDGridLayout):
    

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        for i in range(10):
            item =  MDExpansionPanel(
                content=Content(),
                panel_cls=MDExpansionPanelThreeLine(
                    text="Text",
                    secondary_text="Secondary text",
                    tertiary_text="Tertiary text",
                )
            )
            self.ids.box.add_widget(item)


class Content(MDGridLayout):
    pass


class Example(MDApp):
    dialog = None

    def build(self):
        return Builder.load_string(KV)

    def show_confirmation_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Phone ringtone",
                type="custom",
                content_cls = ItemConfirm(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL", text_color=self.theme_cls.primary_color
                    ),
                    MDFlatButton(
                        text="OK", text_color=self.theme_cls.primary_color
                    ),
                ],
            )
        self.dialog.open()


Example().run()