#!/usr/bin/python

import _thread
import time
import sys
import getopt
import RPi.GPIO as GPIO

import webserver
import nfc
import seriallog
import upload
import settings

import ultraduo
import imaxb6
import charger


# Setup LEDs
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.output(7,False)
GPIO.output(11,False)
GPIO.output(15,False)

# Boot sequence
for i in range(0, 5):
  GPIO.output(7,True)
  GPIO.output(11,True)
  GPIO.output(15,True)
  time.sleep(0.2)
  GPIO.output(7,False)
  GPIO.output(11,False)
  GPIO.output(15,False)
  time.sleep(0.2)


#try:
for charger in settings.chargers:
  _thread.start_new_thread( seriallog.serial_server, charger )
  _thread.start_new_thread( upload.upload_server, (charger[1], ) )
  #webserver.start_webserver(charger[1])

_thread.start_new_thread( nfc.nfc_server, () )

while True:
  pass
#except:
#   print("Error: unable to start threads")
