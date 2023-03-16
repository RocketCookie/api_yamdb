from datetime import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Comment, Review, Title, User

current_year = datetime.now().year
CHAR_LEN = 256


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, username):
        if username == 'me':
            raise ValidationError(
                'Такой никнейм запрещён!')
        return username


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


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title')
            )
        ]

    def validate_score(self, value):
        if not (1 <= value <= 10):
            raise serializers.ValidationError('Введите число от 1 до 10!')
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
