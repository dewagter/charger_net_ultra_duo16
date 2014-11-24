import time
import serial
import charger
import threading

def decimal(data, offset):
    return data[offset+1] * 1000 + data[offset+2] * 10;


class ImaxB6Channel(charger.Channel):    

    def decode_array(self, data):
        sample = {}
        if not (len(data) == 76):
            print("Length Error")
        if not (data[0] == ord('{')):
            print("Start Error")
        if not (data[75] == ord('}')):
            print("End Error")
        crc = 0
        for i in range(1,73):
            crc += data[i]
        crc = crc % 256
        c1 = (crc & 0x0f) + 0x30
        c2 = ((crc & 0xf0) >> 4) + 0x30
        if not ((c2 == data[73]) and (c1 == data[74])) :
            print("CRC ERROR: sum=", hex(crc), hex(data[73]), "!=?", hex(c2), hex(data[74]),"!=?",hex(c1))

        for i in range(1,73):
            data[i] -= 128

        
        # print(data)
        # Protocol reverse engineered by
        # Ref: http://blog.dest-unreach.be/2012/01/29/imax-b6-charger-protocol-reverse-engineered
        sample['state']         = data[7+1]
        sample['mode']          = data[22+1]
        sample['active']        = data[23+1]
        self.current            = decimal(data, 32)
        self.voltage            = decimal(data, 34)
        self.inputvoltage       = decimal(data, 40)
        self.capacity           = decimal(data, 42) / 10.0
        self.cells[0]           = decimal(data, 44)
        self.cells[1]           = decimal(data, 46)
        self.cells[2]           = decimal(data, 48)
        self.cells[3]           = decimal(data, 50)
        self.cells[4]           = decimal(data, 52)
        self.cells[5]           = decimal(data, 54)
        sample['minutes']       = data[69+1]

        if sample['active'] == 0:
            self.status = 'ready'
        elif sample['active'] == 1:
            if sample['state'] == 1:
                self.status = 'charging'
            elif sample['state'] == 0:
                self.status = 'discharging'
            else:
                self.status = 'unknown'
        else:
            self.status = 'unknown'
            
        #print(sample)

        self.extra = sample


class ImaxB6(charger.Charger):
    def __init__(self):
        self.channels = []
        self.line = []
        self.readsize = 32
        self.baudrate = 9600
        self.name = "IMAX B6 Charger"
        self.channels.append(ImaxB6Channel())

    def parse(self,line):
        self.channels[0].decode_array(line)

    def process_serial_data(self,feed):
        for b in feed:
            self.line.append(b)
            if (b == ord('{')):
                #print("<START>")
                self.line = [ b ]
            elif (b == ord('}')):
                #print("<STOP>")
                if (len(self.line) == 76):
                    if (self.line[0] == ord('{')):
                        #print(line)
                        self.parse(self.line)
                    else:
                        print("Bad start character")
                else:
                    print("Bad line length: " + str(len(self.line)))
        


    
    





def serial_server(port):

    mycharger = ImaxB6()
    
    timestr = time.strftime("%Y%m%d-%H%M%S")
    #p = open('logfile_' + timestr + '.csv', 'w')
    f = open('raw_' + timestr + '.hex', 'w')
    #p.write(ultraduo.Charge().header()+ " " + ultraduo.Charge().header()+"\n")
    lock = threading.Lock()
    try:
        ser=serial.Serial(port, mycharger.baudrate, timeout=0.05)
        while (1):
            s = ser.read(mycharger.readsize)
            mycharger.process_serial_data(s)
            f.write(str(s))
            #line = line + s
            #if (s.find('\r') > 0):
            #    lock.acquire()
            #    try:
                    #ultraduo.ultraduo.parse(line)
                    #p.write(ultraduo.ultraduo.ch1.print() + " " + ultraduo.ultraduo.ch2.print() + "\n")
            #    finally:
            #        lock.release()

    except KeyboardInterrupt:
        print ('^C received, closing serial port')
        ser.close()
        #p.close()
        f.close()
        

if __name__ == '__main__':
    serial_server('COM167')
