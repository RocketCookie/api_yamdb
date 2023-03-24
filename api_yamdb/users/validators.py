from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def validate_username(username: str):
    """Валидация имени пользователя"""
    if username == 'me':
        raise ValidationError('Имя пользователя «me» не разрешено.')
    regex_validator = RegexValidator(
        regex=r'^[\w.@+-]+\Z',
        message='Только буквы, цифры и @/./+/-/_.',
        code='invalid_username')
    regex_validator(username)
