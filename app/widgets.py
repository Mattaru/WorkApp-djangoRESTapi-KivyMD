import builtins
from kivy.uix.scrollview import ScrollView

from kivy.properties import DictProperty, StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.card import MDCard, MDSeparator
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelThreeLine
from kivymd.uix.tab import MDTabsBase

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


class OrdersContent(MDBoxLayout):
    """Создает выпадающую вкладку для экземпляра списка заказов.
    Аргументом принимает поле 'description' из запроса."""
    def __init__(self, data,  **kwargs) -> None:
        super(OrdersContent, self).__init__(**kwargs)

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
    def __init__(self, data, **kwargs) -> None:
        super(ProfileCard, self).__init__(**kwargs)

        self.ids.username.text = data['username']
        self.ids.first_name.text = data['first_name']
        self.ids.last_name.text = data['last_name']
        self.ids.email.text = data['email']
        self.ids.region.text = data['profile']['region']
        self.ids.city.text = data['profile']['city']
        if data['profile']['category']:     
            self.ids.category.text = str(data['profile']['category'])
            