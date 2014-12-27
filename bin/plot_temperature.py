#!/usr/bin/env python

import os
import sys
import json
import pylab
import numpy as np
import matplotlib.ticker
from dateutil import parser
from scipy import interpolate
from matplotlib.dates import date2num
from datetime import timedelta, datetime
from pysurvey.plot import setup, dateticks, minmax, hcolorbar


FILENAME = os.path.expanduser('~/.temperature.neon.log')
SEP = ' : '

FILENAME = os.path.expanduser('~/.temperature.xenon.log')
SEP = ' | '


def read_temps(filename=FILENAME):
    out = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            items = line.split(SEP)
            out.append(dict(date=parser.parse(items[1]),
                            temperature=float(items[2])/1000.0))
    return out


def setupplot(secondax=False, **kwargs):
    ytickv = np.linspace(20,75,6)
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


def get_continuum(dates, x, y, delta=2):
    out = []
    t = timedelta(hours=delta)
    for d in dates:
        ii = np.where( (date2num(x) >  date2num(d-t) ) &
                       (date2num(x) <= date2num(d+t) ) )[0]
        if len(ii) <= 20:
            out.append(-1)
        else:
            out.append( np.mean(y[ii]) )
    
    
    t = date2num(dates)
    n = np.min(t)
    tmp = np.array(out)
    ii = np.where(tmp > 0)
    f = interpolate.UnivariateSpline(date2num(dates[ii])-n,tmp[ii], s=4)
    return f(t-n)
    
    
    # print out
    # raise ValueError()
    tmp = np.array(out)
    ii = np.where(tmp > 0)
    
    f = interpolate.interp1d(date2num(dates[ii]), tmp[ii], bounds_error=False)
    return f(date2num(dates))
    
def plot_weather(mindate):
    weatherfile = os.path.expanduser('~/data/weather.json')
    wf = json.load(open(weatherfile,'r'))
    keys = sorted(wf.keys())
    x = np.array(map(np.float, keys))
    y = np.array(map(np.float, [wf[k]['tempm'] for k in keys]))+50
    ii = np.where(x > mindate)
    pylab.plot(x[ii],y[ii])


def plot_temp():
    data = read_temps()
    dates, values = map(np.array, zip(*[(d['date'], d['temperature'])
                                        for d in data]))
    tmp = (date2num(dates) % 1.0)*24.0
    ii = np.where((tmp > 0) & (tmp < 8))[0]
    continuum = get_continuum(dates, dates[ii], values[ii])
    
    
    setup(figsize=(12,6))
    
    setupplot(subplt=(1,2,1), autoticks=True, xlabel='Date',)
    pylab.plot(dates, values)
    pylab.plot(dates[ii], values[ii], '.r')
    pylab.plot(dates, continuum, '.k')
    plot_weather(np.min(date2num(dates)))
    # pylab.plot(dates, values-continuum+38, '.r')
    dateticks('%Y.%m.%d')
    
    
    setupplot(subplt=(2,2,2), autoticks=False, xlabel='Hour of Day')
    pylab.plot(tmp, values, '.')
    setupplot(subplt=(2,2,2), ylabel='', secondax=True)
    
    setupplot(subplt=(2,2,4), autoticks=False, xlabel='Hour of Day')
    sc = pylab.scatter(tmp, values-continuum+38, 
                       c=date2num(dates)-np.min(date2num(dates)), s=15,
                       marker='.', edgecolor='none',
                       label='Days since Start')
    
    setupplot(subplt=(2,2,4), ylabel='', secondax=True)
    hcolorbar(sc, axes=[0.75, 0.42, 0.1, 0.01])
    
    pylab.tight_layout()
    pylab.show()



if __name__ == '__main__':
    from pysurvey import util
    util.setup_stop()
    plot_temp()