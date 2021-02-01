from django.urls import include, path
from apps.pokemon.views import get_home, get_evolution_chain

urlpatterns = [
    path('api/', include(('apps.pokemon.urls_apis', 'api'), namespace='api')),
    path('', get_home, name='home'),
    path('home', get_home, name='home'),
    path('evolution-chain', get_evolution_chain, name='evolution-chain'),
]