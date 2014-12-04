#!/usr/bin/env python

import os
import sys
import pylab
import numpy as np
from dateutil import parser
from pysurvey.plot import setup, dateticks, minmax
from matplotlib.dates import date2num
import matplotlib.ticker
from datetime import timedelta, datetime

FILENAME = os.path.expanduser('~/.temperature.neon.log')


def read_temps(filename=FILENAME):
    out = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            items = line.split(' : ')
            out.append(dict(date=parser.parse(items[1]),
                            temperature=float(items[2])/1000.0))
    return out


def setupplot(secondax=False, **kwargs):
    ytickv = np.linspace(30,75,6)
    yticknames = map('{:0.0f}'.format, ytickv)
    tmp = dict(
        ylabel='Temperature [c]',
        yr=minmax(ytickv), ytickv=ytickv,
        yticknames=yticknames,
    )
    tmp.update(kwargs)
    ax = setup(**tmp)
    
    if secondax:
        subplt = kwargs.get('subplt',None)
        f = lambda x: '{:0.0f}'.format(1.8*x + 32.0)
        yticknames = map(f, ytickv)
        ax2 = ax.twinx()
        ax2.set_ylabel(r"Temperature [F]")
        ax2.set_ylim(minmax(ytickv))
        ax2.yaxis.set_major_locator(matplotlib.ticker.FixedLocator(ytickv))
        ax2.yaxis.set_major_formatter(matplotlib.ticker.FixedFormatter(yticknames))
        pylab.sca(ax)
        
        # setup(ax=ax.twinx(),
        #       subplt=subplt,
        #       ylabel='Temperature [F]',
        #       yr=minmax(ytickv), ytickv=ytickv, yticknames=yticknames)
        
    
    return ax


def get_continuum(dates, x, y, delta=10):
    out = []
    t = timedelta(hours=delta)
    for d in dates:
        ii = np.where( (date2num(x) >  date2num(d-t) ) &
                       (date2num(x) <= date2num(d+t) ) )[0]
        if len(ii) <= 0:
            out.append(-1)
        else:
            out.append( np.mean(y[ii]) )
    
    # print out
    # raise ValueError()
    return np.array(out)
    


def plot_temp():
    data = read_temps()
    dates, values = map(np.array, zip(*[(d['date'], d['temperature'])
                                        for d in data]))
    tmp = (date2num(dates) % 1.0)*24.0
    ii = np.where((tmp > 0) & (tmp < 6))[0]
    continuum = get_continuum(dates, dates[ii], values[ii])
    
    
    setup(figsize=(12,6))
    
    setupplot(subplt=(1,2,1), autoticks=True, xlabel='Date',)
    pylab.plot(dates, values)
    pylab.plot(dates[ii], values[ii], '.r')
    pylab.plot(dates, continuum, '.k')
    # pylab.plot(dates, values-continuum+38, '.r')
    dateticks('%Y.%m.%d')
    
    
    setupplot(subplt=(1,2,2), autoticks=True, xlabel='Hour of Day')
    pylab.plot(tmp, values, '.')
    pylab.plot(tmp, values-continuum+38, '.')
    setupplot(subplt=(1,2,2), ylabel='', secondax=True)
    
    
    
    pylab.show()



if __name__ == '__main__':
    from pysurvey import util
    util.setup_stop()
    plot_temp()