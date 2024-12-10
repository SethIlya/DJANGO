from django.contrib import admin

from games.models import Games, Studio, Genre, Director, Platform
# Register your models here.
@admin.register(Games)
class GamesAdmin(admin.ModelAdmin):
    list_display = ['id','name','studio', 'genre', 'director', 'platform']


@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]

@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "surname"]

@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]  