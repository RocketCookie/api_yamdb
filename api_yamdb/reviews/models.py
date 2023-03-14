from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Genre(models.Model):
    """Модель БД для жанров"""
    name = models.CharField('Наименование', max_length=256)
    slug = models.SlugField('Слаг', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Category(models.Model):
    """Модель БД для категорий"""
    name = models.CharField('Наименование', max_length=256)
    slug = models.SlugField('Слаг', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Title(models.Model):
    """Модель БД для произведений"""
    name = models.CharField('Нименование', max_length=256)
    year = models.IntegerField('Год издания')
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 related_name='title', blank=False, null=True)
    descriptions = models.TextField('Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class GenreTitle(models.Model):
    """Промежуточная модель БД для жанров"""
    ganre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.ganre} {self.title}'
