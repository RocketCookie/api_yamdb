from django.core.exceptions import ValidationError
from django.utils import timezone

current_year = timezone.now().year


def validate_year(year):
    """Валидация года издания"""
    if year > current_year:
        raise ValidationError("Проверьте корректность"
                              "года издания")
    return year
