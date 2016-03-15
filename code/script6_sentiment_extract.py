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


with open("../data/uber_all.json") as f:
     uber = json.load(f)

uber_w_time = []
for status in uber['statuses']:
    if type(status['user']['utc_offset']) == int:
        uber_w_time.append(status)


neg_words = ['bad', 'terrible', 'crap', 'useless', 'hate', ':(', ':-(', 'late', 'angry',  
            'wait', 'expensive', 'drunk', 'protest', 'strike', 'attack', 'traffic', 
            'frustrated', 'disgusting', 'fight', 'disappointed', 'surge', 'violent', 'logo']

def detect_neg(text):
    return any([neg in text for neg in neg_words])

neg_index = []
for i in range(len(uber_w_time)):
    if detect_neg(uber_w_time[i]['text'].lower()):
        neg_index.append(i)

uber_neg = [uber_w_time[i] for i in neg_index]

def utc_offset(status):
    date = datetime.strptime(status['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
    offset = status['user']['utc_offset']/3600
    total_hour = ((date.month - 1) * 31 + date.day - 1) * 24 + date.hour + offset
    month = int(np.floor(total_hour/(31*24))) + 1
    day = int(np.floor((total_hour%(31*24))/24)) + 1
    hour = int((total_hour%(31*24))%24)
    return datetime(date.year, month, day, hour, date.minute, date.second)

def utc_offset(status):
    date = datetime.strptime(status['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
    return date


df1=pd.DataFrame()
date1=pd.Series([utc_offset(status).strftime('%Y-%m-%d %H:00') for status in uber_neg 
         if utc_offset(status) >= datetime(2016, 1, 25, 0, 0, 00) and utc_offset(status) <= datetime(2016, 2, 1, 0, 0, 00)])
df1['Date']=date1
df1['Negative']=1
df11=df1.groupby(df1['Date'], as_index=False).sum()

df2=pd.DataFrame()
date2=pd.Series([utc_offset(status).strftime('%Y-%m-%d %H:00') for status in uber_w_time
         if utc_offset(status) >= datetime(2016, 1, 25, 0, 0, 00) and utc_offset(status) <= datetime(2016, 2, 1, 0, 0, 00)])
df2['Date']=date2
df2['Total']=1
df22=df2.groupby(df2['Date'], as_index=False).sum()

df = pd.merge(df11, df22, on='Date', how='outer')
df = df.sort(['Date'])
df = df.fillna(0)

df.to_csv('total_neg_tweets.csv')



