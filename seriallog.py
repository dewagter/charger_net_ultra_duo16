#!/usr/bin/python

import time
import serial
import charger
import threading


def serial_server(port, mycharger):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    p = open('logs/logfile_' + timestr + '.csv', 'w')
    f = open('logs/raw_' + timestr + '.bin', 'w+b')
    p.write(charger.Channel().header()+ " " + charger.Channel().header()+"\n")
    lock = threading.Lock()
    try:
        ser=serial.Serial(port, mycharger.baudrate, timeout=0.05)
        line = ''
        while (1):
            s = ser.read(mycharger.readsize)
            f.write(s)
            
            log = ''
            updated = 0
            lock.acquire()
            try:
                updated = mycharger.process_serial_data(s)
                if updated == 1:
                    for c in mycharger.channels:
                        log += c.print() + " "
                    log += "\n"
            finally:
                lock.release()

            if updated == 1:
                p.write(log)
                

    except KeyboardInterrupt:
        print ('^C received, closing serial port')
        ser.close()
        p.close()
        f.close()
        
import imaxb6
import ultraduo

if __name__ == '__main__':
    #serial_server('COM167', imaxb6.ImaxB6())
    serial_server('COM11', ultraduo.UltraDuo())


