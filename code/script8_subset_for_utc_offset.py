
import json
import numpy as np
import pandas as pd
from datetime import *
import pylab as pl

with open("uber_all.json") as f:
     uber = json.load(f)

time_count = []
uber_w_time = []
for status in uber['statuses']:
    if type(status['user']['utc_offset']) == int:
        offset = status['user']['utc_offset']/3600
        date = datetime.strptime(status['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
        local = date.hour + offset
        if local < 0:
            local += 24
        if local >= 24:
            local -= 24
        time_count.append(local)
        uber_w_time.append(status)

## time_count indicate which hour of the day the statuses fall into, min=0, max=23
## NOTE: uber_w_time is equivalent to uber['statuses'] since I only appended uber['statuses'] to uber_w_time

hour_count = []
for i in range(24):
    hour_count.append(time_count.count(i))

dt = ['']*24
dt[0]='12 AM'
dt[3]='3 AM'
dt[6]='6 AM'
dt[9]='9 AM'
dt[12]='12 PM'
dt[15]='3 PM'
dt[18]='6 PM'
dt[21]='9 PM'
X = np.arange(len(hour_count))
pl.bar(X, hour_count, width=0.5)
pl.xticks(X+0.25, dt)
ymax = max(hour_count) + 100
pl.ylim(0, ymax)
pl.xlim(-1, 24.5)
pl.title('#uber Frequency by Hour')
pl.xlabel('Hour of the Day')
pl.ylabel('Number of Tweets')
pl.tight_layout()
pl.show()


