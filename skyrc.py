#!/usr/bin/python
import skyrcdevice
import charger
import threading

class SkyRCChannel(charger.Channel):

  def parseData(self, data):
    if data == None:
      return

    self.capacity           = (data[1]*256) + data[2]
    self.chargecount        = (data[3]*256) + data[4]
    self.voltage            = (data[5]*256) + data[6]
    self.current            = (data[7]*256) + data[8]
    self.temperature        = data[9]
    self.internal_temp      = data[10]
    self.impendance         = (data[11]*256) + data[12]
    self.cells[0]           = (data[13]*256) + data[14]
    self.cells[1]           = (data[15]*256) + data[16]
    self.cells[2]           = (data[17]*256) + data[18]
    self.cells[3]           = (data[19]*256) + data[20]
    self.cells[4]           = (data[21]*256) + data[22]
    self.cells[5]           = (data[23]*256) + data[24]
    self.cells[6]           = (data[25]*256) + data[26]
    self.cells[7]           = (data[27]*256) + data[28]

    if data[0] == 0 or data[0] == 2:
      self.status = 'idle'
    elif data[0] == 1 or data[0] > 4:
      self.status = 'charging'
    elif data[0] == 3:
      self.status = 'ready'
    else:
      self.status = 'error ' + str(data[0]) +':'+str(data[1]<<8+data[2])

  def parseSystemFeed(self, data):
    if data == None:
      return
    cell1 =  (data[16]*256) + data[17]
    # connection logic
    if (cell1 > 1000):
      self.connected = True
    # on disconnect
    elif self.connected:
      self.battery = None
      self.connected = False


class SkyRC(charger.Charger):
  def __init__(self, sample_time = 0.2):
    self.channels = []
    self.name = "SkyRC Charger"
    self.dev = skyrcdevice.SkyRCDevice()
    self.channels.append(SkyRCChannel())
    self.sample_time = sample_time

  def identify(self, battery):
    # We have to start charging if we succesfully identified
    if super().identify(battery):
      print('Start charging')
      if not self.dev.startChargeLipo(battery.cells, battery.ccurrent):
        self.channels[0].battery = None
        return False
      return True
    return False

  def run(self):
    lock = threading.Lock()
    while True:
      lock.acquire()
      try:
        self.channels[0].parseSystemFeed(self.dev.getSystemFeed())
        self.channels[0].parseData(self.dev.getData())
        time.sleep(self.sample_time)
      finally:
        lock.release()

import time
if __name__ == '__main__':
  charger = SkyRC()
  charger.start()
