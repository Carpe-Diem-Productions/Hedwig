#!/usr/bin/python3

# Main script for Adafruit Internet of Things Printer 2.  Monitors button
# for taps and holds, performs periodic actions (Twitter polling by default)
# and daily actions (Sudoku and weather by default).
# Written by Adafruit Industries.  MIT license.
#
# MUST BE RUN AS ROOT (due to GPIO access)
#
# Required software includes Adafruit_Thermal, Python Imaging and PySerial
# libraries. Other libraries used are part of stock Python install.
#
# Resources:
# http://www.adafruit.com/products/597 Mini Thermal Receipt Printer
# http://www.adafruit.com/products/600 Printer starter pack

import logging
import os
import socket
import subprocess

import RPi.GPIO as GPIO
from Adafruit_Thermal import *

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

nextInterval = 0.0  # Time of next recurring operation
dailyFlag = False  # Set after daily trigger occurs
lastId = '1'  # State information passed to/from interval script
printer = Adafruit_Thermal(port="/dev/serial0", baudrate=19200, timeout=5)


# Called once per day (6:30am by default).
# Invokes weather forecast and sudoku-gfx scripts.
def daily():
    # GPIO.output(ledPin, GPIO.HIGH)
    subprocess.call(["python", "timetemp.py"])
    subprocess.call(["python", "forecast.py"])
    subprocess.call(["python", "topnews.py"])
    # subprocess.call(["python", "sudoku-gfx.py"])
    # GPIO.output(ledPin, GPIO.LOW)


# Initialization

# Use Broadcom pin numbers (not Raspberry Pi pin numbers) for GPIO
GPIO.setmode(GPIO.BCM)

# Enable LED and button (w/pull-up on latter)
# GPIO.setup(ledPin, GPIO.OUT)
# GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# LED on while working
# GPIO.output(ledPin, GPIO.HIGH)

# Processor load is heavy at startup; wait a moment to avoid
# stalling during greeting.
time.sleep(3)

# Show IP address (if network is available)
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 0))
    printer.print('My IP address is ' + s.getsockname()[0])
    printer.feed(3)
except:
    printer.boldOn()
    printer.println('Network is unreachable.')
    printer.boldOff()
    printer.print('Connect display and keyboard\n'
                  'for network troubleshooting.')
    printer.feed(3)
    exit(0)

# Print greeting image
printer.printImage(Image.open('gfx/hello.png'), False)
printer.feed(3)

# Poll initial button state and time
# prevButtonState = GPIO.input(buttonPin)
prevTime = time.time()
tapEnable = False
holdEnable = False

# Main loop
while True:

    # Poll current button state and time
    # buttonState = GPIO.input(buttonPin)
    t = time.time()
    '''
    # Has button state changed?
    if buttonState != prevButtonState:
      prevButtonState = buttonState   # Yes, save new state/time
      prevTime        = t
    else:                             # Button state unchanged
      if (t - prevTime) >= holdTime:  # Button held more than 'holdTime'?
        # Yes it has.  Is the hold action as-yet untriggered?
        if holdEnable == True:        # Yep!
          hold()                      # Perform hold action (usu. shutdown)
          holdEnable = False          # 1 shot...don't repeat hold action
          tapEnable  = False          # Don't do tap action on release
      elif (t - prevTime) >= tapTime: # Not holdTime.  tapTime elapsed?
        # Yes.  Debounced press or release...
        if buttonState == True:       # Button released?
          if tapEnable == True:       # Ignore if prior hold()
            tap()                     # Tap triggered (button released)
            tapEnable  = False        # Disable tap and hold
            holdEnable = False
        else:                         # Button pressed
          tapEnable  = True           # Enable tap and hold actions
          holdEnable = True
  
    # LED blinks while idle, for a brief interval every 2 seconds.
    # Pin 18 is PWM-capable and a "sleep throb" would be nice, but
    # the PWM-related library is a hassle for average users to install
    # right now.  Might return to this later when it's more accessible.
    if ((int(t) & 1) == 0) and ((t - int(t)) < 0.15):
      GPIO.output(ledPin, GPIO.HIGH)
    else:
      GPIO.output(ledPin, GPIO.LOW)
    '''
    # Once per day (currently set for 6:30am local time, or when script
    # is first run, if after 6:30am), run forecast and sudoku scripts.
    l = time.localtime()
    if (60 * l.tm_hour + l.tm_min) > (60 * 9 + 10):
        if dailyFlag == False:
            daily()
            dailyFlag = True
            logging.debug("Daily Flag == true")
    else:
        dailyFlag = False  # Reset daily trigger

    # Every 30 seconds, run Twitter scripts.  'lastId' is passed around
    # to preserve state between invocations.  Probably simpler to do an
    # import thing.
    if t > nextInterval:
        nextInterval = t + 30.0
        result = interval()
        # if result is not None:
        #  lastId = result.rstrip('\r\n')