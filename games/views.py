from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from games.models import Games
from django.views.generic import TemplateView

class ShowGamesViews(TemplateView):
    template_name = "show_games.html"

    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context['games'] = Games.objects.all()

        return context
        
    

