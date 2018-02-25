#!/usr/bin/python


# Something is fucky and the cryptodb file ends up with blank lines in it
# somehow

from __future__ import print_function
from requests import get

import sys
import os
import re
import time
import threading
import collections
import codecs
from datetime import datetime
import random

iteritems = {}
itervalues = {}
iterkeys = {}

if sys.version_info.major >= 3:
    #raw_input = input
    #unicode = str
    iteritems = dict.items
    itervalues = dict.values
    iterkeys = dict.keys
else:
    iteritems = dict.iteritems
    itervalues = dict.itervalues
    iterkeys = dict.iterkeys


def load_database(name):
    data = {}
    if os.path.isfile(name):
        f = codecs.open(name, 'r', encoding='utf-8')
        for line in f:
            symbol, comparison, price, unixtime, original_price, channel, nick = line.split('\t')
            alert = (unixtime, original_price, channel, nick)
            try:
                data[symbol, price, comparison].append(alert)
            except KeyError:
                data[symbol, price, comparison] = [alert]
        f.close()
    return data


def dump_database(name, data):
    f = codecs.open(name, 'w', encoding='utf-8')
    #for (symbol, price, comparison), alerts in sopel.tools.iteritems(data):
    for (symbol, price, comparison), alerts in iteritems(data):
        for (unixtime, original_price, channel, nick) in alerts:
            f.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (symbol, comparison, price, unixtime, original_price, channel, nick))
    f.close()

def seedalert(db, symbol, price):
    for i in range(4):
        alert = (time.time(), random.uniform(8000,20000), "#lowtech", "Ashy")
        #alert = (time.time(), price, "#lowtech", "Ashy")
        #symbol = "BTC"
        #price = random.uniform(8000,20000)
        comparison = ""
        if float(price) > float(alert[1]):
            comparison = 'gte'
        else:
            comparison = 'lte'
        try:
            db[symbol, price, comparison].append(alert)
        except KeyError:
            db[symbol, price, comparison] = [alert]
    return db

fakedata = {}
fakedata = seedalert(fakedata, "BTC", 4000)
fakedata = seedalert(fakedata, "BTC", 8000)
fakedata = seedalert(fakedata, "ETH", 800)
fakedata = seedalert(fakedata, "ETH", 900)
fakedata = seedalert(fakedata, "ETH", 801)
fakedata = seedalert(fakedata, "ETH", 802)
fakedata = seedalert(fakedata, "ETH", 803)
fakedata = seedalert(fakedata, "ETH", 804)

#del bot.alerts_db[symbol, price, comparison]
del fakedata["BTC", 8000, "lte"]
del fakedata["ETH", 801, "lte"]
del fakedata["ETH", 802, "lte"]
del fakedata["ETH", 803, "lte"]

print(fakedata)

dump_database("test.db", fakedata)

