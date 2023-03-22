import csv
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User



def process_file(name: str):
    return csv.reader(open(os.path.join(settings.BASE_DIR,
                                        'static/data/',
                                        name), 'r', encoding='utf-8'),
                      delimiter=',')


class Command(BaseCommand):
    mapping_data = {'users': {
                    'model': User,
                    'fields': ['id', 'username', 'email', 'role', 'bio',
                               'first_name', 'last_name']},
                    'category': {
                    'model': Category,
                    'fields': ['name', 'slug']},
                    'genre': {
                    'model': Genre,
                    'fields': ['name', 'slug']}
                    }

    def handle(self, *args, **options):
        for data_file, data_config in self.mapping_data.items():
            csv = process_file(f'{data_file}.csv')
            next(csv, None)
            for row in csv:
                data = {field_name: row[index]
                        for index, field_name in enumerate(data_config
                        ['fields'])}
                obj, created = data_config['model'].objects.get_or_create(**data)
            self.stdout.write(self.style.SUCCESS(f'Данные {data_file}'
                                                 ' успешно загружены'))

        csv = process_file('titles.csv')
        next(csv, None)
        for row in csv:
            obj, created = (Title.objects.get_or_create(
                            name=row[1],
                            year=row[2],
                            category=get_object_or_404(
                                Category, id=row[3])))
        self.stdout.write(self.style.SUCCESS('Данные title'
                                             ' успешно загружены'))
        csv = process_file('genre_title.csv')
        next(csv, None)
        for row in csv:
            obj, created = (GenreTitle.objects.get_or_create(
                            title=get_object_or_404(Title, id=row[1]),
                            genre=get_object_or_404(Genre, id=row[2])))
        self.stdout.write(self.style.SUCCESS('Данные genre_title'
                                             ' успешно загружены'))
        csv = process_file('review.csv')
        next(csv, None)
        for row in csv:
            obj, created = (Review.objects.get_or_create(id=row[0],
                            title=get_object_or_404(Title, id=row[1]),
                            text=row[2], author=get_object_or_404(User,
                            id=row[3]), score=row[4],
                            pub_date=row[5]))
        self.stdout.write(self.style.SUCCESS('Данные review'
                                             ' успешно загружены'))
        csv = process_file('comments.csv')
        next(csv, None)
        for row in csv:
            obj, created = (Comment.objects.get_or_create(id=row[0],
                            review=get_object_or_404(Review,
                                                     id=row[1]),
                            text=row[2], author=get_object_or_404(User,
                                                                  id=row[3]),
                            pub_date=row[4]))
        self.stdout.write(self.style.SUCCESS('Данные comments'
                                             ' успешно загружены'))
