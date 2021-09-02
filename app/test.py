from kivy.lang import Builder
from kivy.properties import StringProperty

from kivymd.app import MDApp
from kivymd.uix.gridlayout import MDGridLayout

KV = '''
MDScreen:

    MDGridLayout:
        cols: 1

        MDBoxLayout:
            orientation: 'horizontal'

            MDLabel:
                text: 'Work type:'
                size_hint: None, 1
                width: self.text.size

            MDIconButton:
                icon: 'fountain-pen'
                size_hint_x: None
                width: '40dp'
                user_font_size: '15dp'
                pos_hint: {'center_x': .5, 'center_y': .52}
                theme_text_color: "Custom"
                text_color: 1, 0, 1, 1

        MDBoxLayout:
            orientation: 'vertical'

            MDLabel:
                text: app.text
'''

TEXT = 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry"s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.'


class GG(MDGridLayout):
    pass

class Test(MDApp):
    text = TEXT

    def build(self):
        return Builder.load_string(KV)

    def press(self, label):
        print(label.text)


Test().run()