import serial
import ultraduo
import threading


def serial_server(port):
    lock = threading.Lock()
    try:
        ser=serial.Serial(port, 9600, timeout=0.05)
        line = ''
        while (1):
            s = ser.read(64)
            s = s.decode('utf-8')
            s = s.replace('\x0c','')
            line = line + s
            if (s.find('\r') > 0):
                lock.acquire()
                try:
                    ultraduo.ultraduo.parse(line)
                finally:
                    lock.release()
                print(line)
                line = ''
                # print(ultraduo.ultraduo.ch1.print())

    except KeyboardInterrupt:
        print ('^C received, closing serial port')
        ser.close()
        

if __name__ == '__main__':
    serial_server()
