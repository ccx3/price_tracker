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
from functools import partial as part

try:
    import requests
except ImportError:
    exit("This script requires the requests module\nInstall with: sudo pip install requests")

ONEFORGE_SECRET=os.environ['ONEFORGE_SECRET']
if len(ONEFORGE_SECRET) == 0:
    exit("This script requires the environment variable ONEFORGE_SECRET is set with a registered key")

import inkyphat as ip

#_HICOLOR = ip.RED
#_HICOLOR = ip.YELLOW
_HICOLOR = ip.BLACK

_font_loc = os.path.abspath(os.path.dirname(__file__)) + "/fonts/Verdana.ttf"
_font = ImageFont.truetype(_font_loc, 18)
_font_medium = ImageFont.truetype(_font_loc, 14)
_font_small = ImageFont.truetype(_font_loc, 10)

print_text = part(ip.text, font=_font)
print_small_text = part(ip.text, font=_font_small)

_CENTER_V = ip.WIDTH / 2
_CENTER_Y = ip.HEIGHT / 2

# find out if the user specified the units on the command line
_GMOZ = 'gm' # default unit of weight
if len(sys.argv) > 1:
    if sys.argv[1].lower() == 'oz': # The only valid override value
        _GMOZ = 'oz'

_OZ_TO_G_RATIO = 31.10348

def make_metal_msg(pair, price):
    """Make a displayable message.

    Note we assume only gold or silver is sent to this method.
    Note that if _GMOZ == 'gm' we dispolay the price per gram.
    Any other value is interpreted as an instruction to display
    the price per troy ounce.
    """
    if pair.endswith('usd'):
        msg = u"${0:.2f}"
    else:
        msg = u"£{0:.2f}"

    if _GMOZ == 'gm':
        price = round(price / _OZ_TO_G_RATIO, 2)
    else:
        price = round(price, 2)

    msg = msg.format(price)

    return msg

def _center_text(text,
        origin=(0,0),
        width=ip.WIDTH,
        height=ip.HEIGHT,
        font=_font):
    "Calculates the origin for a text-string."

    text = text.strip() # trim off whitespace

    startx, starty = origin
    w,h = font.getsize(text)

    x = (startx + (width/2)) - (w/2)
    y = (starty + (height/2)) - (h/2)
    return (x,y)

def get_prices():
    "Returns currency-pairs (inc gold price in specified currency)."

    uri = "https://forex.1forge.com/1.0.3/quotes?pairs=XAUUSD,XAUGBP,XAGUSD,XAGGBP&api_key=" + ONEFORGE_SECRET
    res = requests.get(uri)

    json_data = json.loads(res.text) if(res.status_code==200) else {}
    return json_data

prices = get_prices()

# always output bottom rectangle
ip.set_colour("red")
ip.set_border(ip.BLACK)
ip.rectangle((0, ip.HEIGHT-20, ip.WIDTH, ip.HEIGHT), fill=ip.BLACK)

if len(prices) >= 1:

    ip.rectangle((0, 0, ip.WIDTH, 20), fill=ip.BLACK)
    ip.line((0, ip.HEIGHT/2, ip.WIDTH, ip.HEIGHT/2), fill=ip.BLACK) # horizontal
    ip.line((_CENTER_V,0,_CENTER_V,84), fill=ip.BLACK) # vertical

    if _GMOZ == 'gm':
        hdg = 'GOLD  (GM)  SILVER'
    else:
        hdg = 'GOLD  (OZ)  SILVER'
    #print_text(_center_text(hdg, (0,0), _CENTER_V, 15), hdg, fill=ip.WHITE)
    print_text(_center_text(hdg, (0,0), height=15), hdg, fill=ip.WHITE)

    for price_data in prices:
        currency = price_data['symbol'].lower()
        msg = make_metal_msg(currency, price_data['price'])

        if currency == 'xauusd':
            print_text((5,25), msg, fill=_HICOLOR)
        elif  currency == 'xagusd':
            print_text((110, 25), msg, fill=_HICOLOR)
        elif  currency == 'xaugbp':
            print_text((5,55), msg, fill=_HICOLOR)
        elif  currency == 'xaggbp':
            print_text((110,55), msg, fill=_HICOLOR)

    price_data_time = datetime.datetime.fromtimestamp(
            int(prices[0]['timestamp'])
            ).strftime('Updated: %-d %b %Y at %H:%M')
    print_text(
            _center_text(
                price_data_time, 
                (40,ip.HEIGHT-13), 
                ip.WIDTH, 20), 
            price_data_time, 
            fill=ip.WHITE, 
            font=_font_small)
    # And show it!
    ip.show()

else:
    no_pairs = "NO PAIRS FOUND!"
    print_small_text(
            _center_text(
                no_pairs, 
                (40,ip.HEIGHT-13), 
                ip.WIDTH, 20), 
            no_pairs, 
            fill=ip.WHITE)
    # And show it!
    ip.show()
    sys.exit()
