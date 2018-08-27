#!/usr/bin/env python
# -*- coding: utf-8 -*-

# data returned:
# [
#   {"symbol":"XAUGBP","bid":938.0909,"ask":938.9925,"price":938.5417,"timestamp":1535272025},
#   {"symbol":"GBPUSD","bid":1.28476,"ask":1.28511,"price":1.28493,"timestamp":1535272025}
# ]
#
# Note that if an invalid pair is requested, then that item will be omitted
# silently from the results.
#
import os
import datetime
import json
import sys
from PIL import Image, ImageFont

try:
    import requests
except ImportError:
    exit("This script requires the requests module\nInstall with: sudo pip install requests")

ONEFORGE_SECRET=os.environ['ONEFORGE_SECRET']
if len(ONEFORGE_SECRET) == 0:
    exit("This script requires the environment veriable ONEFORGE_SECRET is set with a registered key")

import inkyphat

def get_pairs():
    "Returns currency-pairs (inc gold price in specified currency)."

    uri = "https://forex.1forge.com/1.0.3/quotes?pairs=XAUGBP,GBPUSD&api_key=" + ONEFORGE_SECRET
    res = requests.get(uri)

    json_data = json.loads(res.text) if(res.status_code==200) else {}
    return json_data

pairs = get_pairs()

if len(pairs) >= 1:

    inkyphat.set_colour("red")
    inkyphat.set_border(inkyphat.BLACK)

    font = ImageFont.truetype(inkyphat.fonts.FredokaOne, 18)

    pair_time = datetime.datetime.fromtimestamp(
            int(pairs[0]['timestamp'])
            ).strftime('%Y-%m-%d %H:%M:%S')
    inkyphat.text((5, 0), pair_time, inkyphat.RED, font=font)

    pos = 40
    for pair in pairs:
        currency1, currency2 = (pair['symbol'][:3].lower(),
                pair['symbol'][3:].lower())
        if currency1 == 'xau':
            message = "gold: {} {}/oz".format(pair['price'], currency2)
        else:
            message = "{}/{}: {}".format(currency1, currency2, pair['price'])
        inkyphat.text((5, pos), message, inkyphat.RED, font=font)
        pos += 20

    # And show it!
    inkyphat.show()

else:
    print("Warning, no pairs found!")
    sys.exit()
