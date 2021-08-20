import builtins

from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import DictProperty, StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFloatingActionButton, MDFlatButton
from kivymd.uix.card import MDCard, MDSeparator
from kivymd.uix.dialog import MDDialog
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelThreeLine, MDExpansionPanelOneLine
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.snackbar import Snackbar

from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineAvatarIconListItem, OneLineIconListItem, OneLineListItem, IRightBodyTouch, IconLeftWidget, MDList 


class ChooseCategoryTitle(OneLineIconListItem):
    pass


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

# Wright mixin for the profile dialog content

# class ProfileDialogMixin:
#     pass


class ProfileDialogFieldContent(MDBoxLayout):
    """Отображает содержимое выбранного поля в диалоговом окне."""
    old_data = StringProperty()
    new_data = DictProperty()
    field_name = StringProperty()

    def __init__(self, data, field_name, **kwargs) -> None:
        super().__init__(**kwargs)

        self.old_data = data
        self.field_name = field_name

    def is_profile_field(self):
        """Проверяет поле 'field_name', если оно относится к профилю пользователя,
         то возвращает True иначе False."""
        result = self.field_name.split('.')

        if len(result) == 2:
            return True
        
        return False

    def reset_data(self):
        """Обнуляет все данные класса."""
        self.old_data = ''
        self.new_data = {}
        self.field_name = ''


class ProfileDialogTextContent(MDBoxLayout):
    """Отображает содержимое выбранного поля в диалоговом окне."""
    old_data = StringProperty()
    new_data = DictProperty()
    field_name = StringProperty()

    def __init__(self, data, field_name, **kwargs) -> None:
        super().__init__(**kwargs)

        self.old_data = data
        self.field_name = field_name

    def is_profile_field(self):
        """Проверяет поле 'field_name', если оно относится к профилю пользователя,
         то возвращает True иначе False."""
        result = self.field_name.split('.')

        if len(result) == 2:
            return True
        
        return False

    def reset_data(self):
        """Обнуляет все данные класса."""
        self.old_data = ''
        self.new_data = {}
        self.field_name = ''
