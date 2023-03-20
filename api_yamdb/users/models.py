from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import validate_username


class User(AbstractUser):

    class Roles(models.TextChoices):
        USER = 'user', _('Пользователь')
        MODERATOR = 'moderator', _('Модератор')
        ADMIN = 'admin', _('Администратор')

    username = models.CharField(
        verbose_name='Никнейм',
        max_length=150,
        unique=True,
        validators=(validate_username,))

    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=254,
        unique=True)

    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True)

    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=True)

    bio = models.TextField(
        verbose_name='Биография',
        blank=True)

    role = models.CharField(
        verbose_name='Права доступа',
        default=Roles.USER,
        choices=Roles.choices,
        max_length=25)

    def __str__(self):
        return self.username[:settings.LENGTH_TEXT]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_moderator(self):
        return self.role == self.Roles.MODERATOR

    @property
    def is_admin(self):
        return (self.role == self.Roles.ADMIN
                or self.is_superuser
                or self.is_staff)
