import time
import serial
import ultraduo
import threading


def serial_server(port):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    p = open('logfile_' + timestr + '.csv', 'w')
    f = open('raw_' + timestr + '.hex', 'w')
    p.write(ultraduo.Charge().header()+ " " + ultraduo.Charge().header()+"\n")
    lock = threading.Lock()
    try:
        ser=serial.Serial(port, 9600, timeout=0.05)
        line = ''
        while (1):
            s = ser.read(64)
            s = s.decode('utf-8')
            s = s.replace('\x0c','')
            f.write(s)
            line = line + s
            if (s.find('\r') > 0):
                lock.acquire()
                try:
                    ultraduo.ultraduo.parse(line)
                    p.write(ultraduo.ultraduo.ch1.print() + " " + ultraduo.ultraduo.ch2.print() + "\n")
                finally:
                    lock.release()
                print(line)
                line = ''
                # print(ultraduo.ultraduo.ch1.print())

    except KeyboardInterrupt:
        print ('^C received, closing serial port')
        ser.close()
        p.close()
        f.close()
        

if __name__ == '__main__':
    serial_server('COM11')
