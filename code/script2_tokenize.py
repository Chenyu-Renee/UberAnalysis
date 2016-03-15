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
import numpy as np
import pylab as pl


with open("../data/uber.json") as f:
     uber = json.load(f)

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

def tweet_clean(t):
    cleaned_words = [word for word in t.split()
                     if "http" not in word
                     and not word.startswith("@")
                     and not word.startswith(".@")
                     and not word.startswith("#")
                     and word != "RT"]
    return " ".join(cleaned_words)

def tweet_clean(t):
    clean_words = [word for word in t.split()
                     if "http" not in word
                     and not word.startswith("@")
                     and not word.startswith(".@")
                     and word != "RT"]
    cleaned_words = [word.replace('#', '') for word in clean_words]
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

########################################################

# if want to look at top words
dic = {}
for word in fd.keys():
    if fd[word]>=100:
        dic[word]=fd[word]

dic2 = {}
for word in dic.keys():
    if word.isalpha():
        dic2[word]=dic[word]

X = np.arange(len(dic2))
pl.bar(X, dic2.values(), width=0.5)
pl.xticks(X+0.25, dic2.keys(), rotation=70)
ymax = max(dic2.values()) + 100
pl.ylim(0, ymax)
pl.xlim(-0.5, len(dic2))
pl.tight_layout()
pl.savefig('word_freq.png')
pl.show()



