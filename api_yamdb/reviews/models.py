from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from .validators import validate_year

from django.db.models import Avg


User = get_user_model()
CHAR_LEN = 256
MIN_SCORE = 1
MAX_SCORE = 10


class Genre(models.Model):
    """Модель БД для жанров"""
    name = models.CharField('Наименование', max_length=CHAR_LEN)
    slug = models.SlugField('Слаг', unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель БД для категорий"""
    name = models.CharField('Наименование', max_length=CHAR_LEN)
    slug = models.SlugField('Слаг', unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель БД для произведений"""

    name = models.CharField('Наименование', max_length=256)
    year = models.IntegerField('Год издания', validators=[validate_year],
                               db_index=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='title', blank=False, null=True)
    description = models.TextField('Описание')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
    
    def __str__(self):
        return self.name



    @property
    def rating(self):
        rating = Review.objects.filter(title=self.pk).aggregate(Avg('score'))
        if rating.get('score__avg'):
            return int(rating.get('score__avg'))
        return None


    


class GenreTitle(models.Model):
    """Промежуточная модель БД для жанров"""
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(verbose_name='Текст')
    score = models.IntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(
                MIN_SCORE, message=f'Оценка должна быть не меньше {MIN_SCORE}!'),
            MaxValueValidator(
                MAX_SCORE, message=f'Оценка должна быть не больше {MAX_SCORE}!'),
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-pub_date']
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            ),
        )


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        verbose_name = 'Комментарий к отзыву'
        verbose_name_plural = 'Комментарии к отзыву'
        ordering = ['-pub_date']
