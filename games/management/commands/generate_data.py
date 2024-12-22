from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
import random

from games.models import Games, Studio, Genre, Platform, Director, Comment

class Command(BaseCommand):
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Количество записей для генерации',
        )

    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])
        count = options['count']
        
        # Проверяем наличие связанных данных. Если пусто, создаем заглушки:
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
            User.objects.create_user(username='commenter1', password='pass123')
            User.objects.create_user(username='commenter2', password='pass123')

        studios = list(Studio.objects.all())
        genres = list(Genre.objects.all())
        platforms = list(Platform.objects.all())
        directors = list(Director.objects.all())
        users = list(User.objects.all())

        for _ in range(count):
            game = Games.objects.create(
                name=fake.sentence(nb_words=2), 
                studio=random.choice(studios),
                genre=random.choice(genres),
                platform=random.choice(platforms),
                director=random.choice(directors),
            )

 
            for _c in range(random.randint(2, 3)):
                user = random.choice(users)
                Comment.objects.create(
                    game=game,
                    user=user,
                    text=fake.sentence(nb_words=10)
                )

        self.stdout.write(self.style.SUCCESS(f'{count} записей успешно сгенерировано!'))
