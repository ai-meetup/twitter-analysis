#!/usr/bin/python3

import csv
import json
import gzip
import dateutil.parser as dateparser
import langid
import twokenize
import unidecode

from collections import namedtuple

import json

with open('countries.txt', 'rt') as fin:
    COUNTRIES = set([x.strip().lower() for x in fin.read().split('\n')])

with open('us_states.txt', 'rt') as fin:
    US_STATES = [tuple(x.strip().lower().split('\t')) for x in fin.read().split('\n')]

def resolve_state_name(n):
    for state_name, state_code in US_STATES:
        if n == state_name or n == state_code:
            return state_name
    return None

def location_to_json(loc):
    if isinstance(loc, Country):
        return {'type': 'Country', 'country': loc.country }
    elif isinstance(loc, CityCountry):
        return {'type': 'CityCountry', 'city': loc.city, 'country': loc.country }
    elif isinstance(loc, USAState):
        return {'type': 'USAState', 'state': loc.state }
    elif isinstance(loc, USACityState):
        return {'type': 'USACityState', 'city': loc.city, 'state': loc.state }
    else:
        assert False

Country      = namedtuple('Country',     'country')
CityCountry  = namedtuple('CityCountry', 'city country')
USAState     = namedtuple('USState',     'state')
USACityState = namedtuple('USCityState', 'city state')

Coordinates  = namedtuple('Coordinates', 'coordinates')

def resolve_location(loc):
    decoded_loc = unidecode.unidecode(loc).lower().strip()
    parts = [x.strip() for x in decoded_loc.split(',')]

    if len(parts) == 1:
        value, = tuple(parts)
        # Country
        if value in COUNTRIES:
            return Country(value)
        return None

    elif len(parts) == 2:
        first, second = tuple(parts)
        # State, USA
        if second == 'usa' or second == 'us':
            state = resolve_state_name(first)

            if state is not None:
                return USAState(state)
            else:
                return CityCountry(first, 'usa')

        # City, StateCode
        # City, StateName
        elif resolve_state_name(second) is not None:
            state = resolve_state_name(second)
            return USACityState(first, state)
        else:
            # City, Country
            if second in COUNTRIES:
                return CityCountry(first, second)
            else:
                return None
    else:
        return None

with gzip.open('./tweets.json.gz', 'rt') as fin:
    counter = 0
    try:
        while True:
            line = next(fin)
            try:
                js = json.loads(line)
            except:
                continue

            # Skip all retweets.
            if 'retweeted_status' in js and js['retweeted_status'] is not None:
                continue

            # Skip tweets without text.
            if 'extended_tweet' in js and js['extended_tweet'] is not None:
                text = js['extended_tweet']['full_text']
            elif 'text' in js:
                text = js['text']
            else:
                continue

            # Skip tweets in other languages than English.
            (predicted_language, _) = langid.classify(text)
            if not ('lang' in js and js['lang'] == 'en') or predicted_language != 'en':
                continue

            # Extract user location.
            if js['user']['location'] is not None:
                loc = resolve_location(js['user']['location'])
            else:
                loc = None

            if 'geo' in js and js['geo'] is not None:
                assert js['geo']['type'] == 'Point'
                coordinates = js['geo']['coordinates']
            else:
                coordinates = None

            del js['user']

            print(json.dumps({
                'location': location_to_json(loc) if loc is not None else None,
                'coordinates': coordinates,
                'text': text
            }, indent=2))

    except StopIteration:
        pass
    except EOFError:
        pass