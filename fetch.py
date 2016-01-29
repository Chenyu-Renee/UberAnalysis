from __future__ import division, print_function

import twitter
import json
from operator import itemgetter
import string

from gensim import corpora, models
import nltk
from nltk import word_tokenize, FreqDist
import pandas as pd

# don't forget to put in your credentials
CONSUMER_KEY       = ""
CONSUMER_SECRET    = ""
OAUTH_TOKEN        = ""
OAUTH_TOKEN_SECRET = ""

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)
api = twitter.Twitter(auth=auth)

# first part of code is written by me
uber_list=[]
length = 100
last_id = 1
n = 0
while length == 100 and n < 100:
    uber = api.search.tweets(q='#uber', lang='en', max_id=last_id-1, count=100)
    uber_list.append(uber)
    length = len(uber['statuses'])
    last_id = uber['statuses'][length-1]['id']
    n += 1

all_list = [j['text'] for i in uber_list for j in i['statuses']]
names = [j['user']['screen_name'] for i in uber_list for j in i['statuses']]
locations = [j['user']['location'] for i in uber_list for j in i['statuses']]

# if want to pull out info for only verified account
verified = [j['text'] for i in uber_list for j in i['statuses'] if j['user']['verified'] is True]
names = [j['user']['screen_name'] for i in uber_list for j in i['statuses'] if j['user']['verified'] is True]


text_uber = " ".join([text for text in all_list])
textnltk_uber = nltk.Text(word_tokenize(text_uber))
textnltk_uber.collocations()
textnltk_uber.count("taxi")
textnltk_uber.concordance("taxi")

stopwords = nltk.corpus.stopwords.words("english")

def tweet_clean(t):
    cleaned_words = [word for word in t.split()
                     if "http" not in word
                     and not word.startswith("@")
                     and not word.startswith(".@")
                     and not word.startswith("#")
                     and word != "RT"]
    return " ".join(cleaned_words)

 
def all_punct(x):
    return all([char in string.punctuation for char in x])


def my_tokenize(text):
    init_words = word_tokenize(text)
    return [w.lower() for w in init_words if
            not all_punct(w) and w.lower() not in stopwords]

tweet_list_cleaned = [my_tokenize(tweet_clean(tweet)) for tweet in all_list]

tokens_list_cleaned = []
for i in tweet_list_cleaned:
    tokens_list_cleaned+=i

fd = FreqDist(nltk.Text(tokens_list_cleaned))


## This part of code and function is modified from
## Jarrod's function; used to retrieve key words
## pretty much does what the first part does
## but less messy
## although, I have the same problem with only being
## able to retrieve around 2700 tweets for #uber
## it just stops for some reason, (not going to sleep),
## might need to ask Jarrod why

def retrieve_tag(key_word):

    print("Beginning retrieval of " + key_word)
    try:
        timeline = api.search.tweets(q=key_word, lang='en', count=100)
    except:
        print("Reached rate limit; sleeping 15 minutes")
        sleep(900)
        timeline = api.search.tweets(q=key_word, lang='en', count=100)

    ntweets = len(timeline['statuses'])
    if ntweets < 100:
        return timeline
    while ntweets == 100:
        min_id = min([tweet["id"] for tweet in timeline['statuses']])
        try:
            next_timeline = api.search.tweets(q=key_word, lang='en', count=100, max_id=min_id - 1)
        except:
            print("Reached rate limit; sleeping 15 minutes")
            sleep(900)
            next_timeline = api.search.tweets(q=key_word, lang='en', count=100, max_id=min_id - 1)

        ntweets = len(next_timeline['statuses'])
        timeline['statuses'] += next_timeline['statuses']
    return timeline

uber = retrieve_tag('uber')
all_list = [status['text'] for status in uber['statuses']]

names = [status['user']['screen_name'] for status in uber['statuses']]
locations = [status['user']['location'] for status in uber['statuses']]


verified = [status['text'] for status in uber['statuses'] if status['user']['verified'] is True]
names = [status['user']['screen_name'] for status in uber['statuses'] if status['user']['verified'] is True]


text_uber = " ".join([text for text in all_list])
textnltk_uber = nltk.Text(word_tokenize(text_uber))
textnltk_uber.collocations()
textnltk_uber.count("taxi")
textnltk_uber.concordance("taxi")

stopwords = nltk.corpus.stopwords.words("english")

tweet_list_cleaned = [my_tokenize(tweet_clean(tweet)) for tweet in all_list]

tokens_list_cleaned = []
for i in tweet_list_cleaned:
    tokens_list_cleaned+=i

fd = FreqDist(nltk.Text(tokens_list_cleaned))


