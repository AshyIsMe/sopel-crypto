#!/usr/bin/python

from __future__ import print_function
from requests import get

# AA TODO:
# - alert: .crypto alert btc 50000

# 'https://api.coinmarketcap.com/v1/ticker/?limit=10'
coinmarketcap_all_url = 'https://api.coinmarketcap.com/v1/ticker/'
coinmarketcap_specific_url = 'https://api.coinmarketcap.com/v1/ticker/{}/'
coinmarketcap_convert_url = 'https://api.coinmarketcap.com/v1/ticker/{}/?convert={}'

symbols = [ 'btc', 'eth', 'bch', 'xrp', 'ltc', 'ada', 'miota', 'dash', 'xem',
            'xmr', 'btg', 'eos', 'xlm', 'etc', 'neo', 'trx', 'qtum',
            'bcc', 'ppt', 'omg', 'zec', 'waves', 'lsk', 'bts', 'usdt',
            'strat', 'xvg', 'ardr', 'hsr', 'mona', 'bcn', 'nxt', 'doge',
            'ark', 'veri', 'dcr', 'snt', 'steem', 'salt', 'bnb', 'kmd',
            'sc', 'rep', 'pivx', 'emc2', 'qash', 'gnt', 'gbyte', 'vtc',
            'pay', 'dgb', 'xrb', 'etn', 'dgd', 'ae', 'fct', 'bat', 'san',
            'knc', 'maid', 'ven', 'sys', 'cnx', 'powr', 'btm', 'btcd',
            'zrx', 'wtc', 'mana', 'xzc', 'ppp', 'rdn', 'gas', 'data',
            'icn', 'nxs', 'gno', 'fun', 'mco', 'drgn', 'gxs', 'req',
            'game', 'dent', 'bnt', 'cvc', 'nav', 'mtl', 'link', 'edg',
            'sub', 'ppc', 'qsp', 'etp', 'r', 'pura', 'block', 'storj',
            'aion', 'bay']

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
        return ", ".join(get_crypto_specific(query))

def get_crypto_specific(searchlist=[]):
    coins = get(coinmarketcap_all_url).json()
    if len(searchlist):
        search = list(map(lambda q: q.lower(), searchlist))
        filtered_coins = list(filter(lambda c: (c['name'].lower() in search) or (c['symbol'].lower() in search), coins))
        if len(filtered_coins):
            coins = filtered_coins
    prices = list(map(lambda c: c['symbol'] + ': ' + c['price_usd'], coins))
    return prices

def get_crypto_convert(symbol, currency):
    coins = get(coinmarketcap_convert_url.format(symbol, currency)).json()
    pricekey = 'price_' + currency.lower()
    prices = list(map(lambda c: c['symbol'] + ': ' + c[pricekey] + ' ' + currency, coins))
    return prices

try:
    import sopel.module
except ImportError:
    # Probably running from commandline
    pass
else:
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

if __name__ == "__main__":
    import sys
    crypto = get_crypto(sys.argv[1:])
    print(crypto)
