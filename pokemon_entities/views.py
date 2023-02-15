import folium
import json

from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils import timezone
from django.utils.timezone import localtime

from .models import Pokemon
from .models import PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    local_time = localtime()
    pokemons = Pokemon.objects.all()

    pokemon_entities = PokemonEntity.objects.filter(
        appeared_at__lt=local_time,
        disappeared_at__gt=local_time
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in pokemon_entities.all():
        add_pokemon(
            folium_map, pokemon_entity.latitude,
            pokemon_entity.longitude,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.image.url),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = get_object_or_404(Pokemon, id=pokemon_id)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in requested_pokemon.pokemon_entities.all():
        add_pokemon(
            folium_map,
            pokemon_entity.latitude,
            pokemon_entity.longitude,
            request.build_absolute_uri(requested_pokemon.image.url)
        )

    pokemons_on_page = {
        'pokemon_id': requested_pokemon.id,
        'img_url': request.build_absolute_uri(requested_pokemon.image.url),
        'title': requested_pokemon.title,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'description': requested_pokemon.description,
    }
    next_evolution_pokemon = requested_pokemon.next_evolutions.first()
    if next_evolution_pokemon:
        pokemons_on_page.update({
                "next_evolution": {
                    'title': next_evolution_pokemon.title,
                    'pokemon_id': next_evolution_pokemon.id,
                    'img_url': request.build_absolute_uri(
                        next_evolution_pokemon.image.url
                    )
                }
        })
    if requested_pokemon.previous_evolution:
        pokemons_on_page.update({
            "previous_evolution": {
                'title': requested_pokemon.previous_evolution.title,
                'pokemon_id': requested_pokemon.previous_evolution.id,
                'img_url': request.build_absolute_uri(
                    requested_pokemon.previous_evolution.image.url
                )
            }
        })

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemons_on_page
    })
