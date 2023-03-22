from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils import timezone
from rest_framework import serializers
from rest_framework.status import HTTP_400_BAD_REQUEST

CURRENT_YEAR = timezone.now().year
CHAR_LEN = 256


def validate_username(username):
    """Валидация имени пользователя"""
    if username == 'me':
        raise ValidationError("Username 'me' is not allowed.")
    regex_validator = RegexValidator(
        regex=r'^[\w.@+-]+\Z',
        message='Только буквы, цифры и @/./+/-/_.',
        code='invalid_username'
    )
    regex_validator(username)


def validate_name(name):
    """Валидация длины названия произведения"""
    if len(name) > CHAR_LEN:
        raise serializers.ValidationError(
            "Количество символов в названии не должно"
            "превышать 256 символов",
            code=HTTP_400_BAD_REQUEST)
    return name


def validate_year(year):
    """Валидация года издания"""
    if year > CURRENT_YEAR:
        raise serializers.ValidationError(
            "Проверьте корректность года издания",
            code=HTTP_400_BAD_REQUEST)
    return year
