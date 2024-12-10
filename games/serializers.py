# serializers.py
from rest_framework import serializers
from games.models import Games, Studio, Genre, Platform, Director

class GamesSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        # Проставляем пользователя из контекста
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)

    class Meta:
        model = Games
        fields = "__all__"


class StudioSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)

    class Meta:
        model = Studio
        fields = "__all__"


class GenreSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)

    class Meta:
        model = Genre
        fields = "__all__"


class PlatformSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)

    class Meta:
        model = Platform
        fields = "__all__"


class DirectorSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)

    class Meta:
        model = Director
        fields = "__all__"


