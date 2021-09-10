from kivy.lang import Builder
from kivy.properties import StringProperty

from kivymd.app import MDApp
from kivymd.uix.gridlayout import MDGridLayout

KV = '''
MDScreen:
    MDBoxLayout:
        orientation: 'vertical'
        size_hint: None, None
        height: '100dp'
        width: '120dp'
        spacing: '10dp'
        pos_hint: {'center_x': .5, 'center_y': .5}

        FitImage:
            source: 'images/something.jpg'
            size_hint: None, None
            height: '120dp'
            width: '120dp'
            size_hint_y: None
            pos_hint: {'top': 1}
            radius: 8, 8, 8, 8

        MDRoundFlatIconButton:
            icon: "exit-run"
            text: "выйти"
            pos_hint: {'center_x': .5, 'center_y': .5}
            theme_text_color: "Custom"
            text_color: 0, 0, 0, 1
            line_color: 0, 0, 0, 0.4
            icon_color: 0, 0, 0, 0.4
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