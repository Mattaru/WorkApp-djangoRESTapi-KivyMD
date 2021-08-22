import requests
import json


# Вспомогательный класс для хранения настроек, данных о аутентификации и сессис.
class Settings(object):
    login_data = {}
    access_token = ''
    refresh_token = ''
    registration_role = ''
    order_id = ''
    categories_list = []
    subcategories_list = []
    error_messages = {
        'email_incorrect': "Введите правильный адрес электронной почты.",
        'email_repeat': "Значения поля должны быть уникальны.",
        'username_already_used': "Пользователь с таким именем уже существует.",
        'username_incorrect': "Введите правильное имя пользователя."
                              " Оно может содержать только буквы, цифры и знаки @/./+/-/_.",
    }

    def __init__(self, host):
        self.HOST_URL = host

    def get_jwt_token(self, data):
        """Отправляет запрос на сервер для аутентификации.
        Возвращает ответ с сервера и False в случае успешной аутентификации.
         В случае предоставления не верной информации возвращает True."""
        r = requests.post(self.HOST_URL + 'auth/jwt/create/', data=data)
        err = False

        if r.status_code == 200:
            self.refresh_token = r.json()['refresh']
            self.access_token = r.json()['access']
        else:
            err = True

        return r, err

    def refresh_jwt_token(self):
        """Обновляет 'access' токен. Возвращает ответ на запрос и булиан значение.
         Если у 'refresh' токена не закончился срок годности, то возвращает булиан True"""
        err = False
        data = {'refresh': self.refresh_token}
        r = requests.post(self.HOST_URL + 'auth/jwt/refresh/', data=data)

        if r.status_code != 200:
            err = True

        return r, err

    def make_login_data(self, login, password):
        """Создает словарь с логином и паролем для аутентификации."""
        self.login_data['username'] = login
        self.login_data['password'] = password
