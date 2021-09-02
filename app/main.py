import datetime
import requests

from kivy.properties import DictProperty, StringProperty, ListProperty
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.core.text import LabelBase
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelThreeLine, MDExpansionPanelOneLine
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineListItem, MDList, OneLineIconListItem
from kivymd.uix.screen import Screen
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.toolbar import MDBottomAppBar, MDToolbar

from settings import Settings
from widgets import OrderContent, ProfileDialogFieldContent, ProfileDialogTextContent, ChooseCategoryTitle, CategoryListItem


from kivy.core.window import Window
Window.size = (310, 600)


settings = Settings('http://127.0.0.1:8000/')


class ChooseRole(Screen):

    def write_button_text(self, instance):
        """Записывает выбранную роль в настройки приложения."""
        settings.registration_role = instance.text.lower()

    def go_to_login(self):
        """Перенаправляет на страницу логина."""
        self.manager.current = 'login'
        self.manager.transition.direction = 'left'


class LogIn(Screen):
    form_data = DictProperty({})

    def validate_data(self):
        self.manager.current = 'main_page'
        self.manager.transition.direction = 'left'
    #     """Отправляет запрос с данными на логин в базу и либо дает разрешение на вход в приложение,
    #      либо оповещает об ошибке."""
    #     r, err = settings.get_jwt_token(self.form_data)
    #
    #     if err:
    #         self.message = 'Не верный логин или пароль.'
    #         login_title.color = (1, 0, 0, 1)
    #
    #     if r.status_code == 200:
    #         self.manager.current = 'main_page'
    #         self.manager.transition.direction = 'left'
    
    def go_back(self):
        """Перенаправляет на страницу выбора роли."""
        self.manager.current = 'choose_role'
        self.manager.transition.direction = 'right'


class Registration(Screen):
    background_color = [255, 255, 255, 0.6]
    form_data = DictProperty()
    category_list = []
    categories_data = None
    dialog = None
    dialog_content = None 

    def on_pre_enter(self):
        """Если не выбрана роль 'заказчик', то, перед переходом на экран регистрации, 
        добавляет блок с функционалом для выбора вида работ."""
        settings.categories_list = []
        self.ids.categories_box.clear_widgets()
        self.ids.categories.clear_widgets()

        if settings.registration_role != 'заказчик': 
            self.ids.categories_box.add_widget(self.ids.cat_field)
            self.ids.categories_box.add_widget(self.ids.cat_add_btn)

            r = requests.get(settings.HOST_URL + 'categories-list/')

            if not r.status_code == 200:
                self.show_err_snackbar('Сервер не доступен.')
            else:
                self.categories_data = r.json()

    def on_enter(self):
        pass

    def validate_data(self):
        """Формирует и проверяет данные для регистрации.
        Если данные валидны, то отправляет запрос на регистрацию,
        в случае успеха - перенаправляет на главную страницу приложения."""
        self.make_data_for_send()

        if not self.check_form_data():
            return False

        if not self.check_password():
            return False

        if not self.check_category():
            return False

        settings.make_login_data(
            self.form_data['username'],
            self.form_data['password']
        )
        r = self.send_registration_request()

        if not r.status_code == 201:
            self.show_err_snackbar('Сервер не доступен.')
        else:
            response, err = settings.get_jwt_token(settings.login_data)

            if not response.status_code == 200:
                self.show_err_snackbar('Сервер не доступен.')
            else:
                self.manager.current = 'main_page'
                self.manager.transition.direction = 'left'
                self.reset_data()

    def get_category_data(self, instance, role_label):
        """"Получить данные формы по категории с привязанных кнопок.
         В случае активной фазы кнопки - сменить ее цвет."""
        if instance.active:
            self.category_list.append(role_label.text.lower())
        else:
            self.category_list.remove(role_label.text.lower())

    def make_data_for_send(self):
        """Добавляет данные о категориях и роли в общай словарь с информацией для отправки на сервер."""
        self.form_data['profile'] = {
                'role': [settings.registration_role],
                'categories': [],
                'subcategories': []
            }

        if settings.categories_list:
            for cat in settings.categories_list:
                if len(cat) != 2:
                    category = {'name': cat[0]}
                else:
                    category = {'name': cat[0]}
                    subcategory = {'name': cat[1]}
                    self.form_data['profile']['subcategories'].append(subcategory)
                
                if not category in self.form_data['profile']['categories']:
                    self.form_data['profile']['categories'].append(category)

    def check_form_data(self):
        """Проверяет наличие всей нужной информации для регистрации.
         Если введена не вся информация, то выводится сообщение об ошибке."""
        if not ('username' in self.form_data.keys()):
            self.show_err_snackbar('Введите логин.')
            return False
        elif not ('first_name' in self.form_data.keys()):
            self.show_err_snackbar('Введите имя.')
            return False
        elif not ('last_name' in self.form_data.keys()):
            self.show_err_snackbar('Введите фамилию.')
            return False
        elif not ('password' in self.form_data.keys()):
            self.show_err_snackbar('Введите пароль.')
            return False
        elif not ('re_password' in self.form_data.keys()):
            self.show_err_snackbar('Введите пароль повторно.')
            return False
        elif not ('email' in self.form_data.keys()):
            self.show_err_snackbar('Введите почтовый адрес.')
            return False
        elif not ('profile' in self.form_data.keys()):
            self.show_err_snackbar('Выберите вид работ.')
            return False

        return True

    def check_password(self):
        """Проверяет совпадают ли введенные пароли, а так же длинну пароля,
         если нет то выводит сообщение об ошибке."""
        if self.form_data['password'] != self.form_data['re_password']:
            self.show_err_snackbar('Введенные пароли не совпадают.')
            return False
        elif len(self.form_data['password']) < 8:
            self.show_err_snackbar('Пароль меньше 8 символов.')
            return False

        return True

    def check_category(self):
        """Проверяет выбрын ли тип предоставляемых услуг,
         если при входе выбрана роль не заказчика."""
        if settings.registration_role != 'заказчик':
            if not self.form_data['profile']['categories']:
                self.show_err_snackbar('Тип услуг не выбран.')
                return False
        
        return True

    def send_registration_request(self):
        """Отправить запрос к базе данных с информацией для регистрации пользователя.
         Если статус ответа не 200, то обрабатывает ошибки и выводит сообщения о них."""
        r = requests.post(settings.HOST_URL + 'auth/users/', json=self.form_data)
        email = ('email' in r.json().keys())

        if email:
            email_incorrect = r.json()['email'][0] == settings.error_messages['email_incorrect']
            email_repeat = r.json()['email'][0] == settings.error_messages['email_repeat']
            if email and email_incorrect:
                self.show_err_snackbar('Не корректно введена почта.')
            elif email and email_repeat:
                self.show_err_snackbar('Почта уже используется.')

        username = ('username' in r.json().keys())

        if username:
            username_already_used = r.json()['username'][0] == settings.error_messages['username_already_used']
            username_incorrect = r.json()['username'][0] == settings.error_messages['username_incorrect']
            if username and username_already_used:
                self.show_err_snackbar('Имя пользователя занято.')
            elif username and username_incorrect:
                self.show_err_snackbar('Не допустимые символы в имени.')

        return r

    def reset_data(self):
        """Обновить все данные класса."""
        self.form_data = {}
        self.category_list = []

    def go_back(self):
        """Перенаправляет на страницу выбора роли."""
        self.manager.current = 'choose_role'
        self.manager.transition.direction = 'right'

    def close_dialog(self, *args):
        """Закрывает диалоговое окно и сбрасывает значение self.dialog на None."""
        if self.dialog:
            self.dialog.dismiss(force=True)
            self.dialog = None
            self.dialog_content = None

    def show_dialog(self):
        """Открывает диалоговое окно с данными о категориях и подкатегориях."""
        if not self.dialog:   
            self.dialog = MDDialog(
                size_hint = [0.9, None],
                title='Виды работ:',
                type = 'custom',
                content_cls = CategoriesDialogContent(self.categories_data),
                buttons = [
                    MDFlatButton(
                        text="ОТМЕНА",
                        theme_text_color="Custom",
                        text_color=(0, 0, 0, 1),
                        on_release = self.close_dialog
                    ),
                    MDFlatButton(
                        text="ВЫБРАТЬ",
                        theme_text_color="Custom",
                        text_color=(0, 0, 0, 1),
                        on_release = self.select_categories
                    ),
                ]
            ) 
            self.dialog.open()

    def select_categories(self, *args):
        """Добавляет список выбранных категорий и подкатегорий на экран регистранции."""
        self.ids.categories.clear_widgets()

        if settings.categories_list:
            for category in settings.categories_list:
                cat = category[0]
                if len(category) == 2:
                    subcat = category[1]
                else:
                    subcat = ''
                item = CategoryListItem(
                    text='[size=14][b]' + cat.capitalize() + '[/b][/size]',
                    secondary_text='[size=12][b]' + subcat.lower() + '[/b][/size]'
                )
                self.ids.categories.add_widget(item)

        self.close_dialog()

    def show_err_snackbar(self, message):
        """Открывает всплывающее окно с сообщением об ошибке."""
        snack = Snackbar(
            text=message,
            snackbar_x="10dp",
            snackbar_y="10dp",
        )
        snack.size_hint_x = (
            Window.width - (snack.snackbar_x * 2)
        ) / Window.width
        snack.open()


class CategoriesDialogContent(MDGridLayout):
    """Наполняет диалоговое окно саиском категорий и для каждой категории выпадающим списком подкатегорий."""
    def __init__(self, categories, **kwargs) -> None:
        super().__init__(**kwargs)
        for cat in categories:
            item =  MDExpansionPanel(
                content=CategoriesDialogExpansionContent(cat),
                panel_cls=MDExpansionPanelOneLine(
                    text='[size=14][b]' + cat['name'].upper() + '[/b][/size]'
                )
            )
            self.ids.categories_box.add_widget(item)

            
class CategoriesDialogExpansionContent(MDGridLayout):
    """Наполняет MDExpansionPanel списком подкатегорий с checkbox."""
    def __init__(self, category, **kwargs) -> None:
        super().__init__(**kwargs)
        if 'subcategories' in category.keys() and category['subcategories']:
            for subcat in category['subcategories']:
                item = ChooseCategoriesContent(text='[size=12]' + subcat['name'] + '[/size]', category=category['name'])
                cat = (category['name'], subcat['name'])

                if cat in settings.categories_list:
                    item.ids.check.active = True

                self.add_widget(item)
        else:
            i = ChooseCategoriesContent(text='[size=14]' + category['name'] + '[/size]')
            cat= (category['name'],)

            if cat in settings.categories_list:
                i.ids.check.active = True

            self.add_widget(i)


class ChooseCategoriesContent(OneLineIconListItem):
    """Содержимое диалогового окна с названием категории и checkbox."""

    def __init__(self, category=None, **kwargs) -> None:
        super().__init__(**kwargs)

        self.category = category

    def active_switch(self, instance):
        """Переключает значение checkbox."""
        if instance.active:
            instance.active = False
        else:
            instance.active = True

    def get_cat_data(self, instance, check):
        """Формирует кортеж с данными о категории и подкатегории, если она есть.
        Проверяет состояние активности у checkbox и добавляет либо удаляет сформированный кортеж в список категорий."""
        if self.category:
            category = (f'{self.category}', self.get_cat_name(instance.text)) 
        else:
            category = (f'{self.get_cat_name(instance.text)}',)
                
        if check.active:
            settings.categories_list.append(category)
        else:
            index = settings.categories_list.index(category)
            settings.categories_list.pop(index)

        print(f'categories: {settings.categories_list}')

    def get_cat_name(self, text):
        """Обрабатывает текстовое поля виджета и возвращает название категории или подкатегории."""
        name = text.split('[')[1].split(']')[1]

        return name


class MainPage(Screen):

    def on_enter(self):
        data = {
            'username': 'testing4',
            'password': 'personaldata',
        }
        settings.get_jwt_token(data)
        headers = {'Authorization': f'Bearer {settings.access_token}'}
        r = requests.get(settings.HOST_URL, headers=headers)

        if r.status_code == 200:
            self.get_orders_tab_content(r.json()['Order'])
            self.get_profile_tab_content(r.json()['User'][0])
            
    def get_orders_tab_content(self, orders):
        """Заполняет OrdersTab списком заказов с данными из запроса.
        Аргументом принимает данные из запроса о заказах."""
        scroll = ScrollView()     
        grid = MDGridLayout(cols=1, adaptive_height=True, padding=['10dp', '0dp', '10dp', '0dp'])

        if orders:
            for order in orders:
                row = MDExpansionPanel(
                    icon="information-variant",
                    content=OrderContent(data=order['description']) ,
                    panel_cls=MDExpansionPanelThreeLine(
                        text=order['title'],
                        secondary_text=order['category'][0],
                        tertiary_text=order['order_date'],
                    )
                )
                grid.add_widget(row)

        scroll.add_widget(grid)
        self.ids.orders.add_widget(scroll)
    
    def get_profile_tab_content(self, user):
        """Заполняет ProfileTab данными о залогиненом пользователе.
         Аргументом принимает данные из о пользователе из запроса."""
        scroll = ScrollView()
        grid = MDGridLayout(cols=1, adaptive_height=True)

        if user:
            card = ProfileCard(data=user)
            grid.add_widget(card)
            
        scroll.add_widget(grid)
        self.ids.profile.add_widget(scroll)


class OrdersTab(MDFloatLayout, MDTabsBase):
    pass


class ProfileTab(MDFloatLayout, MDTabsBase):
    pass


class ProfileCard(MDCard):
    """Создает карту профиля пользователя.
    Аргументоп ринимает данные о пользователе из запроса."""
    dialog = None
    dialog_content = None
    instance = None

    def __init__(self, data, **kwargs) -> None:
        super(ProfileCard, self).__init__(**kwargs)

        self.ids.first_name.text = data['first_name'] 
        self.ids.last_name.text = data['last_name'] 
        self.ids.email.text = data['email']

        if data['profile']['phone_number']:
            self.ids.phone_number.text = data['profile']['phone_number']
        else:
            self.ids.phone_number.text = 'не указан'

        if data['profile']['description']:
            self.ids.description.text = data['profile']['description']
        else:
            self.ids.description.text = 'пусто'

        if data['profile']['work_experience']:
            self.ids.work_experience.text = data['profile']['work_experience']
        else:
            self.ids.work_experience.text = 'нк указан'

        self.ids.is_juridical.active = data['profile']['is_juridical']

        if data['profile']['region']:
            self.ids.region.text = data['profile']['region']
        else:
            self.ids.region.text = 'не указан'

        if data['profile']['city']:
            self.ids.city.text = data['profile']['city']
        else:
            self.ids.city.text = 'не указан'

        if data['profile']['categories']:     
            self.ids.category.text = str(data['profile']['categories'])
        
    def show_dialog(self, instance, field_name):
        """Открывает диалоговое окно для смены данных профиля.
         В качестве аргументов передает значение изменяемого поля и его название."""   
        self.instance = instance
        self.dialog_content = ProfileDialogFieldContent(instance.text, field_name)

        if field_name == 'profile.description':
            self.dialog_content = ProfileDialogTextContent(instance.text, field_name)

        if not self.dialog:   
            self.dialog = MDDialog(
                title = 'Изменение данных:',
                type = 'custom',
                content_cls = self.dialog_content,
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
                        on_release = self.update_data
                    ),
                ]
            ) 
        self.dialog.open()

    def put_request(self, form_data):
        """Отправляет запрос в базу для обновления данных о пользователе или профиле пользователя."""
        data = {
            'username': 'testing4',
            'password': 'personaldata',
        }
        settings.get_jwt_token(data)
        headers = {'Authorization': f'Bearer {settings.access_token}'}
        r = requests.put(settings.HOST_URL + 'user-update/', headers=headers, data=form_data)

        return r

    def close_dialog(self, *args):
        """Закрывает диалоговое окно и сбрасывает значение self.dialog на None."""
        if self.dialog:
            self.dialog.dismiss(force=True)
            self.dialog = None
            self.dialog_content.reset_data()

    def update_data(self, *args):
        """Если запрос выполнен успешно, то меняет значение поля на новые данные.
         Усли же нет, то выводит сообщение об ошибке."""
        r = self.put_request(self.dialog_content.new_data)
        field = self.dialog_content.field_name

        if self.dialog_content.is_profile_field():
            field = self.dialog_content.field_name.split('.')[1]

        if r.status_code == 200:
            self.ids[field].text = self.dialog_content.new_data[self.dialog_content.field_name] 
            self.dialog_content.reset_data()
            self.dialog.dismiss(force=True)
            self.dialog = None
        else:
            self.show_err_snackbar('Ошибка при отправлении.')

    def swich_change(self, instance, *args):
        """Отправляет запрос на изменение булеан поля."""
        r = self.put_request({'profile.is_juridical': instance.active})

        if r.status_code != 200:
            instance.active = not instance.active
            self.show_err_snackbar('Ошибка при отправлении.')

    def show_err_snackbar(self, message):
        """Открывает всплывающее окно с сообщением об ошибке."""
        snack = Snackbar(
            text=message,
            snackbar_x="10dp",
            snackbar_y="10dp",
        )
        snack.size_hint_x = (
            Window.width - (snack.snackbar_x * 2)
        ) / Window.width
        snack.open()


class WindowManager(ScreenManager):
    pass


class ForWorkApp(MDApp):

    def build(self):
        Builder.load_file('graphic/choose_role.kv')
        Builder.load_file('graphic/login.kv')
        Builder.load_file('graphic/registration.kv')
        Builder.load_file('graphic/main_page.kv')
        Builder.load_file('graphic/profile_card.kv')

        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.accent_palette = "Red"

        return Builder.load_file('App.kv')

    def test(self):
        pass


if __name__ == '__main__':
    ForWorkApp().run()
