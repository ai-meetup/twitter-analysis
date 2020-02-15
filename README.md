# Twitter Analysis


```bash
git clone git@github.com:saffsd/langid.py.git
pip3 install langid.py

git clone git@github.com:myleott/ark-twokenize-py.git
cp ark-twokenize-py/twokenize.py .

pip3 install geopy

pip3 install unidecode
```

## GeoPy

https://github.com/geopy/geopy

Example:

```python
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="Happiness Report")
location = geolocator.geocode("Denver/Chicago")

print(location.address)
print((location.latitude, location.longitude))
print(location.raw)
```

## Reading tweets

```python
with gzip.open('/Users/akonovalov/tweets2.json.gz', 'rt') as fin:
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

    except StopIteration:
        pass
    except EOFError:
        pass
```