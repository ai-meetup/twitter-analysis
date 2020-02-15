#!/usr/bin/python3

import csv
import json
import gzip
import dateutil.parser as dateparser
import langid
import twokenize
import unidecode

from collections import namedtuple

with open('countries.txt', 'rt') as fin:
    COUNTRIES = set([x.strip() for x in fin.read().split('\n')])

with open('us_states.txt', 'rt') as fin:
    US_STATES = [tuple(x.strip().split('\t')) for x in fin.read().split('\n')]

LOCATIONS = []

with gzip.open('./tweets.json.gz', 'rt') as fin:
    try:
        while True:
            line = next(fin)
            try:
                js = json.loads(line)
            except:
                continue

            if 'retweeted_status' in js and js['retweeted_status'] is not None:
                continue

            if 'extended_tweet' in js and js['extended_tweet'] is not None:
                text = js['extended_tweet']['full_text']
            elif 'text' in js:
                text = js['text']
            else:
                continue

            if js['user']['location'] is not None:
                loc = js['user']['location']
            else:
                loc = "none"

            print()
            print(dateparser.parse(js['created_at']))

            print(text)
            print(js['lang'])
            print(langid.classify(text))
            print(twokenize.tokenize(text))
            print(loc + "\t\t" + unidecode.unidecode(loc))

            print(js['user']['location'])
            del js['user']

            print(js['geo'])
            print(js['coordinates'])

            # print(json.dumps(js, indent=2))

    except StopIteration:
        pass
    except EOFError:
        pass