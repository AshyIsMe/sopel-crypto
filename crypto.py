#!/usr/bin/python


from __future__ import print_function
from requests import get

# 'https://api.coinmarketcap.com/v1/ticker/?limit=10'
coinmarketcap_all_url = 'https://api.coinmarketcap.com/v1/ticker/'
coinmarketcap_specific_url = 'https://api.coinmarketcap.com/v1/ticker/{}/'
coinmarketcap_convert_url = 'https://api.coinmarketcap.com/v1/ticker/{}/?convert={}'

def get_crypto_all(query):
    coins = get(coinmarketcap_all_url).json()
    return coins

def get_crypto_specific(query):
    return 42

def get_crypto_convert(query):
    return 42

try:
    import sopel.module
except ImportError:
    # Probably running from commandline
    pass
else:
    @sopel.module.commands('crypto')
    @sopel.module.example('.crypto btc')
    def f_crypto(bot, trigger):
        """Look up crypto prices with coinmarketcap"""
        query = trigger.group(2).strip().lower()
        coins = get_crypto_all(query)
        if len(coins):
            bot.say(", ".join(coins))
        else:
            bot.say("Couldn't query coinmarketcap with: " + query)
        return sopel.module.NOLIMIT

if __name__ == "__main__":
    import sys
    query = ''
    if len(sys.argv) > 1:
       query = sys.argv[1]
    crypto = get_crypto_all(query)
    print(crypto)
