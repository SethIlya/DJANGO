# Generated by Django 4.2.15 on 2024-11-26 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0008_platform_games_platform'),
    ]

    operations = [
        migrations.AddField(
            model_name='games',
            name='picture',
            field=models.ImageField(null=True, upload_to='games', verbose_name='Картинка'),
        ),
    ]
