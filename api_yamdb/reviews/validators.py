from django.utils import timezone
from django.core.exceptions import ValidationError
current_year = timezone.now().year


def validate_year(year):
    """Валидация года издаения"""
    if year > current_year:
        raise ValidationError("Проверьте корректность"
                              "года издания")
    return year
