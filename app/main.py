import requests

from kivy.properties import DictProperty, StringProperty
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.core.text import LabelBase
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.list import TwoLineIconListItem, IconRightWidget, IconLeftWidget
from kivymd.uix.screen import Screen
from kivymd.uix.toolbar import MDBottomAppBar, MDToolbar

from settings import Settings
from widgets import OrderLIstItem


from kivy.core.window import Window
Window.size = (300, 600)


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
    #
    # def go_back(self):
    #     """Перенаправляет на страницу выбора роли."""
    #     self.manager.current = 'choose_role'
    #     self.manager.transition.direction = 'left'


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
        self.manager.transition.direction = 'left'


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
            self.ids.content.clear_widgets()

            for i in r.json():
                item = OrderLIstItem(
                    order_id=i['id'],
                    text=i['title'],
                    on_release=self.show_list,
                    icon="information-variant"
                )
                self.ids.content.add_widget(item)

    def show_list(self, instance):
        settings.order_id = instance.order_id
        self.manager.current = 'order_detail'
        self.manager.transition.direction = 'left'

    def test(self):
        pass


class OrderDetail(Screen):

    def on_enter(self):
        data = {
            'username': 'testing4',
            'password': 'personaldata',
        }
        settings.get_jwt_token(data)
        headers = {'Authorization': f'Bearer {settings.access_token}'}
        r = requests.get(settings.HOST_URL + f'order/{settings.order_id}', headers=headers)

        # self.ids.gg.add_widget()

    def go_home(self):
        self.manager.current = 'main_page'
        self.manager.transition.direction = 'right'


class WindowManager(ScreenManager):
    pass


class ForWorkApp(MDApp):

    def build(self):
        kv = Builder.load_file('App.kv')

        self.theme_cls.primary_palette = 'Green'
        self.theme_cls.accent_palette = "Red"

        return kv

    def test(self):
        pass


if __name__ == '__main__':
    ForWorkApp().run()
