#!/usr/bin/python
import skyrchelper
import charger

class SkyRCChannel(charger.Channel):

  def parseData(self, data):
    self.capacity           = (data[1]*256) + data[2]
    self.chargecount        = (data[3]*256) + data[4]
    self.voltage            = (data[5]*256) + data[6]
    self.current            = (data[7]*256) + data[8]
    self.temperature        = data[9]
    self.extra['int_temp']  = data[10]
    self.extra['impend']    = (data[11]*256) + data[12]
    self.cells[0]           = (data[13]*256) + data[14]
    self.cells[1]           = (data[15]*256) + data[16]
    self.cells[2]           = (data[17]*256) + data[18]
    self.cells[3]           = (data[19]*256) + data[20]
    self.cells[4]           = (data[21]*256) + data[22]
    self.cells[5]           = (data[23]*256) + data[24]
    self.cells[6]           = (data[25]*256) + data[26]
    self.cells[7]           = (data[27]*256) + data[28]

    if data[0] == 0 or data[0] == 2 or data[0] == 3:
        self.status = 'ready'
    elif data[0] == 1:
        self.status = 'charging'
    else:
        self.status = 'error'

  def parseSystemFeed(self, data):
    voltage =  (data[16]*256) + data[17]
    # connection logic
    if (voltage > 1000):
      self.connection = 'connected'
    else:
      # On disconnect:
      if self.connection == 'connected':
        self.identification = 'unknown'
        self.connection = 'disconnected'

class SkyRC(charger.Charger):
  def __init__(self):
    self.channels = []
    self.name = "SkyRC Charger"
    self.dev = skyrchelper.SkyRCHelper()
    self.channels.append(SkyRCChannel())

  def run(self):
    self.channels[0].parseSystemFeed(self.dev.getSystemFeed())
    self.channels[0].parseData(self.dev.getData())
    time.sleep(0.2)

import time
if __name__ == '__main__':
  test = SkyRC()
  while True:
    test.run()
