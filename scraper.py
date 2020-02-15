from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import gzip

file_out = gzip.open('./tweets.json.gz', 'wt+')

# Consumer key, consumer secret, access token, access secret.
CONSUMER_KEY    = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN    = ""
ACCESS_SECRET   = ""

KEYWORDS = ["happy", "sad", "depressed", "down", "lit", "rad", "frustrated", "mad", "pissed", "annoyed", "annoying", "angry"]

count = 0
class listener(StreamListener):
    def on_data(self, data):
        print(data, file=file_out)
        global count
        count += 1
        if count % 1000 == 0: print(count)
        return(True)

    def on_error(self, status):
        print(status)

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=KEYWORDS)