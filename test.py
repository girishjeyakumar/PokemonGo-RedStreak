
import json
import os
import time

resp = {
  "unknown2": 8145806132888207460, 
  "direction": 1, 
  "auth_ticket": {
    "expire_timestamp_ms": 1469039502454, 
    "start": "9ehk7tePTdEPGR3kwMq+A0fG/NE13lNmbiXqmFoJDAB+UY6bznbviFoR0yXAznk23EdGhw4a5kVJ\nfrces1dfdg==\n", 
    "end": "YI0hQ/dVjL4fk3ZBsaVtFQ==\n"
  }, 
  "responses": {
    "GET_MAP_OBJECTS": {
      "status": 1, 
      "map_cells": [
        {
          "s2_cell_id": 4202522914915876864, 
          "current_timestamp_ms": 1469037702447
        }, 
        {
          "s2_cell_id": 4202522917063360512, 
          "current_timestamp_ms": 1469037702447
        }, 
        {
          "s2_cell_id": 4202522927800778752, 
          "current_timestamp_ms": 1469037702447, 
          "decimated_spawn_points": [
            {
              "latitude": 12.937888358133932, 
              "longitude": 80.23034505179412
            }
          ]
        }, 
        {
          "s2_cell_id": 4202522929948262400, 
          "current_timestamp_ms": 1469037702447
        }, 
        {
          "s2_cell_id": 4202522932095746048, 
          "current_timestamp_ms": 1469037702447
        }, 
        {
          "s2_cell_id": 4202522934243229696, 
          "current_timestamp_ms": 1469037702447
        }, 
        {
          "s2_cell_id": 4202522919210844160, 
          "current_timestamp_ms": 1469037702447
        }, 
        {
          "s2_cell_id": 4202522921358327808, 
          "current_timestamp_ms": 1469037702447
        }, 
        {
          "s2_cell_id": 4202522923505811456, 
          "current_timestamp_ms": 1469037702447
        }, 
        {
          "s2_cell_id": 4202522925653295104, 
          "current_timestamp_ms": 1469037702447
        }, 
        {
          "s2_cell_id": 4202522944980647936, 
          "current_timestamp_ms": 1469037702447
        }, 
        {
          "s2_cell_id": 4202522947128131584, 
          "current_timestamp_ms": 1469037702447
        }, 
        {
          "s2_cell_id": 4202522949275615232, 
          "current_timestamp_ms": 1469037702447
        }, 
        {
          "s2_cell_id": 4202522951423098880, 
          "current_timestamp_ms": 1469037702447
        }, 
        {
          "nearby_pokemons": [
            {
              "distance_in_meters": 200.0, 
              "encounter_id": 15754277110221629837, 
              "pokemon_id": 19
            }, 
            {
              "distance_in_meters": 200.0, 
              "encounter_id": 15961576009561967053, 
              "pokemon_id": 133
            }, 
            {
              "distance_in_meters": 200.0, 
              "encounter_id": 22690897978750397, 
              "pokemon_id": 16
            }
          ], 
          "forts": [
            {
              "last_modified_timestamp_ms": 1467338285215, 
              "enabled": True, 
              "longitude": 80.231216, 
              "latitude": 12.932017, 
              "type": 1, 
              "id": "16f485dd8f8142f68b52d43c1f0210e7.16"
            }, 
            {
              "gym_points": 6565, 
              "last_modified_timestamp_ms": 1469035699064, 
              "guard_pokemon_id": 123, 
              "enabled": True, 
              "longitude": 80.2317, 
              "latitude": 12.931922, 
              "owned_by_team": 3, 
              "id": "4afea7b9b2ae4bf5bf73acde50deb9f9.16"
            }, 
            {
              "last_modified_timestamp_ms": 1469021765668, 
              "enabled": True, 
              "longitude": 80.231579, 
              "latitude": 12.931152, 
              "type": 1, 
              "id": "66cc3dc0b2b34358b06549311da31126.16"
            }
          ], 
          "wild_pokemons": [
            {
              "last_modified_timestamp_ms": 1469037702447, 
              "spawnpoint_id": "3a525c58787", 
              "longitude": 80.23208777065308, 
              "pokemon_data": {
                "pokemon_id": 133
              }, 
              "latitude": 12.93039722469352, 
              "encounter_id": 15961576009561967053, 
              "time_till_hidden_ms": 415885
            }
          ], 
          "current_timestamp_ms": 1469037702447, 
          "catchable_pokemons": [
            {
              "pokemon_id": 133, 
              "spawnpoint_id": "3a525c58787", 
              "longitude": 80.23208777065308, 
              "expiration_timestamp_ms": 1469038118332, 
              "latitude": 12.93039722469352, 
              "encounter_id": 15961576009561967053
            }
          ], 
          "s2_cell_id": 4202522936390713344
        }, 
        {
          "nearby_pokemons": [
            {
              "distance_in_meters": 200.0, 
              "encounter_id": 3718455486281231757, 
              "pokemon_id": 16
            }
          ], 
          "decimated_spawn_points": [
            {
              "latitude": 12.928000832182114, 
              "longitude": 80.22982222916897
            }, 
            {
              "latitude": 12.929008140801553, 
              "longitude": 80.23060646190082
            }, 
            {
              "latitude": 12.92743417468421, 
              "longitude": 80.23130355158837
            }
          ], 
          "wild_pokemons": [
            {
              "last_modified_timestamp_ms": 1469037702447, 
              "spawnpoint_id": "3a525c5886d", 
              "longitude": 80.23173922973986, 
              "pokemon_data": {
                "pokemon_id": 16
              }, 
              "latitude": 12.929584056099431, 
              "encounter_id": 3718455486281231757, 
              "time_till_hidden_ms": 806309
            }
          ], 
          "current_timestamp_ms": 1469037702447, 
          "catchable_pokemons": [
            {
              "pokemon_id": 16, 
              "spawnpoint_id": "3a525c5886d", 
              "longitude": 80.23173922973986, 
              "expiration_timestamp_ms": 1469038508756, 
              "latitude": 12.929584056099431, 
              "encounter_id": 3718455486281231757
            }
          ], 
          "s2_cell_id": 4202522938538196992
        }, 
        {
          "s2_cell_id": 4202522940685680640, 
          "current_timestamp_ms": 1469037702447
        }, 
        {
          "s2_cell_id": 4202522942833164288, 
          "current_timestamp_ms": 1469037702447
        }, 
        {
          "s2_cell_id": 4202522953570582528, 
          "current_timestamp_ms": 1469037702447
        }, 
        {
          "s2_cell_id": 4202522955718066176, 
          "current_timestamp_ms": 1469037702447
        }, 
        {
          "s2_cell_id": 4202522957865549824, 
          "current_timestamp_ms": 1469037702447, 
          "decimated_spawn_points": [
            {
              "latitude": 12.922557030532728, 
              "longitude": 80.22215379463778
            }
          ]
        }
      ]
    }
  }
}

pokemons = {}

seen = {}
visible = []

full_path = os.path.realpath(__file__)
(path, filename) = os.path.split(full_path)
pokemonsJSON = json.load(
        open(path + '/locales/pokemon.' + 'en' + '.json'))

for x in resp['responses']['GET_MAP_OBJECTS']['map_cells']:
        if 'catchable_pokemons' in x:
            for pokemon in x['catchable_pokemons']:
                hash = pokemon['spawnpoint_id'];
                if hash not in seen.keys() or (seen[hash].TimeTillHiddenMs <= pokemon['expiration_timestamp_ms']):
                    visible.append(pokemon)    
                seen[hash] = pokemon['expiration_timestamp_ms']

for pokemon in visible:

        pokeid = str(pokemon['pokemon_id'])
        pokename = pokemonsJSON[pokeid]
  
        disappear_timestamp = time.time() + pokemon['expiration_timestamp_ms']/ 1000

        pokemons[pokemon['spawnpoint_id']] = {
            "lat": pokemon['latitude'],
            "lng": pokemon['longitude'],
            "disappear_time": disappear_timestamp,
            "id": pokeid,
            "name": pokename
        }                  

print pokemons