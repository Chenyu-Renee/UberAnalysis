from __future__ import division, print_function

import twitter
import json
from operator import itemgetter
import string
from time import sleep


CONSUMER_KEY = 'mn4YRu8l9vnoGtIwDn8wDBhJb'
CONSUMER_SECRET = 'vB2CgIWUy6f27Gw806d6HQ4WhQMxKgz06kLybZPcwH6sL7PnJ9'
OAUTH_TOKEN = '4804645274-F9D6CIuGlOY4uIthQh1IijuRLLKGEt2aJ84Q8Al'
OAUTH_TOKEN_SECRET = 'RPqhg5a14PzhCe1NdrpI3S4XOX2kGVtT0fm7LJSc514jz'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)
api = twitter.Twitter(auth=auth)

def retrieve_tag(key_word):

    print("Beginning retrieval of " + key_word)
    try:
        timeline = api.search.tweets(q=key_word, lang='en', count=100)
    except:
        print("Reached rate limit; sleeping 15 minutes")
        sleep(900)
        timeline = api.search.tweets(q=key_word, lang='en', count=100)

    ntweets = len(timeline['statuses'])
    if ntweets == 0:
        return timeline
    #### change 30000 to the total number of tweets you want
    while ntweets > 0 and len(timeline['statuses']) < 20000:
        min_id = min([tweet["id"] for tweet in timeline['statuses']])
        try:
            next_timeline = api.search.tweets(q=key_word, lang='en', count=100, max_id=min_id - 1)
        except:
            print("Reached rate limit; sleeping 15 minutes")
            sleep(900)
            print("Restarting")
            next_timeline = api.search.tweets(q=key_word, lang='en', count=100, max_id=min_id - 1)

        ntweets = len(next_timeline['statuses'])
        timeline['statuses'] += next_timeline['statuses']
    return timeline

uber = retrieve_tag('#uber')


with open("hashtagUber.json", "w") as outfile:
    json.dump(uber, outfile, indent=4, sort_keys=True)

with open("hashtagUber.json") as infile:
    tweet_uber = json.load(infile)



























