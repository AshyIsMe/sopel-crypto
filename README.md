# sopel-crypto

Cryptocoin lookup and alert script for Sopel IRC bot.

## Install

Copy crypto.sh to your sopel modules directory.
Requires the requests module.

```
sudo pip3 install requests
```

## Testing

```
$ python3 crypto.py btc eth ripple neo
BTC: 19384.0, ETH: 728.547, XRP: 0.75649, NEO: 53.5553

$ python3 crypto.py ethereum in eur
ETH: 613.7706267 eur

$ python3 crypto.py
BTC: 19448.9, ETH: 716.977, BCH: 1811.08, XRP: 0.749863, LTC: 316.18, ADA: 0.396677, MIOTA: 3.54268, DASH: 1163.02, XEM: 0.674681, XMR: 354.758, BTG: 298.455, XLM: 0.262045, EOS: 8.60303, ETC: 35.1259, NEO: 50.6751, TRX: 0.0349273, QTUM: 29.1412, BCC: 441.986, PPT: 48.0646, OMG: 14.2302, ZEC: 490.404, WAVES: 13.386, LSK: 10.7763, BTS: 0.434295, USDT: 1.00368, STRAT: 10.9187, ARDR: 0.980783, HSR: 22.9549, XVG: 0.0618473, MONA: 13.3787, BCN: 0.00385412, NXT: 0.687451, DOGE: 0.00605779, SNT: 0.168539, DCR: 89.8583, ARK: 5.80534, VERI: 275.582, STEEM: 2.2349, SALT: 10.1117, BNB: 5.17638, KMD: 4.68782, SC: 0.0148852, REP: 41.8764, EMC2: 1.93586, PIVX: 7.30306, QASH: 1.07748, GNT: 0.428728, PAY: 3.36858, GBYTE: 538.418, VTC: 8.10942, DGB: 0.0334328, ETN: 0.0610921, DGD: 150.665, AE: 1.22158, XRB: 2.13036, FCT: 32.1186, BAT: 0.279508, SAN: 4.55887, KNC: 2.02611, MAID: 0.565186, CNX: 5.57418, BTM: 0.254124, SYS: 0.47217, POWR: 0.698391, VEN: 0.882794, MANA: 0.103185, BTCD: 181.897, ZRX: 0.467039, WTC: 9.27167, XZC: 62.4527, PPP: 2.68485, RDN: 4.29656, ICN: 2.05744, DATA: 0.303171, GAS: 23.7302, NXS: 3.70524, GNO: 179.939, FUN: 0.0438934, DRGN: 0.738795, MCO: 15.3399, GXS: 4.26064, REQ: 0.265593, GAME: 2.63335, BNT: 3.90723, DENT: 0.0149822, CVC: 0.449972, MTL: 7.73365, NAV: 2.37275, LINK: 0.400877, EDG: 1.70699, SUB: 0.618636, ETP: 3.73163, PPC: 5.53247, BAY: 0.127876, R: 0.697301, PURA: 0.72784, AION: 2.3435, QSP: 0.199521, STORJ: 1.16817, BLOCK: 24.6328

```

## Docker ...

Run the Sopel IRC bot in a Docker container with this module added

### Building

```
docker build -t sopel-crypto .
```

### Running

Create a directory where you want to store the config, log and data files (can
also be a volume container); adjust the name to your likings:

```
mkdir mybot
```

Initialize the bot configuration:

```
docker run --rm -it -v $(pwd)/mybot:/home/sopel/.sopel sopel-crypto sopel -w
```

Create and run the bot:

```
docker run -d --name mybot -v $(pwd)/mybot:/home/sopel/.sopel sopel-crypto
```

If you want it to autostart, add `--restart=always`.

### Running Sopel commands

You can, at any time, run specific Sopel commands. For example:

```
docker run --rm -it -v $(pwd)/mybot:/home/sopel/.sopel sopel-crypto sopel --configure-modules
```
