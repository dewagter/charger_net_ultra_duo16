#!/usr/bin/python

import _thread
import time
import sys
import getopt

import webserver
import seriallog
import upload
import settings
import nfc
import led

import ultraduo
import imaxb6
import skyrc
import charger

led.init()
led.blink()


c = skyrc.SkyRC()

#for charger in settings.chargers:
_thread.start_new_thread( c.run, () )
#_thread.start_new_thread( seriallog.serial_server, (p, c) )
_thread.start_new_thread( upload.upload_server, (c, ) )
_thread.start_new_thread( webserver.start_webserver, (c, ) )
_thread.start_new_thread( nfc.nfc_server, () )

while True:
  if c.channels[0].newdata > 0:
    led.toggle(led.RED)
    c.channels[0].newdata = 0
  if (nfc.tag.new > 0):
    led.toggle(led.ORANGE)
    nfc.tag.new = 0
    print('Main: ', nfc.tag)
  if (upload.response == 200):
    led.toggle(led.GREEN)
    upload.response = 0
  time.sleep(0.25)

