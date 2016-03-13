#!/usr/bin/python

import charger


class UltraDuoChannel(charger.Channel):
    """Single Channel of Ultra Duo"""

    #000000	-> nothing
    #010800	-> charging CC/CV
    #010B00	-> charging FAST
    #010700	-> charging Store 3.90
    #010900	-> charging CV Link
    #030001	-> pause: wait before discharge
    #050200	-> ready
    #050400	-> overtemperature
    #070000	-> pure balancing
    #020200	-> discharge normal
    #020300	-> discharge linear
    #020700     -> discharge Store 3.90
    #060300	-> error battery disconnected
    #061100	-> error balancer disconnected

    def decode_status(self, status):
        ret = 'parse-error'
        if (len(status) == 6):
            s = status[1]
            #ret += str(bin(int(self.status[1],16)))
            #ret += str(bin(int(self.status[3],16)))
            if (s == '1'):
                ret = 'charging'
            elif (s == '2'):
                ret = 'discharging'
            elif (s == '3'):
                ret = 'waiting'
            elif (s == '6'):
                ret = 'error'
            elif (s == '7'):
                ret = 'balancing'
            elif ((s == '0') or (s == '5')):
                ret = 'ready'
            else:
                ret = 'unknown'
        return ret
    
    def parse(self, s):
        if (len(s) == 64):
            # store raw
            self.raw_data = s
            # parse content
            self.battery = 'CDW' + str(int(s[0:2],16))
            self.identification = 'identified'
            self.chargecount = int(s[2:6],16)
            self.inputvoltage = int(s[6:10],16)
            self.status = self.decode_status(s[10:16])
            self.voltage = int(s[16:20],16)
            self.current = int(s[20:24],16)
            self.capacity = int(s[24:28],16)
            self.temperature = int(s[28:32],16)
            self.extra['unknown'] = s[32:36]
            self.extra['status'] = s[10:16]
            nr = 0
            for i in [36,40,44,48,52,56,60]:
                self.cells[nr] = int(s[i:i+4] , 16)
                nr = nr + 1
            # connection logic
            if (self.cells[0] > 0) or (self.status == 'charging') or (self.status == 'discharging'):
                self.connection = 'connected'
            else:
                self.connection = 'disconnected'
            self.newdata += 1

class UltraDuo(charger.Charger):
    def __init__(self):
        self.channels = []
        self.readsize = 128
        self.baudrate = 9600
        self.name = 'Graupner Ultra Duo Plus 60'
        self.channels.append( UltraDuoChannel() )
        self.channels.append( UltraDuoChannel() )
        self.line = ''

    def parse(self,line):
        if ((len(line) >= 136) and (len(line) <=138)):
            if (line[0:4] == '8205'):
                v = [ line[0:4] , line[4:68] , line[68:132], line[132:136] ]
                self.channels[0].parse(v[1])
                self.channels[1].parse(v[2])
            else:
                print("Parsed Bad Line (header error): " + line)
        else:
            print("Parsed Bad Line (size error): " + line)

    def process_serial_data(self,s):
        updated = 0
        s = s.decode('utf-8')
        s = s.replace('\x0c','')
        self.line = self.line + s
        if (s.find('\r') > 0):
            updated = 1
            self.parse(self.line)
            print(self.line)
            self.line = ''
        return updated
        

if __name__ == '__main__':
    f = open('teraterm.log')
    lines = f.readlines()
    f.close()

    #f = open('result.txt', 'w')
    #for line in lines:
    #    f.write(line[0:4]+ " " + line[4:10]+ " " +
    #            line[10:14]+ " " +
    #            line[14:20]+ " " + # 6 elements status
    #            line[20:24]+ " " + line[24:28]+ " " +
    #            line[28:32]+ " " + line[32:36]+ " " +
    #            line[36:40]+ " " + # 0100
    #            line[40:44]+ " " + line[44:48] + " " + line[48:52] + " " + # 3 cols
    #            line[52:68] + " " + # pause 16
    #            line[68:74] + " " + line[74:78] + " " +
    #            line[78:84] + " " + # e elements status
    #            line[84:88] + " " +
    #            line[88:92] + " " + line[92:96] + " " + line[96:100] + " " +
    #            line[100:104] + " " + # 0100
    #            line[104:108] + " " + line[108:112] + " " + line[112:116] + " " +  # 3 cols
    #            line[116:132] + " " + # pause 16
    #            line[132:]) # checksum?
    #f.close()

    mycharger = UltraDuo()
    p = open('converted.csv', 'w')
    p.write(charger.Channel().header()+ " " + charger.Channel().header()+"\n")
    for line in lines:
        mycharger.parse(line)
        p.write(mycharger.channels[0].print() + " " + mycharger.channels[1].print() + "\n")
    p.close()
