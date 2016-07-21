#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import getpass
import json
import os
import re
import struct
import sys
import time
from datetime import datetime

import requests
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from geopy.geocoders import GoogleV3
from google.protobuf.internal import encoder
from google.protobuf.message import DecodeError
from requests.adapters import ConnectionError
from requests.models import InvalidURL
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from s2sphere import *

import threading

import pokemon_pb2
from pgoapi import PGoApi

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

API_URL = 'https://pgorelease.nianticlabs.com/plfe/rpc'
LOGIN_URL = \
    'https://sso.pokemon.com/sso/login?service=https://sso.pokemon.com/sso/oauth2.0/callbackAuthorize'
LOGIN_OAUTH = 'https://sso.pokemon.com/sso/oauth2.0/accessToken'
APP = 'com.nianticlabs.pokemongo'

with open('credentials.json') as file:
    credentials = json.load(file)

PTC_CLIENT_SECRET = credentials.get('ptc_client_secret', None)
ANDROID_ID = credentials.get('android_id', None)
SERVICE = credentials.get('service', None)
CLIENT_SIG = credentials.get('client_sig', None)
GOOGLEMAPS_KEY = credentials.get('gmaps_key', None)

SESSION = requests.session()
SESSION.headers.update({'User-Agent': 'Niantic App'})
SESSION.verify = False

global_password = None
global_token = None
access_token = None
DEBUG = False
VERBOSE_DEBUG = False  # if you want to write raw request/response to the console
COORDS_LATITUDE = 0
COORDS_LONGITUDE = 0
COORDS_ALTITUDE = 0
FLOAT_LAT = 0
FLOAT_LONG = 0
NEXT_LAT = 0
NEXT_LONG = 0
auto_refresh = 0
default_step = 0.001
api_endpoint = None
pokemons = []
gyms = {}
pokestops = {}
numbertoteam = {
    0: 'Gym',
    1: 'Mystic',
    2: 'Valor',
    3: 'Instinct',
}
origin_lat, origin_lon = None, None

api = None


def memoize(obj):
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = obj(*args, **kwargs)
        return cache[key]

    return memoizer


def parse_unicode(bytestring):
    decoded_string = bytestring.decode(sys.getfilesystemencoding())
    return decoded_string


def debug(message):
    if DEBUG:
        print '[-] {}'.format(message)


def time_left(ms):
    s = ms / 1000
    (m, s) = divmod(s, 60)
    (h, m) = divmod(m, 60)
    return (h, m, s)


def encode(cellid):
    output = []
    encoder._VarintEncoder()(output.append, cellid)
    return ''.join(output)


def get_cellid(lat, lng):
    origin = CellId.from_lat_lng(LatLng.from_degrees(lat, lng)).parent(15)
    walk = [origin.id()]

    # 10 before and 10 after
    next = origin.next()
    prev = origin.prev()
    for i in range(10):
        walk.append(prev.id())
        walk.append(next.id())
        next = next.next()
        prev = prev.prev()
    return ''.join(map(encode, sorted(walk)))


def getNeighbors():
    origin = CellId.from_lat_lng(LatLng.from_degrees(FLOAT_LAT,
                                                     FLOAT_LONG)).parent(15)
    walk = [origin.id()]

    # 10 before and 10 after

    next = origin.next()
    prev = origin.prev()
    for i in range(10):
        walk.append(prev.id())
        walk.append(next.id())
        next = next.next()
        prev = prev.prev()
    return walk


def f2i(float):
    return struct.unpack('<Q', struct.pack('<d', float))[0]


def f2h(float):
    return hex(struct.unpack('<Q', struct.pack('<d', float))[0])


def h2f(hex):
    return struct.unpack('<d', struct.pack('<Q', int(hex, 16)))[0]


def retrying_set_location(location_name):
    """
    Continue trying to get co-ords from Google Location until we have them
    :param location_name: string to pass to Location API
    :return: None
    """

    while True:
        try:
            set_location(location_name)
            return
        except (GeocoderTimedOut, GeocoderServiceError), e:
            debug(
                'retrying_set_location: geocoder exception ({}), retrying'.format(str(e)))
        time.sleep(1.25)


def set_location(location_name):
    geolocator = GoogleV3()
    prog = re.compile('^(\-?\d+(\.\d+)?),\s*(\-?\d+(\.\d+)?)$')
    global origin_lat
    global origin_lon
    if prog.match(location_name):
        local_lat, local_lng = [float(x) for x in location_name.split(",")]
        alt = 0
        origin_lat, origin_lon = local_lat, local_lng
    else:
        loc = geolocator.geocode(location_name)
        origin_lat, origin_lon = local_lat, local_lng = loc.latitude, loc.longitude
        alt = loc.altitude
        print '[!] Your given location: {}'.format(loc.address.encode('utf-8'))

    print('[!] lat/long/alt: {} {} {}'.format(local_lat, local_lng, alt))
    set_location_coords(local_lat, local_lng, alt)


def set_location_coords(lat, long, alt):
    global COORDS_LATITUDE, COORDS_LONGITUDE, COORDS_ALTITUDE
    global FLOAT_LAT, FLOAT_LONG
    FLOAT_LAT = lat
    FLOAT_LONG = long
    COORDS_LATITUDE = f2i(lat)  # 0x4042bd7c00000000 # f2i(lat)
    COORDS_LONGITUDE = f2i(long)  # 0xc05e8aae40000000 #f2i(long)
    COORDS_ALTITUDE = f2i(alt)


def get_location_coords():
    return (COORDS_LATITUDE, COORDS_LONGITUDE, COORDS_ALTITUDE)


def retrying_api_req(service, api_endpoint, access_token, *args, **kwargs):
    while True:
        try:
            response = api_req(service, api_endpoint, access_token, *args,
                               **kwargs)
            if response:
                return response
            debug('retrying_api_req: api_req returned None, retrying')
        except (InvalidURL, ConnectionError, DecodeError), e:
            debug('retrying_api_req: request error ({}), retrying'.format(
                str(e)))
        time.sleep(1)


def api_req(service, api_endpoint, access_token, *args, **kwargs):
    p_req = pokemon_pb2.RequestEnvelop()
    p_req.rpc_id = 1469378659230941192

    p_req.unknown1 = 2

    (p_req.latitude, p_req.longitude, p_req.altitude) = \
        get_location_coords()

    p_req.unknown12 = 989

    if 'useauth' not in kwargs or not kwargs['useauth']:
        p_req.auth.provider = service
        p_req.auth.token.contents = access_token
        p_req.auth.token.unknown13 = 14
    else:
        p_req.unknown11.unknown71 = kwargs['useauth'].unknown71
        p_req.unknown11.unknown72 = kwargs['useauth'].unknown72
        p_req.unknown11.unknown73 = kwargs['useauth'].unknown73

    for arg in args:
        p_req.MergeFrom(arg)

    protobuf = p_req.SerializeToString()

    r = SESSION.post(api_endpoint, data=protobuf, verify=False)

    p_ret = pokemon_pb2.ResponseEnvelop()
    p_ret.ParseFromString(r.content)

    if VERBOSE_DEBUG:
        print 'REQUEST:'
        print p_req
        print 'Response:'
        print p_ret
        print '''

'''
    time.sleep(0.51)
    return p_ret


def get_api_endpoint(service, access_token, api=API_URL):
    profile_response = None

    while not profile_response:
        profile_response = retrying_get_profile(service, access_token, api,
                                                None)
        if not hasattr(profile_response, 'api_url'):
            debug(
                'retrying_get_profile: get_profile returned no api_url, retrying')
            profile_response = None
            continue
        if not len(profile_response.api_url):
            debug(
                'get_api_endpoint: retrying_get_profile returned no-len api_url, retrying')
            profile_response = None

    return 'https://%s/rpc' % profile_response.api_url


def retrying_get_profile(service, access_token, api, useauth, *reqq):
    profile_response = None

    while not profile_response:
        profile_response = get_profile(service, access_token, api, useauth,
                                       *reqq)
        if not hasattr(profile_response, 'payload'):
            debug(
                'retrying_get_profile: get_profile returned no payload, retrying')
            profile_response = None
            continue
        if not profile_response.payload:
            debug(
                'retrying_get_profile: get_profile returned no-len payload, retrying')
            profile_response = None

    return profile_response


def get_profile(service, access_token, api, useauth, *reqq):
    req = pokemon_pb2.RequestEnvelop()
    req1 = req.requests.add()
    req1.type = 2
    if len(reqq) >= 1:
        req1.MergeFrom(reqq[0])

    req2 = req.requests.add()
    req2.type = 126
    if len(reqq) >= 2:
        req2.MergeFrom(reqq[1])

    req3 = req.requests.add()
    req3.type = 4
    if len(reqq) >= 3:
        req3.MergeFrom(reqq[2])

    req4 = req.requests.add()
    req4.type = 129
    if len(reqq) >= 4:
        req4.MergeFrom(reqq[3])

    req5 = req.requests.add()
    req5.type = 5
    if len(reqq) >= 5:
        req5.MergeFrom(reqq[4])
    return retrying_api_req(service, api, access_token, req, useauth=useauth)


def get_heartbeat(service, api_endpoint, access_token, response, ):
    m4 = pokemon_pb2.RequestEnvelop.Requests()
    m = pokemon_pb2.RequestEnvelop.MessageSingleInt()
    m.f1 = int(time.time() * 1000)
    m4.message = m.SerializeToString()
    m5 = pokemon_pb2.RequestEnvelop.Requests()
    m = pokemon_pb2.RequestEnvelop.MessageSingleString()
    m.bytes = '05daf51635c82611d1aac95c0b051d3ec088a930'
    m5.message = m.SerializeToString()
    walk = sorted(getNeighbors())
    m1 = pokemon_pb2.RequestEnvelop.Requests()
    m1.type = 106
    m = pokemon_pb2.RequestEnvelop.MessageQuad()
    m.f1 = ''.join(map(encode, walk))
    m.f2 = \
        "\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"
    m.lat = COORDS_LATITUDE
    m.long = COORDS_LONGITUDE
    m1.message = m.SerializeToString()
    response = get_profile(service,
                           access_token,
                           api_endpoint,
                           response.unknown7,
                           m1,
                           pokemon_pb2.RequestEnvelop.Requests(),
                           m4,
                           pokemon_pb2.RequestEnvelop.Requests(),
                           m5, )

    try:
        payload = response.payload[0]
    except (AttributeError, IndexError):
        return

    heartbeat = pokemon_pb2.ResponseEnvelop.HeartbeatPayload()
    heartbeat.ParseFromString(payload)
    return heartbeat


def get_token(service, username, password):
    global global_token, api

    if global_token is None:
        api = PGoApi()
        if api.login(service, username, password):
            global_token = api._auth_provider._auth_token
        return global_token
    else:
        return global_token


def init_config():
    parser = argparse.ArgumentParser()
    config_file = "config.json"

    # If config file exists, load variables from json
    load = {}
    if os.path.isfile(config_file):
        with open(config_file) as data:
            load.update(json.load(data))

    # Read passed in Arguments
    required = lambda x: not x in load
    parser.add_argument("-a", "--auth_service", help="Auth Service ('ptc' or 'google')",
                        required=required("auth_service"))
    parser.add_argument("-u", "--username", help="Username", required=required("username"))
    parser.add_argument("-p", "--password", help="Password", required=required("password"))
    parser.add_argument("-l", "--location", help="Location", required=required("location"))
    parser.add_argument('-st', '--step-limit', help='Steps', required=required("step-limit"))

    parser.add_argument("-L", "--locale",
                        help="Locale for Pokemon names: default en, check locale folder for more options", default="en")
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-i', '--ignore', help='Comma-separated list of Pokémon names or IDs to ignore')
    group.add_argument('-o', '--only', help='Comma-separated list of Pokémon names or IDs to search')

    parser.add_argument('-d', '--debug', help='Debug Mode', action='store_true')
    parser.set_defaults(DEBUG=False)

    config = parser.parse_args()

    # Passed in arguments shoud trump
    for key in config.__dict__:
        if key in load and config.__dict__[key] == None:
            config.__dict__[key] = load[key]

    if config.auth_service not in ['ptc', 'google']:
        raise Exception("[-] Invalid Auth service specified! ('ptc' or 'google')")

    return config


@memoize
def login(config):
    global global_password

    if not global_password:
        if config.password:
            global_password = config.password
        else:
            global_password = getpass.getpass()

    access_token = get_token(config.auth_service, config.username, global_password)

    if access_token is None:
        raise Exception('[-] Wrong username/password')

    print '[+] RPC Session Token: {} ...'.format(access_token[:25])

    api_endpoint = get_api_endpoint(config.auth_service, access_token)

    if api_endpoint is None:
        raise Exception('[-] RPC server offline')

    print '[+] Received API endpoint: {}'.format(api_endpoint)

    profile_response = retrying_get_profile(config.auth_service, access_token,
                                            api_endpoint, None)

    if profile_response is None or not profile_response.payload:
        raise Exception('Could not get profile')

    print '[+] Login successful'

    payload = profile_response.payload[0]
    profile = pokemon_pb2.ResponseEnvelop.ProfilePayload()
    profile.ParseFromString(payload)
    print '[+] Username: {}'.format(profile.profile.username)

    creation_time = datetime.fromtimestamp(int(profile.profile.creation_time) / 1000)
    print '[+] You started playing Pokemon Go on: {}'.format(creation_time.strftime('%Y-%m-%d %H:%M:%S'))

    for curr in profile.profile.currency:
        print '[+] {}: {}'.format(curr.type, curr.amount)

    return api_endpoint, access_token, profile_response


def getNearbyPokemon():
    full_path = os.path.realpath(__file__)
    (path, filename) = os.path.split(full_path)

    config = init_config()

    if config.auth_service not in ['ptc', 'google']:
        print '[!] Invalid Auth service specified'
        return

    print('[+] Locale is ' + config.locale)
    pokemonsJSON = json.load(open(path + '/locales/pokemon.' + config.locale + '.json'))

    if config.debug:
        global DEBUG
        DEBUG = True
        print '[!] DEBUG mode on'

    # only get location for first run
    if not (FLOAT_LAT and FLOAT_LONG):
        print('[+] Getting initial location')
        retrying_set_location(config.location)

    api_endpoint, access_token, profile_response = login(config)

    clear_stale_pokemons()

    steplimit = int(config.step_limit)

    ignore = []
    only = []
    if config.ignore:
        ignore = [i.lower().strip() for i in config.ignore.split(',')]
    elif config.only:
        only = [i.lower().strip() for i in config.only.split(',')]

    pos = 1
    x = 0
    y = 0
    dx = 0
    dy = -1
    steplimit2 = steplimit ** 2

    for step in range(steplimit2):

        debug('looping: step {} of {}'.format((step + 1), steplimit ** 2))
        debug('steplimit: {} x: {} y: {} pos: {} dx: {} dy {}'.format(steplimit2, x, y, pos, dx, dy))

        if -steplimit2 / 2 < x <= steplimit2 / 2 and -steplimit2 / 2 < y <= steplimit2 / 2:
            set_location_coords(x * 0.0025 + origin_lat, y * 0.0025 + origin_lon, 0)
        if x == y or x < 0 and x == -y or x > 0 and x == 1 - y:
            (dx, dy) = (-dy, dx)

        (x, y) = (x + dx, y + dy)

        process_step(config, api_endpoint, access_token, profile_response,
                     pokemonsJSON, ignore, only)

        print('Completed: ' + str(((step + 1) + pos * .25 - .25) / (steplimit2) * 100) + '%')

    global NEXT_LAT, NEXT_LONG

    if (NEXT_LAT and NEXT_LONG and
            (NEXT_LAT != FLOAT_LAT or NEXT_LONG != FLOAT_LONG)):
        print('Update to next location %f, %f' % (NEXT_LAT, NEXT_LONG))
        set_location_coords(NEXT_LAT, NEXT_LONG, 0)
        NEXT_LAT = 0
        NEXT_LONG = 0
    else:
        set_location_coords(origin_lat, origin_lon, 0)

    register_background_thread()

def process_step(config, api_endpoint, access_token, profile_response,
                 pokemonsJSON, ignore, only):
    print('[+] Searching for Pokemon at location {} {}'.format(FLOAT_LAT, FLOAT_LONG))

    origin = LatLng.from_degrees(FLOAT_LAT, FLOAT_LONG)
    step_lat = FLOAT_LAT
    step_long = FLOAT_LONG

    parent = CellId.from_lat_lng(LatLng.from_degrees(FLOAT_LAT, FLOAT_LONG)).parent(15)
    h = get_heartbeat(config.auth_service, api_endpoint, access_token, profile_response)
    hs = [h]
    seen = {}

    for child in parent.children():
        latlng = LatLng.from_point(Cell(child).get_center())
        set_location_coords(latlng.lat().degrees, latlng.lng().degrees, 0)
        hs.append(get_heartbeat(config.auth_service, api_endpoint, access_token, profile_response))

    set_location_coords(step_lat, step_long, 0)

    visible = []

    for hh in hs:

        try:

            for cell in hh.cells:

                for wild in cell.WildPokemon:
                    hash = wild.SpawnPointId;
                    if hash not in seen.keys() or (seen[hash].TimeTillHiddenMs <= wild.TimeTillHiddenMs):
                        visible.append(wild)
                    seen[hash] = wild.TimeTillHiddenMs

                if cell.Fort:
                    for Fort in cell.Fort:
                        if Fort.Enabled == True:
                            if Fort.GymPoints:
                                gyms[Fort.FortId] = [Fort.Team, Fort.Latitude, Fort.Longitude, Fort.GymPoints]
                            elif Fort.FortType:
                                pokestops[Fort.FortId] = [Fort.Latitude, Fort.Longitude]
        except AttributeError:
            break

    for poke in visible:

        pokeid = str(poke.pokemon.PokemonId)
        pokename = pokemonsJSON[pokeid]

        if config.ignore:
            if pokename.lower() in ignore or pokeid in ignore:
                continue
        elif config.only:
            if pokename.lower() not in only and pokeid not in only:
                continue

        disappear_timestamp = time.time() + poke.TimeTillHiddenMs / 1000

        pokemon = {
            "lat": poke.Latitude,
            "lng": poke.Longitude,
            "disappear_time": disappear_timestamp,
            "id": poke.pokemon.PokemonId,
            "name": pokename
        }

        if pokemon not in pokemons: pokemons.append(pokemon)


def clear_stale_pokemons():
    current_time = time.time()

    for pokemon in pokemons:
        if current_time > pokemon['disappear_time']:
            print "[+] removing stale pokemon %s at %f, %f from list" % (
                pokemon['name'].encode('utf-8'), pokemon['lat'], pokemon['lng'])
            pokemons.remove(pokemon)

def register_background_thread(initial_registration=False):

    """
    Start a background thread to search for Pokemon
    :param initial_registration: True if first registration and thread should start immediately, False if it's being called by the finishing thread to schedule a refresh
    :return: None
    """

    debug('register_background_thread called')
    global search_thread

    if initial_registration:
        if search_thread:
            debug('register_background_thread: initial registration requested but thread already running')
            return
        debug('register_background_thread: initial registration')
        search_thread = threading.Thread(target=getNearbyPokemon)

    else:
        debug('register_background_thread: queueing')
        search_thread = threading.Timer(30, main)  # delay, in seconds

    search_thread.daemon = True
    search_thread.name = 'search_thread'
    search_thread.start()

def encounter_and_capture(pokemon):
    lat, lng = (pokemon['lat'], pokemon['lng'])
    altitude = 0.0

    api.set_position(lat, lng, altitude)

    timestamp = "\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000"
    cellid = get_cellid(lat, lng)
    resp = api.get_map_objects(latitude=f2i(lat), longitude=f2i(lng), since_timestamp_ms=timestamp,
                               cell_id=cellid).call()

    encounter_id, spawnpoint_id = -1, -1

    for x in resp['responses']['GET_MAP_OBJECTS']['map_cells']:
        if encounter_id != -1: break
        if 'catchable_pokemons' in x:
            for p in x['catchable_pokemons']:
                if p['pokemon_id'] == pokemon['id']:
                    encounter_id, spawnpoint_id = p['encounter_id'], p['spawnpoint_id']
                    break

    if encounter_id != -1:

        while True:

            api.encounter(encounter_id=encounter_id, spawnpoint_id=spawnpoint_id, player_latitude=f2i(lat),
                          player_longitude=f2i(lng))
            api.catch_pokemon(encounter_id=encounter_id, spawn_point_guid=spawnpoint_id, pokeball=1,
                              normalized_reticle_size=1.0, hit_pokemon=True, spin_modifier=1.0,
                              NormalizedHitPosition=1.0)
            resp = api.call()

            # print('Response dictionary: \n\r{}'.format(json.dumps(resp, indent=2)))

            en_status = resp['responses']['ENCOUNTER']['status']
            cap_status = resp['responses']['CATCH_POKEMON']['status']

            if en_status == 1:

                cp = resp['responses']['ENCOUNTER']['wild_pokemon']['pokemon_data']['cp']

                if cap_status == 1:
                    print '[+] %s of CP %d has been successfully captured' % (pokemon['name'], cp)
                    break
                elif cap_status != 4:
                    if cap_status == 3:
                        reason = 'It ran away!'
                    else:
                        reason = 'It escaped!'
                    print '[!] Encountered but was unable to capture %s of CP %d.%s' % (pokemon['name'], cp, reason)
                    break


def spin(pokestop, fortid):
    lat, lng = pokestop[0], pokestop[1]
    api.set_position(lat, lng, 0.0)
    api.fort_search(fort_id=fortid, fort_latitude=lat, fort_longitude=lng, player_latitude=f2i(lat),
                    player_longitude=f2i(lng))
    resp = api.call()
    if 'experience_awarded' in resp['responses']['FORT_SEARCH']:
        print "[+] Successfully gained %d XP and other items from spinning Pokestop %s" %(resp['responses']['FORT_SEARCH']['experience_awarded'],fortid)

def main():
    getNearbyPokemon()

    print "[+] Number of pokemons found in the neighbourhood: %d" % (len(pokemons))

    print pokemons
    # print pokestops
    # print gyms

    print "---- Capturing Pokemon -----"

    while True:

        for pokemon in pokemons:
            encounter_and_capture(pokemon)
            pokemons.remove(pokemon)
            time.sleep(5)

    # print "---- Spinning Pokestops -----"
    #
    # for key in pokestops:
    #     pokestop = pokestops[key]
    #     spin(pokestop, key)
        # time.sleep(5)

if __name__ == '__main__':
    main()
    register_background_thread(initial_registration=True)
