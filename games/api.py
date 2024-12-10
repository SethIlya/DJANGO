from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets
from rest_framework.decorators import action

from games.models import Games, Studio, Director, Genre, Platform
from games.serializers import GamesSerializer, StudioSerializer, GenreSerializer, DirectorSerializer, PlatformSerializer

class GamesViewset(
    mixins.CreateModelMixin, 
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin, 
    mixins.DestroyModelMixin,
    GenericViewSet):

    queryset = Games.objects.all()
    serializer_class = GamesSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if not user.is_authenticated:
            # Неаутентифицированный пользователь не видит ничего
            return qs.none()
        if user.is_superuser:
            # Суперпользователь может видеть всё
            user_id = self.request.query_params.get('user_id')
            if user_id:
                qs = qs.filter(user_id=user_id)
            return qs
        # Обычный пользователь видит только свои данные
        return qs.filter(user=user)


class StudioViewset(
    mixins.CreateModelMixin, 
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin, 
    mixins.DestroyModelMixin,
    GenericViewSet):

    queryset = Studio.objects.all()
    serializer_class = StudioSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if not user.is_authenticated:
            return qs.none()
        if user.is_superuser:
            user_id = self.request.query_params.get('user_id')
            if user_id:
                qs = qs.filter(user_id=user_id)
            return qs
        return qs.filter(user=user)


class GenreViewset(
    mixins.CreateModelMixin, 
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin, 
    mixins.DestroyModelMixin,
    GenericViewSet):

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if not user.is_authenticated:
            return qs.none()
        if user.is_superuser:
            user_id = self.request.query_params.get('user_id')
            if user_id:
                qs = qs.filter(user_id=user_id)
            return qs
        return qs.filter(user=user)


class PlatformViewset(
    mixins.CreateModelMixin, 
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin, 
    mixins.DestroyModelMixin,
    GenericViewSet):

    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer

def get_queryset(self):
    qs = super().get_queryset()
    user = self.request.user

    if not user.is_authenticated:
        return qs.none()

    # Если суперпользователь - может видеть всех
    if user.is_superuser:
        username = self.request.query_params.get('username')
        if username:
            qs = qs.filter(user__username=username)
        return qs

    # Обычный пользователь видит только свои данные
    return qs.filter(user=user)



class DirectorViewset(
    mixins.CreateModelMixin, 
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin, 
    mixins.DestroyModelMixin,
    GenericViewSet):

    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if not user.is_authenticated:
            return qs.none()
        if user.is_superuser:
            user_id = self.request.query_params.get('user_id')
            if user_id:
                qs = qs.filter(user_id=user_id)
            return qs
        return qs.filter(user=user)


class UserProfileViewSet(GenericViewSet):
    @action(url_path="info", detail=False, methods=["GET"])
    def get_info(self, request, *args, **kwargs):
        user = request.user
        data = {
            "is_authenticated": user.is_authenticated
        }
        if user.is_authenticated:
            data.update({
                "is_superuser": user.is_superuser,
                "name": user.username
            })
        return Response(data)
