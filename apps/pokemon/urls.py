from django.urls import path
from apps.pokemon.views import get_home, get_evolution_chain

urlpatterns = [
    path('', get_home, name='home'),
    path('home', get_home, name='home'),
    path('evolution-chain', get_evolution_chain, name='evolution-chain'),
]