#!/usr/bin/python

import sys
import getopt

import webserver
import seriallog
import upload
import settings
import nfc
import led

def handle_nfc(battery):
  led.toggle(led.ORANGE)
  for charger in settings.chargers:
    if charger.identify(battery):
      return True
  return False



led.init()
led.blink()

# Start all the chargers
for charger in settings.chargers:
  charger.start()

nfc.start(settings.logserver_address, handle_nfc)
upload.start(settings.chargers, settings.logserver_address, settings.logserver_timeout)

#for charger in settings.chargers:
#_thread.start_new_thread( seriallog.serial_server, (p, c) )
#_thread.start_new_thread( webserver.start_webserver, (c, ) )
#_thread.start_new_thread( nfc.nfc_server, () )

while True:
  pass
#  if c.channels[0].newdata > 0:
#    led.toggle(led.RED)
#    c.channels[0].newdata = 0
#  if (nfc.tag.new > 0):
#    led.toggle(led.ORANGE)
#    nfc.tag.new = 0
#    print('Main: ', nfc.tag)
#  print(upload.response)
#  if (upload.response == 200):
#    led.toggle(led.GREEN)
#    upload.response = 0
#  time.sleep(0.25)

