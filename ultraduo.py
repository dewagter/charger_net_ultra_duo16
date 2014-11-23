
class Charge:
    def __init__(self):
        input = ''
        battery = 0
        chargecount = 0
        inputvoltage = 0
        status = ''
        voltage = 0
        current = 0
        capacity = 0
        temperature = 0
        v2 = 0
        cells = [0, 0, 0, 0, 0, 0, 0]

    def print(self):
        s = str(self.battery) + ","
        s = s + str(self.chargecount) + ","
        s = s + str(self.inputvoltage) + ","
        s = s + "\'" + self.status + ","
        s = s + str(self.voltage) + ","
        s = s + str(self.current) + ","
        s = s + str(self.capacity) + ","
        s = s + str(self.temperature) + ","
        for i in range(0,7):
            s = s +( str(self.cells[i]) + ",")
        return s

    def header(self):
        return "battery,chargecount,inputvoltage,status,voltage,current,capacity,temperature,cell1,cell2,cell3,cell4,cell5,cell6,cell7,"
    
    def parse(self, s):
        if (len(s) == 64):
            # store raw
            self.input = s
            # parse content
            self.battery = int(s[0:2],16)
            self.chargecount = int(s[2:6],16)
            self.inputvoltage = int(s[6:10],16)
            self.status = s[10:16]
            self.voltage = int(s[16:20],16)
            self.current = int(s[20:24],16)
            self.capacity = int(s[24:28],16)
            self.temperature = int(s[28:32],16)
            self.v2 = s[32:36]
            nr = 0
            for i in [36,40,44,48,52,56,60]:
                self.cells[nr] = int(s[i:i+4] , 16)
                nr = nr + 1
    

class UltraDuo:
    def __init__(self):
        ch1 = Charge()
        ch2 = Charge()

    def parse(self,line):
        v = [ line[0:4] , line[4:68] , line[68:132], line[132:136] ]
        self.ch1.parse(v[1])
        self.ch2.parse(v[2])

ultraduo = UltraDuo()

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

    p = open('converted.csv', 'w')
    p.write(Charge().header()+ " " + Charge().header()+"\n")
    for line in lines:
        ultraduo.parse(line)
        p.write(ultraduo.ch1.print() + " " + ultraduo.ch2.print() + "\n")
    p.close()
