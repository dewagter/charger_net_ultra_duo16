#!/usr/bin/python

import _thread
import webserver
import myserial

import time

# Create two threads as follows
try:
    _thread.start_new_thread( myserial.serial_server, ('COM11', ) )
    webserver.start_webserver()
except:
   print("Error: unable to start thread")
