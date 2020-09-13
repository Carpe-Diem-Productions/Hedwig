#!/usr/bin/python
#
#
# Required software includes Adafruit_Thermal and PySerial libraries.
# Other libraries used are part of stock Python install.
#
# Resources:
# http://www.adafruit.com/products/597 Mini Thermal Receipt Printer
# http://www.adafruit.com/products/600 Printer starter pack


from Adafruit_Thermal import *
from newsapi import NewsApiClient
import json
import os

# #######################################################
# PyCharm Remote Debugging
if "HEDWIG_REMOTE_DEBUGGING_HOST" in os.environ and "HEDWIG_REMOTE_DEBUGGING_HOST" in os.environ:
    import pydevd_pycharm

    try:
        pydevd_pycharm.settrace(os.environ["HEDWIG_REMOTE_DEBUGGING_HOST"],
                                port=int(os.environ["HEDWIG_REMOTE_DEBUGGING_PORT"]),
                                stdoutToServer=True, stderrToServer=True)
    except:
        logging.debug("Not connected to PyCharm debugger.")
# #######################################################

api = NewsApiClient(api_key=os.environ["HEDWIG_NEWSAPI_KEY"])

# Get only headlines
def print_headlines():
    headlines = api.get_top_headlines(country='us')

    if headlines['status'] != 'ok':
        printer.setSize('S')
        printer.justify('L')
        printer.println(headlines['status']);
        return False

    num_headlines_to_print = min(1, headlines['totalResults'])

    for i in range(num_headlines_to_print):
        source = headlines['articles'][i]['source']['name']
        title = headlines['articles'][i]['title']
        description = headlines['articles'][i]['description']
        content = headlines['articles'][i]['content']

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


printer = Adafruit_Thermal("/dev/serial0", baudrate=19200, timeout=5)

# Print heading
printer.inverseOn()
printer.print('{:^32}'.format("US Top Headlines"))
printer.inverseOff()

# Print headlines
print_headlines()

printer.feed(3)
