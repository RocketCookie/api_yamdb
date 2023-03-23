from csv import DictReader
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User

MAPPING_DATA = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    GenreTitle: 'genre_title.csv',
    Review: 'review.csv',
    Comment: 'comments.csv'}


class Command(BaseCommand):
    def handle(self, *args, **options):
        for model, data in MAPPING_DATA.items():
            csv_path = Path(settings.BASE_DIR) / 'static/data/' / data
            with open(csv_path, 'r', encoding='utf=8')as csvfile:
                reader = DictReader(csvfile)
                for dict in reader:
                    try:
                        if model == Title:
                            dict['category'] = Category.objects.get(
                                id=dict['category'])
                        elif model in (Review, Comment):
                            dict['author'] = User.objects.get(
                                id=dict['author'])
                        model.objects.get_or_create(**dict)
                    except (ValueError, KeyError, model.DoesNotExist)as e:
                        self.stdout.write(self.style.ERROR(
                            f'Упс! загружая {data}'
                            f' произошла {e}'))
                self.stdout.write(self.style.SUCCESS(f'Ура! {data}'
                                                     ' загружено'))
