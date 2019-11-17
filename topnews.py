#!/usr/bin/python
#
#
# Required software includes Adafruit_Thermal and PySerial libraries.
# Other libraries used are part of stock Python install.
#
# Resources:
# http://www.adafruit.com/products/597 Mini Thermal Receipt Printer
# http://www.adafruit.com/products/600 Printer starter pack

from __future__ import print_function
from Adafruit_Thermal import *
from newsapi import NewsApiClient
import json

API_KEY = '50a17179539943c7bda01fc4aadfa03a'
api = NewsApiClient(api_key=API_KEY)

def encode_ascii(input_string):
    if input_string is not None:
        return input_string.encode(encoding='ascii', errors='replace')

# Get only headlines
def print_headlines():
    headlines = api.get_top_headlines(country='us')

    if headlines['status'] != 'ok':
        printer.setSize('S')
        printer.justify('L')
        printer.println(headlines['status']);
        return False

    num_headlines_to_print = min(10, headlines['totalResults'])

    for i in xrange(num_headlines_to_print):
        source      = encode_ascii(headlines['articles'][i]['source']['name'])
        title       = encode_ascii(headlines['articles'][i]['title'])
        description = encode_ascii(headlines['articles'][i]['description'])
        content     = encode_ascii(headlines['articles'][i]['content'])

        printer.setSize('S')
        printer.justify('C')
        printer.inverseOn()
        printer.println(source)

        printer.inverseOff()
        printer.setSize('S')
        printer.boldOn()
        printer.underlineOn()
        printer.println(title)

        printer.underlineOff()
        printer.boldOff()
        printer.justify('L')
        printer.setSize('S')
        printer.println(description)

        # printer.println(content)
    return True

printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)

# printer = Adafruit_Thermal()

# Print heading
printer.inverseOn()
printer.print('{:^32}'.format("US Top Headlines"))
printer.inverseOff()

# Print headlines
print_headlines()

printer.feed(3)

