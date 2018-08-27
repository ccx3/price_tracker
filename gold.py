#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
import json
import time
import urllib
import sys
from PIL import Image, ImageFont

try:
    import requests
except ImportError:
    exit("This script requires the requests module\nInstall with: sudo pip install requests")

import inkyphat

QUANDL_SECRET=os.environ['QUANDL_SECRET']
if len(QUANDL_SECRET) == 0:
    exit("This script requires the environment veriable QUANDL_SECRET is set with a registered key")

if len(sys.argv) < 2:
    print("""Usage: {} <colour>
       Valid colours: red, yellow, black
""".format(sys.argv[0]))
    sys.exit(0)

colour = sys.argv[1]
inkyphat.set_colour(colour)

inkyphat.set_border(inkyphat.BLACK)


def get_gold_prices():
    uri="https://www.quandl.com/api/v3/datasets/LBMA/GOLD?start_date=2018-08-22&end_date=2018-08-24&api_key=" + QUANDL_SECRET
    res = requests.get(uri)

    if(res.status_code==200):
        json_data = json.loads(res.text)
        return json_data

    return {}

gold_prices = get_gold_prices()

if "data" in gold_prices["dataset"]:
    results = gold_prices["dataset"]["data"]
    for i in results:
        price_date = i[0]
        price = i[4]
        break

else:
    print("Warning, no gold prices found!")

# Load the built-in FredokaOne font
font = ImageFont.truetype(inkyphat.fonts.FredokaOne, 22)

# And now some text
message = "{}GBP/oz".format(price)
w,h = font.getsize(message)
x = (inkyphat.WIDTH / 2) - (w / 2)
y = (inkyphat.HEIGHT / 2) - (h / 2)

inkyphat.text((x, y), message, inkyphat.RED, font=font)

# And show it!
inkyphat.show()
