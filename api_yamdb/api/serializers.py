from rest_framework import serializers
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.exceptions import ValidationError
from reviews.models import Title, Category

from datetime import datetime
current_year = datetime.now().year
CHAR_LEN = 256


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title"""
    # genre = serializers.SlugRelatedField(queryset=Genre.objects.all(),
    #                                      slug_field='slug')
    category = serializers.SlugRelatedField(queryset=Category.objects.all(),
                                            slug_field='slug')

    class Meta:
        model = Title
        fields = '__all__'


def validate_year(data):
    """Проверяет год издания"""
    if data['year'] > current_year:
        raise ValidationError("Проверьте корректность года издания",
                              code=HTTP_400_BAD_REQUEST)


def validate_name_long(data):
    """Проверяет длину поля name"""
    if len(data['name']) > CHAR_LEN:
        raise ValidationError("Строка слишком длинная!",
                              code=HTTP_400_BAD_REQUEST)
