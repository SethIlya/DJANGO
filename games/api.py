from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from games.models import Games, Studio, Director, Genre, Platform, Comment
from games.serializers import GamesSerializer, StudioSerializer, GenreSerializer, DirectorSerializer, PlatformSerializer, CommentSerializer

from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count

from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import GenericViewSet

from games.models import Games
from games.serializers import GamesSerializer

class GamesViewset(
    mixins.CreateModelMixin, 
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin, 
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = Games.objects.all()
    serializer_class = GamesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'studio', 'genre', 'director', 'platform']

    @action(detail=False, methods=["GET"], url_path="statistics")
    def statistics(self, request):
        queryset = self.get_queryset()

        most_prod_studio = (
            queryset.values('studio__name')
                    .annotate(count=Count('id'))
                    .order_by('-count')
                    .first()
        )
        most_productive_studio = most_prod_studio['studio__name'] if most_prod_studio else None

        most_pop_genre = (
            queryset.values('genre__name')
                    .annotate(count=Count('id'))
                    .order_by('-count')
                    .first()
        )
        most_popular_genre = most_pop_genre['genre__name'] if most_pop_genre else None

        most_prod_director = (
            queryset.values('director__name', 'director__surname')
                    .annotate(count=Count('id'))
                    .order_by('-count')
                    .first()
        )
        if most_prod_director:
            most_productive_director = f"{most_prod_director['director__name']} {most_prod_director['director__surname']}"
        else:
            most_productive_director = None

        most_pop_platform = (
            queryset.values('platform__name')
                    .annotate(count=Count('id'))
                    .order_by('-count')
                    .first()
        )
        most_popular_platform = most_pop_platform['platform__name'] if most_pop_platform else None

        data = {
            'most_productive_studio': most_productive_studio,
            'most_popular_genre': most_popular_genre,
            'most_productive_director': most_productive_director,
            'most_popular_platform': most_popular_platform,
        }

        return Response(data)

    @action(detail=True, methods=["GET", "POST"], url_path="comments", permission_classes=[IsAuthenticatedOrReadOnly])
    def comments(self, request, pk=None):
        game = self.get_object()

        if request.method == 'GET':
            # Возвращаем только последние 4 комментария
            comments = game.comments.order_by('-created')[:4]
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            if not request.user.is_authenticated:
                return Response({"detail": "Authentication required."}, status=403)
            
            text = request.data.get('text')
            if not text:
                return Response({"detail": "Comment text is required."}, status=400)
            
            comment = Comment.objects.create(game=game, user=request.user, text=text)
            serializer = CommentSerializer(comment)
            return Response(serializer.data, status=201)


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
