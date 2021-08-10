import builtins
from kivy.uix.scrollview import ScrollView

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import DictProperty, StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFloatingActionButton, MDFlatButton
from kivymd.uix.card import MDCard, MDSeparator
from kivymd.uix.dialog import MDDialog
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelThreeLine
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.textfield import MDTextField

from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget, MDList 


class OrderLIstItem(OneLineIconListItem):
    """Дополнительно содержит в себе icon и принимает аргументы order_id и
    icon - название/путь к файлу иконки."""
    def __init__(self, order_id, icon, **kwargs) -> None:
        super(OrderLIstItem, self).__init__(**kwargs)
        self.order_id = order_id
        self.icon = icon

        icon = IconLeftWidget(icon=self.icon)
        self.add_widget(icon)


class OrderContent(MDBoxLayout):
    """Создает выпадающую вкладку для экземпляра списка заказов.
    Аргументом принимает поле 'description' из запроса."""
    def __init__(self, data,  **kwargs) -> None:
        super(OrderContent, self).__init__(**kwargs)

        self.orientation='vertical'
        self.adaptive_height = False
        self.size_hint_y = None
        self.height = '400dp'

        label = MDLabel(text=data, adaptive_height=True)
        button = MDFloatingActionButton(icon='language-python')

        self.add_widget(label)
        self.add_widget(button)


class ProfileCard(MDCard):
    """Создает карту профиля пользователя.
    Аргументоп ринимает данные о пользователе из запроса."""
    dialog = None

    def __init__(self, data, **kwargs) -> None:
        super(ProfileCard, self).__init__(**kwargs)

        self.ids.first_name.text = data['first_name'] 
        self.ids.last_name.text = data['last_name'] 
        self.ids.email.text = data['email']

        self.ids.phone_number.text = data['profile']['phone_number']
        self.ids.description.text = data['profile']['description']
        self.ids.work_experience.text = data['profile']['work_experience']
        self.ids.is_juridical.text = str(data['profile']['is_juridical'])


        self.ids.region.text = data['profile']['region']
        self.ids.city.text = data['profile']['city']

        if data['profile']['category']:     
            self.ids.category.text = str(data['profile']['category'])
        
    def show_dialog(self, instance, field_name):
        """Открывает диалоговое окно для смены данных профиля.
         В качестве аргументов передает значение изменяемого поля и его название."""   
        if not self.dialog:
            content = Content(instance.text, field_name)
            self.dialog = MDDialog(
                title = 'Изменение данных:',
                type = 'custom',
                content_cls = content,
                buttons = [
                    MDFlatButton(
                        text="ОТМЕНА",
                        theme_text_color="Custom",
                        text_color=(0, 0, 0, 1),
                        on_release = self.close_dialog
                    ),
                    MDFlatButton(
                        text="ОБНОВИТЬ",
                        theme_text_color="Custom",
                        text_color=(0, 0, 0, 1),
                        on_release = content.update_data
                    ),
                ]
            ) 
        self.dialog.open()

    def close_dialog(self, *args):

        if self.dialog:
            self.dialog = None

  
class Content(BoxLayout):
    old_data = StringProperty()
    new_data = DictProperty()
    field_name = StringProperty()

    def __init__(self, data, field_name, **kwargs) -> None:
        super().__init__(**kwargs)

        self.old_data = data
        self.field_name = field_name

    def update_data(self, *args):
        print(self.new_data)