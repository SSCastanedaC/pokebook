from django.db.models import Q
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from apps.pokemon.models import Pokemon, Evolution
import pandas as pd
import requests
import json

# Create your views here.

def query_chain(pokemon_list, chain, evolves_from):
    pokemon_data = {}
    pokemon_name = chain['species']['name']
    pokemon_data['name'] = pokemon_name
    print(chain['species']['name'])
    pokemon_stats = requests.get('https://pokeapi.co/api/v2/pokemon/' + pokemon_name)
    pokemon_stats = pokemon_stats.json()
    pokemon_data['id'] = pokemon_stats['id']
    pokemon_data['hp'] = pokemon_stats['stats'][0]['base_stat']
    pokemon_data['attack'] = pokemon_stats['stats'][1]['base_stat']
    pokemon_data['special_attack'] = pokemon_stats['stats'][2]['base_stat']
    pokemon_data['deffense'] = pokemon_stats['stats'][3]['base_stat']
    pokemon_data['special_deffense'] = pokemon_stats['stats'][4]['base_stat']
    pokemon_data['speed'] = pokemon_stats['stats'][5]['base_stat']
    pokemon_data['height'] = pokemon_stats['height']*10 #Convertir a cm
    pokemon_data['weight'] = pokemon_stats['weight']*100 #Convertir a gramos
    pokemon_data['url_image'] = pokemon_stats['sprites']['front_default']
    pokemon_data['evolves_from'] = evolves_from    
    pokemon_evolutions = chain['evolves_to']
    pokemon_data['evolves_to'] = [pokemon['species']['name'] for pokemon in pokemon_evolutions]
    pokemon_list.append(pokemon_data)
    #for pokemon in pokemon_evolutions:
    [query_chain(pokemon_list, pokemon, pokemon_name) for pokemon in pokemon_evolutions]
    return pokemon_list

def get_home(request):
    context = {}    
    return render (request, 'web/home.html', context)

def get_evolution_chain(request):
    pokemon_list = []
    context = {}
    if request.method == 'POST':
        evolution_chain_id = request.POST['evolution_chain_id']
        evolution_chain = requests.get('https://pokeapi.co/api/v2/evolution-chain/' + evolution_chain_id)
        evolution_chain = evolution_chain.json()
        chain = evolution_chain['chain']
        pokemon_list = query_chain(list(), chain, None)
        context = {
            'query': True,
            'evolution_chain_id': evolution_chain_id,
            'pokemon_list': pokemon_list
        }
    return render (request, 'web/evolution_chain.html', context)