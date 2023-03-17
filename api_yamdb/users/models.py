from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    USER_ROLE_CHOICES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )

    username = models.CharField(
        verbose_name='Никнейм',
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9@.+_-]*$',
                message='Username только буквы, цифры и @/./+/-/_',
                code='invalid_username')])

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
        default=USER,
        choices=USER_ROLE_CHOICES,
        max_length=25)

    def __str__(self):
        return self.username[:settings.LENGTH_TEXT]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser or self.is_staff
