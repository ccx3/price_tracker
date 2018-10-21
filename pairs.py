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

#_hicolor = ip.RED
#_hicolor = ip.YELLOW
_hicolor = ip.BLACK

_font_loc = os.path.abspath(os.path.dirname(__file__)) + "/fonts/Verdana.ttf"
_font = ImageFont.truetype(_font_loc, 18)
_font_medium = ImageFont.truetype(_font_loc, 14)
_font_small = ImageFont.truetype(_font_loc, 10)

print_text = part(ip.text, font=_font)
print_small_text = part(ip.text, font=_font_small)

_CENTER_V = ip.WIDTH / 2
_CENTER_Y = ip.HEIGHT / 2
_OZ_TO_G_RATIO = 31.10348

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

def get_pairs():
    "Returns currency-pairs (inc gold price in specified currency)."

    uri = "https://forex.1forge.com/1.0.3/quotes?pairs=XAUUSD,XAUGBP,XAGUSD,XAGGBP&api_key=" + ONEFORGE_SECRET
    res = requests.get(uri)

    json_data = json.loads(res.text) if(res.status_code==200) else {}
    return json_data

pairs = get_pairs()

# always output bottom rectangle
ip.set_colour("red")
ip.set_border(ip.BLACK)
ip.rectangle((0, ip.HEIGHT-20, ip.WIDTH, ip.HEIGHT), fill=ip.BLACK)

if len(pairs) >= 1:

    ip.rectangle((0, 0, ip.WIDTH, 20), fill=ip.BLACK)
    ip.line((0, ip.HEIGHT/2, ip.WIDTH, ip.HEIGHT/2), fill=ip.BLACK) # horizontal
    ip.line((_CENTER_V,0,_CENTER_V,84), fill=ip.BLACK) # vertical

    hdg = "GOLD"
    print_text(_center_text(hdg, (0,0), _CENTER_V, 15), hdg, fill=ip.WHITE)

    hdg = "SILVER"
    print_text(_center_text(hdg, (107,0), _CENTER_V, 15), hdg, fill=ip.WHITE)

    for pair in pairs:
        currency = pair['symbol'].lower()
        currency1, currency2 = (currency[:3],currency[3:])
        price = round(pair['price'], 2)

        if currency == 'xauusd':
            msg_oz = u"${}/oz".format(price)
            msg_g = u"${}/g".format(round(price / _OZ_TO_G_RATIO, 2))
            print_text((5, 21), msg_oz, fill=ip.BLACK, font=_font_medium)
            print_text((5, 38), msg_g, fill=_hicolor, font=_font_small)
        elif  currency == 'xagusd':
            msg_oz = u"${}/oz".format(price)
            msg_g = u"${}/g".format(round(price / _OZ_TO_G_RATIO, 2))
            print_text((110, 21), msg_oz, fill=ip.BLACK, font=_font_medium)
            print_text((110, 38), msg_g, fill=_hicolor, font=_font_small)
        elif  currency == 'xaugbp':
            msg_oz = u"£{}/oz".format(price)
            msg_g = u"£{}/g".format(round(price / _OZ_TO_G_RATIO, 2))
            print_text((5, 53), msg_oz, fill=ip.BLACK, font=_font_medium)
            print_text((5, 70), msg_g, fill=_hicolor, font=_font_small)
        elif  currency == 'xaggbp':
            msg_oz = u"£{}/oz".format(price)
            msg_g = u"£{}/g".format(round(price / _OZ_TO_G_RATIO, 2))
            print_text((110, 53), msg_oz, fill=ip.BLACK, font=_font_medium)
            print_text((110, 70), msg_g, fill=_hicolor, font=_font_small)

    pair_time = datetime.datetime.fromtimestamp(
            int(pairs[0]['timestamp'])
            ).strftime('Updated: %-d %b %Y at %H:%M')
    print_text(
            _center_text(
                pair_time, 
                (40,ip.HEIGHT-13), 
                ip.WIDTH, 20), 
            pair_time, 
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
