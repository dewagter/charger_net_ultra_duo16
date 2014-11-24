#!/usr/bin/python

import _thread
import webserver
import myserial
import upload
import time

import ultraduo
import imaxb6


mycharger = imaxb6.ImaxB6()
mycharger.channels[0].battery = '20130612-02'

try:
    _thread.start_new_thread( myserial.serial_server, ('COM167', mycharger, ) )
#    _thread.start_new_thread( upload.upload_thread, (mycharger))
    webserver.start_webserver(mycharger)
except:
   print("Error: unable to start threads")
