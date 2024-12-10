from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
import random

from games.models import Games, Studio, Genre, Platform, Director

class Command(BaseCommand):
    help = "Создать случайные записи в модель Games."
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Количество записей для генерации (по умолчанию 10)',
        )

    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])
        count = options['count']
        
        # Проверяем наличие связанных данных. Если пусто, вы можете создать заглушки:
        if Studio.objects.count() == 0:
            Studio.objects.create(name="Default Studio")
        if Genre.objects.count() == 0:
            Genre.objects.create(name="Action")
        if Platform.objects.count() == 0:
            Platform.objects.create(name="PC")
        if Director.objects.count() == 0:
            Director.objects.create(name="Иван", surname="Иванов")
        if User.objects.count() == 0:
            User.objects.create_user(username='testuser', password='testpass')

        studios = list(Studio.objects.all())
        genres = list(Genre.objects.all())
        platforms = list(Platform.objects.all())
        directors = list(Director.objects.all())
        users = list(User.objects.all())

        for _ in range(count):
            Games.objects.create(
                name=fake.sentence(nb_words=3),  # более "игровое" название
                studio=random.choice(studios),
                genre=random.choice(genres),
                platform=random.choice(platforms),
                director=random.choice(directors),

            )

        self.stdout.write(self.style.SUCCESS(f'{count} записей успешно сгенерировано!'))
