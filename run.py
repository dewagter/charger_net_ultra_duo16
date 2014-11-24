#!/usr/bin/python

import _thread
import time

import webserver
import myserial
import upload
import settings

import ultraduo
import imaxb6
import charger


c1 = imaxb6.ImaxB6()
c1.channels[0].battery = '20130612-02'

c2 = ultraduo.UltraDuo()

#mycharger = charger.Charger()
#mycharger.name = 'Special Combination'
#mycharger.channels.append(c1.channels[0])
#mycharger.channels.append(c2.channels[0])
#mycharger.channels.append(c2.channels[1])

mycharger = c2
url = settings.MY_PRIVATE_SERVER

#try:
#_thread.start_new_thread( myserial.serial_server, ('COM167', mycharger, ) )
_thread.start_new_thread( myserial.serial_server, ('COM11', mycharger, ) )
_thread.start_new_thread( upload.upload_thread, (url, mycharger))
webserver.start_webserver(mycharger)
#except:
#   print("Error: unable to start threads")
