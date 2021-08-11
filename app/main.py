import datetime
import requests

from kivy.properties import DictProperty, StringProperty
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
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelThreeLine
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList
from kivymd.uix.screen import Screen
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.toolbar import MDBottomAppBar, MDToolbar

from settings import Settings
from widgets import OrderLIstItem, OrderContent, ProfileDialogContent


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
    message = StringProperty('')
    form_data = DictProperty({})

    def validate_data(self, login_title):
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
    message = StringProperty('')
    background_color = [255, 255, 255, 0.6]
    form_data = DictProperty({})
    category_list = []

    def validate_data(self, reg_label):
        """Получить разрешение на отображение связанной страницы."""
        self.make_data_for_send()
        check_data = self.check_form_data(reg_label)

        if not check_data:
            return False

        check_password = self.check_password(reg_label)

        if not check_password:
            return False

        settings.make_login_data(
            self.form_data['username'],
            self.form_data['password']
        )

        r = self.send_registration_request(self.form_data, reg_label)

        if r.status_code == 201:
            response, err = settings.get_jwt_token(settings.login_data)

            if response.status_code == 200:
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
        self.form_data['profile.category'] = self.category_list
        self.form_data['profile.role'] = settings.registration_role

    def check_form_data(self, reg_label):
        """Проверяет наличие всей нужной информации для регистрации.
         Если введена не вся информация, то выводится сообщение об ошибке."""
        if not ('username' in self.form_data.keys()):
            self.message = 'Введите логин.'
            reg_label.color = (1, 0, 0, 1)
            return False
        if not ('password' in self.form_data.keys()):
            self.message = 'Введите пароль.'
            reg_label.color = (1, 0, 0, 1)
            return False
        elif not ('re_password' in self.form_data.keys()):
            self.message = 'Введите пароль повторно.'
            reg_label.color = (1, 0, 0, 1)
            return False
        elif not ('email' in self.form_data.keys()):
            self.message = 'Введите почтовы адрес.'
            reg_label.color = (1, 0, 0, 1)
            return False
        elif not self.form_data['profile.category']:
            self.message = 'Выберите вид работ.'
            reg_label.color = (1, 0, 0, 1)
            return False

        return True

    def check_password(self, reg_label):
        """Проверяет совпадают ли введенные пароли, а так же длинну пароля,
         если нет то выводит сообщение об ошибке."""
        if self.form_data['password'] != self.form_data['re_password']:
            self.message = 'Введенные пароли не совпадают.'
            reg_label.color = (1, 0, 0, 1)
            return False
        elif len(self.form_data['password']) < 8:
            self.message = 'Пароль меньше 8 символов.'
            reg_label.color = (1, 0, 0, 1)
            return False

        return True

    def send_registration_request(self, form_data, reg_label):
        """Отправить запрос к базе данных с информацией для регистрации пользователя.
         Если статус ответа не 200, то обрабатывает ошибки и выводит сообщения о них."""
        r = requests.post(settings.HOST_URL + 'auth/users/', data=form_data)

        email = ('email' in r.json().keys())

        if email:
            email_incorrect = r.json()['email'][0] == settings.error_messages['email_incorrect']
            email_repeat = r.json()['email'][0] == settings.error_messages['email_repeat']

            if email and email_incorrect:
                reg_label.color = (1, 0, 0, 1)
                self.message = 'Не корректно введена почта.'
            elif email and email_repeat:
                reg_label.color = (1, 0, 0, 1)
                self.message = 'Почта уже используется.'

        username = ('username' in r.json().keys())

        if username:
            username_already_used = r.json()['username'][0] == settings.error_messages['username_already_used']
            username_incorrect = r.json()['username'][0] == settings.error_messages['username_incorrect']

            if username and username_already_used:
                reg_label.color = (1, 0, 0, 1)
                self.message = 'Имя пользователя занято.'

            if username and username_incorrect:
                reg_label.color = (1, 0, 0, 1)
                self.message = 'Не допустимые символы в имени.'

        return r

    def reset_data(self):
        """Обновить все данные класса."""
        self.form_data = {}
        self.category_list = []

    def go_back(self):
        """Перенаправляет на страницу выбора роли."""
        self.manager.current = 'choose_role'
        self.manager.transition.direction = 'right'


class MainPage(Screen):
    def pre_enter(self):
        pass

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
        self.ids.phone_number.text = data['profile']['phone_number']
        self.ids.description.text = data['profile']['description']
        self.ids.work_experience.text = data['profile']['work_experience']
        self.ids.is_juridical.active = data['profile']['is_juridical']
        self.ids.region.text = data['profile']['region']
        self.ids.city.text = data['profile']['city']

        if data['profile']['category']:     
            self.ids.category.text = str(data['profile']['category'])
        
    def show_dialog(self, instance, field_name):
        """Открывает диалоговое окно для смены данных профиля.
         В качестве аргументов передает значение изменяемого поля и его название."""   
        self.instance = instance

        if not self.dialog:
            self.dialog_content = ProfileDialogContent(instance.text, field_name)
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

    def put_request(self, data):
        """Отправляет запрос в базу для обновления данных о пользователе или профиле пользователя."""
        data = {
            'username': 'testing4',
            'password': 'personaldata',
        }
        settings.get_jwt_token(data)
        headers = {'Authorization': f'Bearer {settings.access_token}'}
        r = requests.put(settings.HOST_URL + 'user-update/', headers=headers, data=data)

        return r

    def close_dialog(self, *args):
        """Закрывает диалоговое окно и и спрасывает значение self.dialog на None."""
        if self.dialog:
            self.dialog.dismiss(force=True)
            self.dialog = None

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
        r = self.put_request(data={'profile.is_juridical': instance.active})
        print(f'Status: {r.status_code} swich-status: {instance.active} data: {r}')
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

        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.accent_palette = "Red"

        return Builder.load_file('App.kv')

    def test(self):
        pass


if __name__ == '__main__':
    ForWorkApp().run()
