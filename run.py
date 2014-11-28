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
import charger

led.init()
led.blink()


c = ultraduo.UltraDuo()
p = 'COM11'

#for charger in settings.chargers:
_thread.start_new_thread( seriallog.serial_server, (p, c) )
_thread.start_new_thread( upload.upload_server, (c, ) )
webserver.start_webserver(c)
_thread.start_new_thread( nfc.nfc_server, () )

while True:
  if c.channel[0].newdata > 0:
    led.toggle(led.RED)
    c.channel[0].newdata = 0
  if nfc.tag.new > 1:
    led.toggle(led.ORANGE)
    nfc.tag.new = 0

