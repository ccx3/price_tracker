# price_tracker

Simple Raspberry Pi project to display current Gold & Silver prices on an
inky-phat display.
    
## Overview

You will need to sign up with some online resource and get an API key to use.
I used 1forge.com. A free account gets you 1000 calls / day which is more than enough with the polling once every
10 minutes that I used here.

I keep the key in an environment variable so that it doesn't appear anywhere in my uploaded code. The environment
variable is ONEFORGE_SECRET.

I retrieve the current price of gold and silver in USD and GBP and display those 4 pieces of information in a little
table. The last retrieval date and time is shown at the bottom of the screen.

You can change what currency pairs are retrieved. 
Note, though, that if you do. you will need to change the column-headings manually to what you want.

NOTE: I stuck with black & white output. The red ink refresh rate was slower than I wanted.

## Kit & Resources

You need an API key from 1forge.com. The font used is from 
http://www.fontpalace.com/font-download/Verdana/

    - Raspberry Pi Zero WH (with wifi)
    - inky-phat display that fits over it neatly
    - Pi Zero case so the Pi+display can be stuck to a vertical surface somewhere.
    
See [photo](./price_tracker.jpg) for how the prices are displayed.
