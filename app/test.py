from kivy.lang import Builder
from kivy.properties import StringProperty

from kivymd.app import MDApp
from kivymd.uix.gridlayout import MDGridLayout

KV = '''
<GG>:
    cols: 2

    MDLabel:
        text: 'Тип услуг:'
        theme_text_color: "Custom"

    MDIconButton:
        icon: "plus-circle"
        user_font_size: "30sp"
'''


class GG(MDGridLayout):
    pass


class Test(MDApp):
    def build(self):
        return Builder.load_string(KV)


Test().run()