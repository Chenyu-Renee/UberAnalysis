
# coding: utf-8

# In[1]:

from __future__ import division, print_function
import twitter
import json
from operator import itemgetter
import string
import nltk
from nltk import word_tokenize, FreqDist
import pandas as pd
from time import sleep


# In[2]:

CONSUMER_KEY       = "GzSVL0oiRgswNuy1ahsLDQ9wP"
CONSUMER_SECRET    = "vLysutoROVjJw0mIiax17T4Tk9kVZfgcMxm3X70hi3a6NFG1Q7"
OAUTH_TOKEN        = "164963267-sPOdlztIj7PUH6NlVz8YeEwu4sTD7JCNM721UtLI"
OAUTH_TOKEN_SECRET = "ZMpMRzl4FOb5K2ywtguIk9oJnhKMgBZuha2jUnGdUuWRX"


# In[3]:

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)


# In[4]:

api = twitter.Twitter(auth=auth)


# In[7]:

with open("uber_all.json") as f:
    uber = json.load(f)


# In[10]:

all_list = [status['text'] for status in uber['statuses']]


# In[11]:

len(all_list)


# In[12]:

def tweet_clean(t):
    cleaned_words = [word for word in t.split()
                     if "http" not in word
                     and not word.startswith("@")
                     and not word.startswith(".@")
                     and not word.startswith("#")
                     and word != "RT"]
    return " ".join(cleaned_words)


# In[13]:

stopwords = nltk.corpus.stopwords.words("english")


# In[14]:

def all_punct(x):
    return all([char in string.punctuation for char in x])


# In[15]:

def my_tokenize(text):
    init_words = word_tokenize(text)
    return [w.lower() for w in init_words if
            not all_punct(w) and w.lower() not in stopwords]


# In[16]:

tweet_list_cleaned = [my_tokenize(tweet_clean(tweet)) for tweet in all_list]


# In[18]:

tokens_list_cleaned = []
for i in tweet_list_cleaned:
    tokens_list_cleaned+=i


# In[21]:

fd = FreqDist(nltk.Text(tokens_list_cleaned))


# In[22]:

fd


# In[42]:

logo, bad = [], []
for x in all_list:
    (bad, logo)[x.__contains__("logo")].append(x)


# In[43]:

len(logo)


# In[44]:

tweet_list_logo = [my_tokenize(tweet_clean(tweet)) for tweet in logo]


# In[45]:

tokens_list_logo = []
for i in tweet_list_logo:
    tokens_list_logo+=i


# In[47]:

fd = FreqDist(nltk.Text(tokens_list_logo))


# In[50]:

fd


# In[51]:

with open('logowords.txt','w') as f:
  f.write('\n'.join(tokens_list_logo))


# In[ ]:



