#!/usr/bin/python

import time
import serial
import threading
import _thread

def serial_server(port, handle_data, baudrate, readsize, logging):
    if logging:
        timestr = time.strftime("%Y%m%d-%H%M%S")
        f = open('logs/raw_' + timestr + '.bin', 'w+b')

    lock = threading.Lock()
    try:
        ser=serial.Serial(port, baudrate, timeout=0.05)
        line = ''
        while (1):
            s = ser.read(readsize)

            if logging:
                f.write(s)
            
            lock.acquire()
            try:
                handle_data(s)
            finally:
                lock.release()
                

    except KeyboardInterrupt:
        print ('^C received, closing serial port')
        ser.close()
        if logging:
            f.close()

def start(port, handle_data, baudrate = 9600, readsize = 1024, logging = True):
    _thread.start_new_thread(serial_server, (port, handle_data, baudrate, readsize, logging))

if __name__ == '__main__':
    start('/dev/tyUSB0', print)
