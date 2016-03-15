from __future__ import division, print_function

import twitter
import json
from operator import itemgetter
import string

from gensim import corpora, models
import nltk
from nltk import word_tokenize, FreqDist
import pandas as pd
from time import sleep

# fill in your own credentials
CONSUMER_KEY       = ""
CONSUMER_SECRET    = ""
OAUTH_TOKEN        = ""
OAUTH_TOKEN_SECRET = ""

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)
api = twitter.Twitter(auth=auth)

## function used to retrieve key words
def retrieve_tag(key_word):

    print("Beginning retrieval of " + key_word)
    try:
        timeline = api.search.tweets(q=key_word, lang='en', count=100)
    except:
        print("Reached rate limit; sleeping 15 minutes")
        sleep(900)
        print("Restarting")
        timeline = api.search.tweets(q=key_word, lang='en', count=100)

    ntweets = len(timeline['statuses'])
    if ntweets == 0:
        return timeline
    while ntweets > 0 and len(timeline['statuses']) < 15000:
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

# retrieve
uber = retrieve_tag('#uber')
uber2 = retrieve_tag('#uber%20-RT')

# write file
with open("../data/uber.json", "w") as f:
    json.dump(uber, f, indent=4, sort_keys=True)



