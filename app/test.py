from kivy.lang import Builder
from kivy.properties import StringProperty

from kivymd.app import MDApp
from kivymd.uix.gridlayout import MDGridLayout

KV = '''
MDScreen:

    MDBoxLayout:
        orientation: 'vertical'

        MDToolbar:
            title: 'Вход:'
            left_action_items: [['arrow-left']]
            elevation: 8
            specific_text_color: 1, 1, 1, 1

        MDGridLayout:
            cols: 1
            size_hint: 1, 1
            padding: '20dp', '20dp', '20dp', '20dp'

            MDTextField:
                hint_text: 'логин'
                helper_text: 'введите имя пользователя'
                helper_text_mode: 'on_focus'
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                required: True
                icon_right: 'lead-pencil'
                icon_right_color: app.theme_cls.primary_color
'''

class GG(MDGridLayout):
    pass

class Test(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def press(self, label):
        print(label.text)


Test().run()