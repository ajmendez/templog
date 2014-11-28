#!/usr/bin/env python

import os
import pylab
import numpy as np
from dateutil import parser
from pysurvey.plot import setup


FILENAME = os.path.expanduser('~/.temperature.neon.log')


def read_temps(filename=FILENAME):
    out = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            items = line.split(':')
            out.append(dict(date=parser.parse(items[1]),
                            temperature=float(items[2])/1000.0))
    return out
    

def plot_temp():
    data = read_temps()
    dates, values = zip(*[(d['date'], d['temperature'])
                          for d in data])
    
    setup(figsize=(12,12))
    
    setup(subplt=(2,2,1), xlabel='Date', ylabel='Temp [c]')
    pylab.plot(dates, values)
    dateticks('%Y.%m.%h')
    
    pylab.show()



if __name__ == '__main__':
    plot_temp()