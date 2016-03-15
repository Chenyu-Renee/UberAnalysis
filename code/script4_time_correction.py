
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
with open("../data/uber.json") as f:
     uber = json.load(f)

list_time_zones = {
        'AK': -9,
        'AL': -6,
        'AR': -6,
        'AS': -11,
        'AZ': -7,
        'CA': -8,
        'CO': -7,
        'CT': -5,
        'DC': -8,
        'DE': -5,
        'FL': -5,
        'GA': -5,
        'GU': +10,
        'HI': -10,
        'IA': -6,
        'ID': -7,
        'IL': -6,
        'IN': -5,
        'KS': -6,
        'KY': -5,
        'LA': -6,
        'MA': -5,
        'MD': -5,
        'ME': -5,
        'MI': -5,
        'MN': -6,
        'MO': -6,
        'MP': +10,
        'MS': -6,
        'MT': -7,
        'NA': -5,
        'NC': -5,
        'ND': -6,
        'NE': -6,
        'NH': -5,
        'NJ': -5,
        'NM': -7,
        'NV': -8,
        'NY': -5,
        'OH': -5,
        'OK': -6,
        'OR': -8,
        'PA': -5,
        'PR': -4,
        'RI': -5,
        'SC': -5,
        'SD': -6,
        'TN': -6,
        'TX': -6,
        'UT': -7,
        'VA': -5,
        'VI': -4,
        'VT': -5,
        'WA': -8,
        'WI': -6,
        'WV': -5,
        'WY': -7
}


us_index = df.index.tolist()

dates={}
for ind in us_index:
    date = datetime.strptime(uber['statuses'][ind]['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
    if date >= datetime(2016, 1, 26, 0, 0, 00) and date < datetime(2016, 2, 4, 12, 0, 00):
        dates[ind] = date

locations={}
for ind in us_index:
    locations[ind] = df.ix[ind,'STATE']

time_count = []
for key in dates.keys():
    if type(uber['statuses'][key]['user']['utc_offset']) == int:
        offset = uber['statuses'][key]['user']['utc_offset']/3600
        time_count.append(((dates[key].month - 1) * 31 + dates[key].day - 26) * 24 + dates[key].hour + offset)    
    else:
        time_count.append(((dates[key].month - 1) * 31 + dates[key].day - 26) * 24 + dates[key].hour + list_time_zones[locations[key].upper()])


all(type(time_ct) == int for time_ct in time_count)

hour_count = []
for i in range(7*24):
    hour_count.append(time_count.count(i))

dt = ['']*168
dt[12]='1/21'
dt[36]='1/22'
dt[60]='1/23'
dt[84]='1/24'
dt[108]='1/25'
dt[132]='1/26'
dt[156]='1/27'
X = np.arange(len(hour_count))
pl.bar(X, hour_count, width=0.5)
pl.xticks(X+0.25, dt)
ymax = max(hour_count) + 50
pl.ylim(0, ymax)
pl.xlim(-1, 168.5)
# add shaded rectangles
pl.axvspan(-0.25, 23.75, color='y', alpha=0.3, lw=0)
pl.axvspan(23.75, 47.75, color='r', alpha=0.3, lw=0)
pl.axvspan(47.75, 71.75, color='y', alpha=0.3, lw=0)
pl.axvspan(71.75, 95.75, color='r', alpha=0.3, lw=0)
pl.axvspan(95.75, 119.75, color='y', alpha=0.3, lw=0)
pl.axvspan(119.75, 143.75, color='r', alpha=0.3, lw=0)
pl.axvspan(143.75, 167.75, color='y', alpha=0.3, lw=0)
pl.tight_layout()
pl.savefig('../figure/time_corrected.png', dpi=500)



