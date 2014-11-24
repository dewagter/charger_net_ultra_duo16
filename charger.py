


class Channel():
    """Store the charging state of a single battery"""
    def __init__(self):
        self.input = ''
        self.battery = 0
        self.chargecount = 0
        self.inputvoltage = 0
        self.status = 'unknown'
        self.voltage = 0
        self.current = 0
        self.capacity = 0
        self.temperature = 0
        self.cells = [0, 0, 0, 0, 0, 0, 0, 0]
        self.extra = {}

    def print(self):
        s = str(self.battery) + ","
        s = s + str(self.chargecount) + ","
        s = s + str(self.inputvoltage) + ","
        s = s + "\'" + self.status + ","
        s = s + str(self.voltage) + ","
        s = s + str(self.current) + ","
        s = s + str(self.capacity) + ","
        s = s + str(self.temperature) + ","
        for i in range(0,8):
            s = s +( str(self.cells[i]) + ",")
        return s

    def header(self):
        return "battery,chargecount,inputvoltage,status,voltage,current,capacity,temperature,cell1,cell2,cell3,cell4,cell5,cell6,cell7,cell8,"
    

class Charger():
    def __init__(self):
        channels = []

