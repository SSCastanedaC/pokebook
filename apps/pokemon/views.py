from django.db.models import Q
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from apps.pokemon.models import Pokemon, Evolution
import pandas as pd
import requests
import json

"""
Se declara una función recursiva que permitirá almacenar en las listas
pokemon_list y pokemon_chain_evolution la lista de pokemones y las cadenas
de evolución respectivamente.
Los parámetros de esta función son:
- pokemon_list / lista: En esta variable se almacena la lista de pokemones
- pokemon_chain_evolution: Es esta variable se almacena la cadena de evolución
    para los pokemones
- chain / diccionario: Este diccionario contiene las futuras evoluciones para 
    cada pokemon
- evolves_from / string: Esta variable almacena el nombre del pokemon para el
    cual se están consultando sus evoluciones

"""
def query_chain(pokemon_list, pokemon_chain_evolution, chain, evolves_from):
    #Se crea un diccionario para almacenar las propiedades del pokemon
    pokemon_data = {}
    pokemon_name = chain['species']['name']
    pokemon_data['name'] = pokemon_name
    #Se consulta la API para obtener las propiedades del pokemon y almacenarlas en pokemon_data
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
    #Se almacena el pokemon en pokemon_list
    pokemon_list.append(pokemon_data)
    #Se almacena el nombre del pokemon y su evolución
    pokemon_chain_evolution.append({'evolves_from':evolves_from, 'evolves_to':pokemon_name})
    pokemon_evolutions = chain['evolves_to']
    [query_chain(pokemon_list, pokemon_chain_evolution, pokemon_chain, pokemon_name) for pokemon_chain in pokemon_evolutions]
    return (pokemon_list, pokemon_chain_evolution)

def save_pokemon(pokemon_list):
    new_pokemon_list = []
    for pokemon in pokemon_list:
        pokemon_new = Pokemon()
        pokemon_new.pokeapi_id = int(pokemon['id'])
        pokemon_new.name = pokemon['name']
        pokemon_new.height = pokemon['height']
        pokemon_new.weight = pokemon['weight']
        pokemon_new.hp = pokemon['hp']
        pokemon_new.attack = pokemon['attack']
        pokemon_new.special_attack = pokemon['special_attack']
        pokemon_new.deffense = pokemon['deffense']
        pokemon_new.special_deffense = pokemon['special_deffense']
        pokemon_new.speed = pokemon['speed']
        pokemon_new.url_image = pokemon['url_image']
        new_pokemon_list.append(pokemon_new)
    Pokemon.objects.bulk_create(new_pokemon_list)
    return None

def save_pokemon_chain_evolution(evolution_chain_id, pokemon_chain_evolution, pokemon_list):
    evolution_list = []
    for evolution in pokemon_chain_evolution[1:]:
        evolution_new = Evolution()
        evolution_new.pokeapi_id = evolution_chain_id
        evolution_new.evolves_from_id = list(filter(lambda pokemon: pokemon['name'] == (evolution['evolves_from']), pokemon_list))[0]['id']
        evolution_new.evolves_to_id = list(filter(lambda pokemon: pokemon['name'] == (evolution['evolves_to']), pokemon_list))[0]['id']
        evolution_list.append(evolution_new)
    Evolution.objects.bulk_create(evolution_list)
    return None

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
        #Se instancia una lista vacía para almacenar los datos de los pokemones
        pokemon_list = list()
        #Se instancia una lista vacía para almacenar la cadena de evolución de los pokemones
        pokemon_chain_evolution = list()
        pokemon_list, pokemon_chain_evolution = query_chain(pokemon_list, pokemon_chain_evolution, chain, 0)
        #Se valida si la cadena de evolución ya está almacenada en DB, en caso que no se almacena
        #la cadena de evolución y los datos de cada uno de los pokemones que pertenecen a ella
        if Evolution.objects.filter(pokeapi_id = evolution_chain_id).count() == 0:
            save_pokemon(pokemon_list)
            save_pokemon_chain_evolution(evolution_chain_id, pokemon_chain_evolution, pokemon_list)
        context = {
            'query': True,
            'evolution_chain_id': evolution_chain_id,
            'pokemon_list': pokemon_list,
            'pokemon_chain_evolution': pokemon_chain_evolution,
        }
    return render (request, 'web/evolution_chain.html', context)