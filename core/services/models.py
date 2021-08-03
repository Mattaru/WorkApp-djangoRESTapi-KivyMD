import uuid

from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _

from multiselectfield import MultiSelectField


class CategoryChoices(models.TextChoices):
    FIRST = 'первая', _('первая')
    SECOND = 'вторая', _('вторая')
    THREED = 'третья', _('третья')

    __empty__ = _('не выбрана')


class RoleChoices(models.TextChoices):
    CLIENT = 'заказчик', _('заказчик')
    WORKER = 'исполнитель', _('исполнитель')
    FIRM = 'фирма', _('фирма')

    __empty__ = _('не выбрана')


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name=_('пользователь'), on_delete=models.CASCADE, blank=True, null=True)
    region = models.CharField(_('регион'), max_length=255)
    city = models.CharField(_('город'), max_length=255)
    category = MultiSelectField(_('категория'), choices=CategoryChoices.choices, max_length=355, blank=True, null=True)
    role = MultiSelectField(_('роль'), choices=RoleChoices.choices, max_length=113,
                            null=True, blank=True)

    class Meta:
        verbose_name = _('Профиль')
        verbose_name_plural = _('Профили')

    def __str__(self):
        return f'{self.user.username} profile'


class Order(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.ForeignKey(User, verbose_name=_('пользователь'), on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(_('заголовок'), max_length=255, unique=True)
    slug = models.SlugField(max_length=355, blank=True, null=True, unique=True)
    description = models.TextField(_('описание'), blank=True)
    category = MultiSelectField(_('категория'), choices=CategoryChoices.choices, max_length=355, blank=True, null=True)
    order_date = models.DateTimeField(_('дата заказа'), auto_now_add=True)
    open = models.BooleanField(_('открыт'), default=True)

    class Meta:
        verbose_name = _('Заказ')
        verbose_name_plural = _('Заказы')
        ordering = ['order_date']

    def __str__(self):
        return f'{self.user.username} ({self.uuid})'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.slug and self.name:
            self.slug = slugify(self.title)

        return super().save(*args, **kwargs)


class Message(models.Model):
    sender = models.ForeignKey(User, verbose_name=_('пользователь'), on_delete=models.SET_NULL,
                               related_name='sender', blank=True, null=True)
    receiver = models.ForeignKey(User, verbose_name=_('пользователь'), on_delete=models.SET_NULL,
                                 related_name='receiver', blank=True, null=True)
    timestamp = models.DateTimeField(_('дата заказа'), auto_now_add=True)
    text = models.TextField(_('текст'))
    is_read = models.BooleanField(_('прочитано'), default=False)

    class Meta:
        verbose_name = 'Сообшение'
        verbose_name_plural = 'Сообщения'
        ordering = ['timestamp']

    def __str__(self):
        return f'{self.user.username} ({self.publication_date})'


class Comment(models.Model):
    user = models.ForeignKey(User, verbose_name=_('пользователь'), on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, verbose_name=_('заказ'), on_delete=models.SET_NULL, blank=True, null=True)
    timestamp = models.DateTimeField(_('дата заказа'), auto_now_add=True)
    text = models.TextField(_('текст'))

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['timestamp']

    def __str__(self):
        return f'{self.user.username} ({self.publication_date})'
