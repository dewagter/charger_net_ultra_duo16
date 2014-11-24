import time
import serial
import charger
import threading


def serial_server(port, mycharger):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    p = open('logfile_' + timestr + '.csv', 'w')
    f = open('raw_' + timestr + '.hex', 'w')
    p.write(charger.Channel().header()+ " " + charger.Channel().header()+"\n")
    lock = threading.Lock()
    try:
        ser=serial.Serial(port, mycharger.baudrate, timeout=0.05)
        line = ''
        while (1):
            s = ser.read(mycharger.readsize)
            mycharger.process_serial_data(s)
                # print(ultraduo.ultraduo.ch1.print())

    except KeyboardInterrupt:
        print ('^C received, closing serial port')
        ser.close()
        p.close()
        f.close()
        
import imaxb6
import ultraduo

if __name__ == '__main__':
    serial_server('COM167', imaxb6.ImaxB6())
