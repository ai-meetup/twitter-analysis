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

## References

* Emojis & Sentiment
  + https://github.com/hougrammer/emoji_project
  + [Using millions of emoji occurrences to learn any-domain representations for detecting sentiment, emotion and sarcasm](https://arxiv.org/abs/1708.00524)
  + [Multi-task Emoji Learning](http://ceur-ws.org/Vol-2130/paper2.pdf)
  + [Are Emojis Predictable?](https://arxiv.org/pdf/1702.07285.pdf)
  + [Twitter Sentiment Analysis via Bi-sense Emoji Embedding and Attention-based LSTM](https://arxiv.org/abs/1807.07961)
  + [Using Neural Networks to Predict Emoji Usage from Twitter Data](https://pdfs.semanticscholar.org/4537/69b9e338a6ebf6026225515df8fb012a11e3.pdf)
  + [Exploiting Deep Neural Networks for Tweet-based Emoji Prediction](http://ceur-ws.org/Vol-2244/paper_11.pdf)
* Locations
  + [Hierarchical Geographical Modeling of User Locationsfrom Social Media Posts](https://storage.googleapis.com/pub-tools-public-publication-data/pdf/40840.pdf)
* Events
  + [Learning to Extract Events from Knowledge Base Revisions](https://aritter.github.io/www17.pdf)
