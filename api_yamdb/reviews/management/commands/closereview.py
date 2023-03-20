import os
import csv
from django.conf import settings
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from reviews.models import (Category, Comment, Genre,
                            GenreTitle, Review, Title)
from users.models import User


def process_file(name: str):
    return csv.reader(open(os.path.join(settings.BASE_DIR,
                                        'static/data/',
                                        name), 'r', encoding='utf-8'),
                      delimiter=',')


class Command(BaseCommand):

    def handle(self, *args, **options):

        csv = process_file('users.csv')
        next(csv, None)
        for row in csv:
            obj, created = User.objects.get_or_create(id=row[0],
                                                      username=row[1],
                                                      email=row[2],
                                                      role=row[3],
                                                      bio=row[4],
                                                      first_name=row[5],
                                                      last_name=row[6])
        self.stdout.write(self.style.SUCCESS('Данные о юзерах'
                                             'успешно загружены'))

        csv = process_file('category.csv')
        next(csv, None)
        for row in csv:
            obj, created = Category.objects.get_or_create(name=row[1],
                                                          slug=row[2])
        self.stdout.write(self.style.SUCCESS('Данные о категориях'
                                             'успешно загружены'))

        csv = process_file('genre.csv')
        next(csv, None)
        for row in csv:
            obj, created = Genre.objects.get_or_create(name=row[1],
                                                       slug=row[2])
        self.stdout.write(self.style.SUCCESS('Данные о жанрах'
                                             'успешно загружены'))

        csv = process_file('titles.csv')
        next(csv, None)
        for row in csv:
            obj, created = (Title
                            .objects
                            .get_or_create(name=row[1],
                                           year=row[2],
                                           category=get_object_or_404(Category,
                                                                      id=row[3]
                                                                      )))
        self.stdout.write(self.style.SUCCESS('Данные о произведениях'
                                             'успешно загружены'))

        csv = process_file('genre_title.csv')
        next(csv, None)
        for row in csv:
            obj, created = (GenreTitle
                            .objects
                            .get_or_create(title=get_object_or_404(Title,
                                                                   id=row[1]),
                                           genre=get_object_or_404(Genre,
                                                                   id=row[2])))
        self.stdout.write(self.style.SUCCESS('Данные о жанрах произведений'
                                             'успешно загружены'))

        csv = process_file('review.csv')
        next(csv, None)
        for row in csv:
            obj, created = (Review
                            .objects
                            .get_or_create(id=row[0],
                                           title=get_object_or_404(Title,
                                                                   id=row[1]),
                                           text=row[2],
                                           author=get_object_or_404(User,
                                                                    id=row[3]),
                                           score=row[4],
                                           pub_date=row[5]))
        self.stdout.write(self.style.SUCCESS('Данные о отзывах'
                                             'успешно загружены'))

        csv = process_file('comments.csv')
        next(csv, None)
        for row in csv:
            obj, created = (Comment
                            .objects
                            .get_or_create(id=row[0],
                                           review=get_object_or_404(Review,
                                                                    id=row[1]),
                                           text=row[2],
                                           author=get_object_or_404(User,
                                                                    id=row[3]),
                                           pub_date=row[4]))
        self.stdout.write(self.style.SUCCESS('Данные о комментариях'
                                             'успешно загружены'))
