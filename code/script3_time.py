
import json
import numpy as np
import pylab as pl
import string
import re
import us
import pandas as pd
from datetime import *

#load data: It is the location list of all the tweets
with open("../data/uber.json") as f:
     uber = json.load(f)

# you can change data range
dates={}
for tweet in uber['statuses']:
    date = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
    if date >= datetime(2016, 1, 21, 0, 0, 00) and date < datetime(2016, 1, 28, 0, 0, 00):
        dates[tweet['id']] = date

time_count = []
for key in dates.keys():
    time_count.append((dates[key].day - 21) * 24 + dates[key].hour)

hour_count = []
for i in range(168):
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
ymax = max(hour_count) + 100
pl.ylim(0, ymax)
pl.xlim(-1, 168.5)
pl.tight_layout()
pl.savefig('../figure/hour_no_correction.png')


# time series plot
with open("../data/uber2.json") as f:
     uber2 = json.load(f)

dates={}
for tweet in uber2['statuses']:
    date = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
    dates[tweet['id']] = date

time_count = []
for key in dates.keys():
    time_count.append(((dates[key].month - 1) * 31 + dates[key].day - 29) * 24 + dates[key].hour)

hour_count = []
for i in range(min(time_count), max(time_count)+1):
    hour_count.append(time_count.count(i))

dt = [''] * len(hour_count)  # 136
dt[1]='1/29 \n 12PM'
dt[13]='1/30 \n 0AM'
dt[25]='1/30 \n 12PM'
dt[37]='1/31 \n 0AM'
dt[49]='1/31 \n 12PM'
dt[61]='2/1 \n 0AM'
dt[73]='2/1 \n 12PM'
dt[85]='2/2 \n 0AM'
dt[97]='2/2 \n 12PM'
dt[109]='2/3 \n 0AM'
dt[121]='2/3 \n 12PM'
dt[133]='2/4 \n 0AM'
X = np.arange(len(hour_count))
pl.plot(X, hour_count)
pl.xticks(X, dt)
ymax = max(hour_count) + 50
pl.ylim(0, ymax)
pl.xlim(-1, 137)
pl.tight_layout()
pl.savefig('../figure/hour_line_no_correction.png', dpi=500)


# full 15 days

dates={}
for tweet in uber['statuses']:
    date = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
    if date >= datetime(2016, 1, 21, 0, 0, 00) and date < datetime(2016, 2, 5, 0, 0, 00):
        dates[tweet['id']] = date

time_count = []
for key in dates.keys():
    time_count.append(((dates[key].month - 1) * 31 +dates[key].day - 21) * 24 + dates[key].hour)

hour_count = []
for i in range(15*24):
    hour_count.append(time_count.count(i))

dt = ['']*(15*24)
dt[12]='1/21 \nThu'
dt[36]='1/22 \nFri'
dt[60]='1/23 \nSat'
dt[84]='1/24 \nSun'
dt[108]='1/25 \nMon'
dt[132]='1/26 \nTue'
dt[156]='1/27 \nWed'
dt[180]='1/28 \nThu'
dt[204]='1/29 \nFri'
dt[228]='1/30 \nSat'
dt[252]='1/31 \nSun'
dt[276]='2/1 \nMon'
dt[300]='2/2 \nTue'
dt[324]='2/3 \nWed'
dt[348]='2/4 \nThu'
X = np.arange(len(hour_count))
pl.plot(X, hour_count)
pl.xticks(X, dt)
ymax = max(hour_count) + 50
pl.ylim(0, ymax)
pl.xlim(-1, 360.5)
# add shaded rectangles
pl.axvspan(-0.25, 23.75, color='y', alpha=0.3, lw=0)
pl.axvspan(23.75, 47.75, color='r', alpha=0.3, lw=0)
pl.axvspan(47.75, 71.75, color='y', alpha=0.3, lw=0)
pl.axvspan(71.75, 95.75, color='r', alpha=0.3, lw=0)
pl.axvspan(95.75, 119.75, color='y', alpha=0.3, lw=0)
pl.axvspan(119.75, 143.75, color='r', alpha=0.3, lw=0)
pl.axvspan(143.75, 167.75, color='y', alpha=0.3, lw=0)
pl.axvspan(167.75, 191.75, color='r', alpha=0.3, lw=0)
pl.axvspan(191.75, 215.75, color='y', alpha=0.3, lw=0)
pl.axvspan(215.75, 239.75, color='r', alpha=0.3, lw=0)
pl.axvspan(239.75, 263.75, color='y', alpha=0.3, lw=0)
pl.axvspan(263.75, 287.75, color='r', alpha=0.3, lw=0)
pl.axvspan(287.75, 311.75, color='y', alpha=0.3, lw=0)
pl.axvspan(311.75, 335.75, color='r', alpha=0.3, lw=0)
pl.axvspan(335.75, 359.75, color='y', alpha=0.3, lw=0)
pl.title('Time Series of Tweets Volume Per Hour')
pl.xlabel('UTC Time')
pl.tight_layout()


