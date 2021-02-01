from django.db.models import Q
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.response import Response
from apps.pokemon.models import Pokemon, Evolution
import pandas as pd

@api_view(['POST'])
@permission_classes((AllowAny, ))
def search_pokemon(request):
    try:
        name = request.data['name']
        pokemon = Pokemon.objects.get(name__trigram_similar = name)
        pokemon_data = {}
        pokemon_data['id'] = pokemon.pokeapi_id
        pokemon_data['name'] = pokemon.name
        pokemon_data['height'] = pokemon.height
        pokemon_data['weight'] = pokemon.weight
        pokemon_data['hp'] = pokemon.hp
        pokemon_data['attack'] = pokemon.attack
        pokemon_data['special_attack'] = pokemon.special_attack
        pokemon_data['deffense'] = pokemon.deffense
        pokemon_data['special_deffense'] = pokemon.special_deffense
        pokemon_data['speed'] = pokemon.speed
        pokemon_data['url_image'] = pokemon.url_image
        #Consultar las evoluciones y preevoluciones inmediatas de ese pokemon
        chain_evolutions = Evolution.objects.filter(
            Q(evolves_from = pokemon) |
            Q(evolves_to = pokemon)
        )
        #Validar si el pokemon tiene una o más evoluciones
        if chain_evolutions.count() > 0:
            chain_evolutions_id = chain_evolutions.first().pokeapi_id
            #Consultar todas las evoluciones de ese pokemon
            #Esta consulta puede ser mayor o igual que la consulta anterior
            chain_evolutions = Evolution.objects.select_related('evolves_from', 'evolves_to').filter(pokeapi_id = chain_evolutions_id).order_by('id')
            evolutions_params = ['evolves_to_id', 'evolves_to__name', 'evolves_from_id', 'evolves_from__name']
            chain_evolutions = pd.DataFrame(list(chain_evolutions.values_list(*evolutions_params)), columns=evolutions_params)        
            #Obtener y consultar todos los pokemones de la evolución
            pokemones_id = list(set(chain_evolutions['evolves_from_id'].tolist() + chain_evolutions['evolves_to_id'].tolist()))
            pokemones = Pokemon.objects.filter(pokeapi_id__in = pokemones_id)
            pokemones_params = ['pokeapi_id', 'name']
            pokemones = pd.DataFrame(list(pokemones.values_list(*pokemones_params)), columns=pokemones_params)
            """
            Dado que cada pokemon puede evolucionar dos veces máximo, se van a crear 3 arrays que contienen
            los ID de los pokemones según su grado de evolución, donde el grado 0 es el pokemon base -sin evolución-,
            el grado 1 es la 1ra evolución y el grado 2 es la 2da evolución
            """
            #Determinar cuál es el pokemon base
            pokemon_base_id = [chain_evolutions['evolves_from_id'].min()]
            #Pokemones de la 1ra Evolución
            pokemon_first_evolution_id = chain_evolutions.loc[chain_evolutions['evolves_from_id'].isin(pokemon_base_id), 'evolves_to_id'].reset_index(drop=True).tolist()
            #Pokemones de la 2da Evolución
            pokemon_second_evolution_id = chain_evolutions.loc[chain_evolutions['evolves_from_id'].isin(pokemon_first_evolution_id), 'evolves_to_id'].reset_index(drop=True).tolist()
            evolutions = []
            """
            Se itera sobre cada uno de los pokemones de la evolución y se comparan con el pokemon de la consulta
            para verificar su tipo de evolución.
            Si el tipo de evolución es 'Not related', significa que ambos pokemones se derivan de un mismo
            pokemon base
            """
            for pokemon_evolution in pokemones.index:
                pokemon_id = pokemones.iat[pokemon_evolution, 0]
                if pokemon_id != pokemon.pokeapi_id:
                    #Validar si eñ pokemon de la iteración es evolución del pokemon de la consulta
                    if (
                        (pokemon_id in pokemon_second_evolution_id and pokemon.pokeapi_id in pokemon_first_evolution_id) or
                        (pokemon_id in pokemon_second_evolution_id and pokemon.pokeapi_id in pokemon_base_id) or 
                        (pokemon_id in pokemon_first_evolution_id and pokemon.pokeapi_id in pokemon_base_id)
                        ):
                        evolutions.append({
                            'id': pokemon_id,
                            'name': pokemones.loc[pokemones['pokeapi_id']==pokemon_id, 'name'].values[0],
                            'type': 'Evolution'
                        })
                    #Validar si eñ pokemon de la iteración es preevolución del pokemon de la consulta
                    elif (
                        (pokemon.pokeapi_id in pokemon_second_evolution_id and pokemon_id in pokemon_first_evolution_id) or
                        (pokemon.pokeapi_id in pokemon_second_evolution_id and pokemon_id in pokemon_base_id) or 
                        (pokemon.pokeapi_id in pokemon_first_evolution_id and pokemon_id in pokemon_base_id)
                        ):
                        evolutions.append({
                            'id': pokemon_id,
                            'name': pokemones.loc[pokemones['pokeapi_id']==pokemon_id, 'name'].values[0],
                            'type': 'Preevolution'
                        })
                    #Si ninguna de las condiciones anteriores se cumple, significa que los pokemones provienen
                    #de una misma cadena de evolución pero sus evoluciones no están relacionadas directamente
                    else:
                        evolutions.append({
                            'id': pokemon_id,
                            'name': pokemones.loc[pokemones['pokeapi_id']==pokemon_id, 'name'].values[0],
                            'type': 'Not related'
                        })
            pokemon_data['evolutions'] = evolutions
        else:
            pokemon_data['evolutions'] = []
        return Response({'valid':True, 'pokemon': pokemon_data})
    except Exception as e:
        return Response({'valid':False, 'details': str(e)})