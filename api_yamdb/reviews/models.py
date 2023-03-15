from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    #title = models.ForeignKey(
    #   Title,
    #    on_delete=models.CASCADE,
    #    related_name='reviews',
    #    verbose_name='Произведение'
    #)
    text = models.TextField(verbose_name='Текст')
    score = models.IntegerField(verbose_name='Оценка')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата добавления'
    )
    
    class Meta:
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