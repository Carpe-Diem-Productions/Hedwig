#!/usr/bin/python3

# Weather forecast for Raspberry Pi w/Adafruit Mini Thermal Printer.
# Retrieves data from DarkSky.net's API, prints current conditions and
# forecasts for next two days.  See timetemp.py for a different
# weather example using nice bitmaps.
# Written by Adafruit Industries.  MIT license.
#
# Required software includes Adafruit_Thermal and PySerial libraries.
# Other libraries used are part of stock Python install.
#
# Resources:
# http://www.adafruit.com/products/597 Mini Thermal Receipt Printer
# http://www.adafruit.com/products/600 Printer starter pack

import calendar
import json
import os
import urllib.error
import urllib.request
from datetime import datetime

from Adafruit_Thermal import *

API_KEY = os.environ["HEDWIG_DARKSKY_API_KEY"]

LAT = "34.420830"
LONG = "-119.698189"


# Dumps one forecast line to the printer
def forecast(idx):
    date = datetime.fromtimestamp(int(data['daily']['data'][idx]['time']))

    day = calendar.day_name[date.weekday()]
    lo = data['daily']['data'][idx]['temperatureMin']
    hi = data['daily']['data'][idx]['temperatureMax']
    cond = data['daily']['data'][idx]['summary']
    printer.print(day + ': low ' + str(lo))
    printer.print(deg)
    printer.print(' high ' + str(hi))
    printer.print(deg)
    printer.println(' ' + cond.replace('\u2013', '-').encode('utf-8'))  # take care of pesky unicode dash


printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)
deg = chr(0xf8)  # Degree symbol on thermal printer

url = "https://api.darksky.net/forecast/" + API_KEY + "/" + LAT + "," + LONG + "?exclude=[alerts,minutely,hourly,flags]&units=ca"
response = urllib.request.urlopen(url)
data = json.loads(response.read())

# Print heading
printer.inverseOn()
printer.print('{:^32}'.format("DarkSky.Net Forecast"))
printer.inverseOff()

# Print current conditions
printer.boldOn()
printer.print('{:^32}'.format('Current conditions:'))
printer.boldOff()

temp = data['currently']['temperature']
cond = data['currently']['summary']
printer.print(temp)
printer.print(deg)
printer.println(' ' + cond)
printer.boldOn()

# Print forecast
printer.print('{:^32}'.format('Forecast:'))
printer.boldOff()
forecast(0)
forecast(1)

printer.feed(3)
