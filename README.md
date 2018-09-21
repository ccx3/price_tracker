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

You can change what information is retrieved. If I remember correctly the display title will alter in accordance.

NOTE: I stuck with black & white output. The red ink refresh rate was slower than I wanted.

## Kit & Resources

    - Raspberry Pi Zero WH (with wifi)
    - inky-phat display that fits over it neatly
    - Pi Zero case so I could stick the whole thing up somewhere.
    - Data supplied by 1forge.com
    - A tidy Verdana font from http://www.fontpalace.com/font-download/Verdana/
    
    
