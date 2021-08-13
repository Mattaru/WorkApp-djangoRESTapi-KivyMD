from django.contrib.auth.models import User
from django.db import IntegrityError


def get_img_upload_path(instance, filename):
    """Создает путь для загрузки файлов."""
    return f'images/users/{instance.user.username}/avatar/{filename}'


def create_user(data):
    """Создает пользователя по переданным данным.
     Возвращает созданные объект пользователя"""
    user = User.objects.create(
        username=data['username'],
        email=data['email'],
    )
    user.set_password(data['password'])
    user.save()

    return user

def fill_user_profile(data, instance):
    """Заполнить данные профиля пользователя."""
    instance.profile.role = data['role']
    instance.profile.category = data['category']
    instance.profile.save()
