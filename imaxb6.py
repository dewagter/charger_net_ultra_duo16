import time
import serial
#import ultraduo
import threading

def decimal(data, offset):
    return data[offset+1] + data[offset+2] / 100.0;

def imax_b6_decode(data):
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

    
    print(data)
    # Protocol reverse engineered by
    # Ref: http://blog.dest-unreach.be/2012/01/29/imax-b6-charger-protocol-reverse-engineered
    sample['state']         = data[7+1]
    sample['mode']          = data[22+1]
    sample['active']        = data[23+1]
    sample['current']       = decimal(data, 32)
    sample['voltage']       = decimal(data, 34)
    sample['input_voltage'] = decimal(data, 40)
    sample['charge']        = decimal(data, 42) / 10.0
    sample['cell1']         = decimal(data, 44)
    sample['cell2']         = decimal(data, 46)
    sample['cell3']         = decimal(data, 48)
    sample['cell4']         = decimal(data, 50)
    sample['cell5']         = decimal(data, 52)
    sample['cell6']         = decimal(data, 54)
    sample['minutes']       = data[69+1]
    print(sample)
    return sample
    





def serial_server(port):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    #p = open('logfile_' + timestr + '.csv', 'w')
    f = open('raw_' + timestr + '.hex', 'w')
    #p.write(ultraduo.Charge().header()+ " " + ultraduo.Charge().header()+"\n")
    lock = threading.Lock()
    try:
        ser=serial.Serial(port, 9600, timeout=0.05)
        line = []
        count = 0
        while (1):
            s = ser.read(32)
            for b in s:
                line.append(b)
                count += 1
                if (b == ord('{')):
                    #print("<START>")
                    line = [ b ]
                    count = 1
                elif (b == ord('}')):
                    #print("<STOP>")
                    if (len(line) == 76):
                        if (line[0] == ord('{')):
                            #print(line)
                            imax_b6_decode(line)
                        else:
                            print("Bad start character")
                    else:
                        print("Bad line length: " + str(len(line)) + " / " + str(count))
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
