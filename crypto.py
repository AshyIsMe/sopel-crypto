#!/usr/bin/python

from __future__ import print_function
from requests import get

import os
import re
import time
import threading
import collections
import codecs
from datetime import datetime

# 'https://api.coinmarketcap.com/v1/ticker/?limit=10'
coinmarketcap_all_url = 'https://api.coinmarketcap.com/v1/ticker/'
coinmarketcap_specific_url = 'https://api.coinmarketcap.com/v1/ticker/{}/'
coinmarketcap_convert_url = 'https://api.coinmarketcap.com/v1/ticker/{}/?convert={}'

# These arrays might come in handy for something...
symbols = [ 'BTC', 'ETH', 'BCH', 'XRP', 'LTC', 'ADA', 'MIOTA', 'DASH', 'XEM',
            'XMR', 'BTG', 'EOS', 'XLM', 'ETC', 'NEO', 'TRX', 'QTUM',
            'BCC', 'PPT', 'OMG', 'ZEC', 'WAVES', 'LSK', 'BTS', 'USDT',
            'STRAT', 'XVG', 'ARDR', 'HSR', 'MONA', 'BCN', 'NXT', 'DOGE',
            'ARK', 'VERI', 'DCR', 'SNT', 'STEEM', 'SALT', 'BNB', 'KMD',
            'SC', 'REP', 'PIVX', 'EMC2', 'QASH', 'GNT', 'GBYTE', 'VTC',
            'PAY', 'DGB', 'XRB', 'ETN', 'DGD', 'AE', 'FCT', 'BAT', 'SAN',
            'KNC', 'MAID', 'VEN', 'SYS', 'CNX', 'POWR', 'BTM', 'BTCD',
            'ZRX', 'WTC', 'MANA', 'XZC', 'PPP', 'RDN', 'GAS', 'DATA',
            'ICN', 'NXS', 'GNO', 'FUN', 'MCO', 'DRGN', 'GXS', 'REQ',
            'GAME', 'DENT', 'BNT', 'CVC', 'NAV', 'MTL', 'LINK', 'EDG',
            'SUB', 'PPC', 'QSP', 'ETP', 'R', 'PURA', 'BLOCK', 'STORJ',
            'AION', 'BAY']

names = ['bitcoin', 'ethereum', 'bitcoin cash', 'ripple', 'litecoin',
        'cardano', 'iota', 'dash', 'nem', 'monero', 'bitcoin gold',
        'eos', 'stellar', 'ethereum classic', 'neo', 'tron', 'qtum',
        'bitconnect', 'populous', 'omisego', 'zcash', 'waves', 'lisk',
        'bitshares', 'tether', 'stratis', 'verge', 'ardor', 'hshare',
        'monacoin', 'bytecoin', 'nxt', 'dogecoin', 'ark', 'veritaseum',
        'decred', 'status', 'steem', 'salt', 'binance coin', 'komodo',
        'siacoin', 'augur', 'pivx', 'einsteinium', 'qash', 'golem',
        'byteball bytes', 'vertcoin', 'tenx', 'digibyte', 'raiblocks',
        'electroneum', 'digixdao', 'aeternity', 'factom', 'basic attention token',
        'santiment network token', 'kyber network', 'maidsafecoin',
        'vechain', 'syscoin', 'cryptonex', 'power ledger', 'bytom',
        'bitcoindark', '0x', 'walton', 'decentraland', 'zcoin', 'paypie',
        'raiden network token', 'gas', 'streamr datacoin', 'iconomi',
        'nexus', 'gnosis', 'funfair', 'monaco', 'dragonchain',
        'gxshares', 'request network', 'gamecredits', 'dent', 'bancor',
        'civic', 'nav coin', 'metal', 'chainlink', 'edgeless',
        'substratum', 'peercoin', 'quantstamp', 'metaverse etp', 'revain',
        'pura', 'blocknet', 'storj', 'aion', 'bitbay']

def get_crypto(query=[]):
    if len(query) == 3 and query[1] == 'in':
        return ", ".join(get_crypto_convert(query[0], query[2]))
    else:
        return price_line(get_crypto_specific(query))

def get_crypto_specific(searchlist=[]):
    coins = get(coinmarketcap_all_url).json()
    if len(searchlist):
        search = list(map(lambda q: q.lower(), searchlist))
        filtered_coins = list(filter(lambda c: (c['name'].lower() in search) or (c['symbol'].lower() in search), coins))
        if len(filtered_coins):
            coins = filtered_coins
    return coins

def get_crypto_convert(symbol, currency):
    coins = get(coinmarketcap_convert_url.format(symbol, currency)).json()
    pricekey = 'price_' + currency.lower()
    prices = list(map(lambda c: c['symbol'] + ': ' + c[pricekey] + ' ' + currency, coins))
    return prices

def price_line(coins, currency="usd"):
    prices = list(map(lambda c: c['symbol'] + ': ' + c['price_'+currency], coins))
    return ", ".join(prices)

try:
    import sopel.module
except ImportError:
    # Probably running from commandline
    pass
else:
    def filename(self):
        name = self.nick + '-' + self.config.core.host + '.cryptoalerts.db'
        return os.path.join(self.config.core.homedir, name)

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
        for (symbol, price, comparison), alerts in sopel.tools.iteritems(data):
            for (unixtime, original_price, channel, nick) in alerts:
                f.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (symbol, comparison, price, unixtime, original_price, channel, nick))
        f.close()

    def setup(bot):
        bot.alerts_fn = filename(bot)
        bot.alerts_db = load_database(bot.alerts_fn)

        def cmp(op, a, b):
            if op == 'gte':
                return a >= b
            elif op == 'lte':
                return a <= b
            elif op == 'gt':
                return a > b
            elif op == 'lt':
                return a < b

        def monitor(bot):
            time.sleep(5)
            print(time.time(), "monitor() starting")
            while True:
                print(time.time(), "monitor() len(bot.alerts_db): ", len(bot.alerts_db))
                if len(bot.alerts_db):
                    coins = {c['symbol']: c for c in get(coinmarketcap_all_url).json()}
                alerted = False
                for (symbol, price, comparison) in list(bot.alerts_db):
                    if cmp(comparison, float(coins[symbol.upper()]['price_usd']), float(price)):
                        for (unixtime, original_price, channel, nick) in bot.alerts_db[symbol, price, comparison]:
                            if comparison == 'gte':
                                message = "{} {} USD. Up from {} USD on {}."
                            elif comparison == 'lte':
                                message = "{} {} USD. Down from {} USD on {}."
                            date = time.asctime(time.localtime(float(unixtime)))
                            message = message.format(symbol, coins[symbol.upper()]['price_usd'], original_price, date)
                            bot.msg(channel, nick + ': ' + message)
                        del bot.alerts_db[symbol, price, comparison]
                        alerted = True

                if alerted:
                    dump_database(bot.alerts_fn, bot.alerts_db)

                #time.sleep(60 * 10)
                time.sleep(60 * 5)

        targs = (bot,)
        t = threading.Thread(target=monitor, args=targs)
        t.start()

    @sopel.module.commands('crypto')
    @sopel.module.example('.crypto btc eth neo')
    def f_crypto(bot, trigger):
        """Look up crypto prices with coinmarketcap"""
        query = (trigger.group(2) or "").strip().lower().split(" ")
        crypto = get_crypto(query)
        if len(crypto):
            bot.say(crypto)
        else:
            bot.say("Couldn't query coinmarketcap with: " + query)
        return sopel.module.NOLIMIT

    @sopel.module.commands('alert')
    @sopel.module.example('.alert btc 50000')
    def f_crypto_alert(bot, trigger):
        if not trigger.group(2):
            bot.say("No arguments given for alert command.")
            return NOLIMIT
        regex = re.compile(r'([a-zA-Z]*)\s*(\d+\.?\d*)')
        match = regex.match(trigger.group(2).upper())
        if not match:
            bot.reply("Sorry, but I didn't understand your input.")
            return NOLIMIT
        symbol, price = match.groups()
        if symbol.upper() in symbols or symbol.lower() in names:
            create_alert(bot, trigger, symbol, price)
        else:
            bot.reply("Symbol not found: {}".format(symbol))

    def create_alert(bot, trigger, symbol, price):
        coin = get_crypto_specific([symbol])[0]

        if float(price) > float(coin['price_usd']):
            comparison = 'gte'
        else:
            comparison = 'lte'
        alert = (time.time(), coin['price_usd'], trigger.sender, trigger.nick)
        try:
            bot.alerts_db[symbol, price, comparison].append(alert)
        except KeyError:
            bot.alerts_db[symbol, price, comparison] = [alert]
        dump_database(bot.alerts_fn, bot.alerts_db)

        bot.reply("Okay, will alert when {} is {} {} USD"
                    .format(symbol, comparison, price))


if __name__ == "__main__":
    import sys
    crypto = get_crypto(sys.argv[1:])
    print(crypto)
