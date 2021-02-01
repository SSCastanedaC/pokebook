from django.conf.urls import url
from django.urls import include, path
from apps.pokemon.apis import search_pokemon

urlpatterns = [
    path('search_pokemon', search_pokemon),
]