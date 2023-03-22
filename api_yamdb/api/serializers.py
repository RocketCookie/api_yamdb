from datetime import datetime

from django.db.models import Avg
from rest_framework import serializers
from rest_framework.status import HTTP_400_BAD_REQUEST

from .validators import validate_username
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
    """Сериализатор создания пользователя"""
    username = serializers.CharField(
        max_length=150, required=True, validators=(validate_username,))

    class Meta:
        model = User
        fields = ('email', 'username')
        extra_kwargs = {'email': {'validators': []},
                        'username': {'validators': []}}

    def validate(self, data):
        if User.objects.filter(username=data.get('username'),
                               email=data.get('email')).exists():
            return data
        if User.objects.filter(username=data.get('username')):
            raise serializers.ValidationError(
                'Данный пользователь уже существует!')
        if User.objects.filter(email=data.get('email')):
            raise serializers.ValidationError(
                'Данная почта уже существует!')
        return data


class UserSendTokenSerializer(serializers.ModelSerializer):
    """Сериализатор проверки кода подтверждения"""
    username = serializers.CharField(max_length=150,)
    confirmation_code = serializers.CharField(max_length=39,)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User"""
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title"""
    genre = serializers.SlugRelatedField(many=True,
                                         queryset=Genre.objects.all(),
                                         slug_field='slug')
    category = serializers.SlugRelatedField(queryset=Category.objects.all(),
                                            slug_field='slug')
    rating = serializers.IntegerField(read_only=True)

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
            raise serializers.ValidationError(
                "Проверьте корректность года издания",
                code=HTTP_400_BAD_REQUEST)
        return year

    def validate_name(self, name):
        if len(name) > CHAR_LEN:
            raise serializers.ValidationError(
                "Количество символов в названии не должно"
                "превышать 256 символов",
                code=HTTP_400_BAD_REQUEST)
        return name


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review"""
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Review
        exclude = ('title',)

    def validate(self, data):
        """Запрещает пользователям оставлять повторные отзывы."""
        if not self.context.get('request').method == 'POST':
            return data
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Можно оставить только один отзыв на произведение!')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment"""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username')

    class Meta:
        model = Comment
        exclude = ('review',)
