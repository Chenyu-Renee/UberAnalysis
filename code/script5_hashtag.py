
import json
import numpy as np
import pylab as pl
import string
import re
import us
import pandas as pd
from datetime import *

# create df from location.py file

#load data: It is the location list of all the tweets
with open("../data/uber_all.json") as f:
     uber = json.load(f)

uber['statuses'][0]['entities']['hashtags'][0]['text']

hashtag_list = []
for status in uber['statuses']:
    if len(status['entities']['hashtags']) > 0:
        for i in range(len(status['entities']['hashtags'])):
            hashtag_list.append(status['entities']['hashtags'][i]['text'].lower())

unique_hash = list(set(hashtag_list))

hash_count = {}
for word in unique_hash:
    hash_count[word] = hashtag_list.count(word)

hash_top = {}
for word in hash_count.keys():
    if hash_count[word] >= 300:
        hash_top[word] = hash_count[word]

with open("../data/hash_top.json", "w") as f:
    json.dump(hash_top, f, indent=4, sort_keys=True)

import operator
sorted_hash = sorted(hash_top.items(), key=operator.itemgetter(1), reverse=True)
hash_tuple = [('uber',t[0]) for t in sorted_hash]
node_list = [t[0] for t in sorted_hash]

from networkx import *

hash_tuple = [('uber',t[0]) for t in sorted_hash]
pl.title('Hashtag Network', fontsize=20)
G = Graph()
G.add_edges_from(hash_tuple[1:])
node_list = [t[0] for t in sorted_hash]
weights = np.asarray([t[1] for t in sorted_hash])
draw_spring(G, with_labels=True, nodelist=node_list, edgelist=hash_tuple[1:], width=np.sqrt(weights[1:]/500), node_size=weights/10, node_color='b', alpha=0.3, font_size=16)
pl.savefig('network.png')
pl.show()






