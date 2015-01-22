#!/usr/bin/env python
import os
import json
import urllib2
from pymendez import auth
from matplotlib.dates import date2num
from datetime import datetime, timedelta

# URL = 'http://api.wunderground.com/api/{key}/history_{date}/q/{state}/{city}.json'
URL = 'http://api.wunderground.com/api/{key}/history_{date}/q/{station}.json'

outfile = os.path.expanduser('~/data/weather.json')
key = auth('weatherunderground', 'key')
# state = 'MD'
# city = 'Baltimore'
station='pws:KMDBALTI35'

date = datetime.now()


def get_weather(d):
    # url = URL.format(key=key, date=d, state=state, city=city)
    url = URL.format(key=key, date=d, station=station)
    print url
    f = urllib2.urlopen(url)
    json_string = f.read()
    parsed_json = json.loads(json_string)
    return parsed_json
    f.close()


try:
    data = json.load(open(outfile, 'r'))
except:
    data = {}

try:
    for i in range(1,30):
        print i
        d = '{0.year}{0.month:02d}{0.day:02d}'.format(date-timedelta(days=i))
        tmp = get_weather(d)
        for obs in tmp['history']['observations']:
            k = d+obs['date']['hour']+obs['date']['min']
            print '  ',datetime.strptime(k, '%Y%m%d%H%M')
            k = date2num(datetime.strptime(k, '%Y%m%d%H%M'))
            
            if k in data:
                if d not in ['20141102']:
                    raise ValueError('Already observed data')
            data[k] = obs
except Exception as e:
    print 'is Done?'
    raise
finally:
    json.dump(data, open(outfile,'w'), indent=2)

