from datetime import datetime

from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Comment, Genre, Review, Title, User

current_year = datetime.now().year
CHAR_LEN = 256


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre"""
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category"""
    class Meta:
        model = Category
        fields = ('name', 'slug')


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, username):
        if username == 'me':
            raise ValidationError(
                'Такой никнейм запрещён!')
        return username


class UserSendTokenSerializer(serializers.ModelSerializer):

    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title"""
    genre = serializers.SlugRelatedField(many=True,
                                         queryset=Genre.objects.all(),
                                         slug_field='slug')
    category = serializers.SlugRelatedField(queryset=Category.objects.all(),
                                            slug_field='slug')
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        genres = instance.genre.all()
        representation['genre'] = [{'name': genre.name, 'slug': genre.slug}
                                   for genre in genres]
        category = instance.category
        representation['category'] = {'name': category.name,
                                      'slug': category.slug}
        return representation

    def validate_year(self, year):
        if year > current_year:
            raise ValidationError("Проверьте корректность года издания",
                                  code=HTTP_400_BAD_REQUEST)
        return year

    def validate_name(self, name):
        if len(name) > CHAR_LEN:
            raise ValidationError("Количество символов в названии не должно"
                                  "превышать 256 символов",
                                  code=HTTP_400_BAD_REQUEST)
        return name

    def get_rating(self, obj):
        rating = Review.objects.filter(title=obj).aggregate(Avg('score'))
        if rating.get('score__avg'):
            return int(rating.get('score__avg'))
        return None


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
