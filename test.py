import usb.core
import sys

def sendPacket( cmd, data, cmd2 = None ):
  if cmd2 != None:
    s_data = bytearray(len(data)+8)
    s_data[0] = 15
    s_data[1] = 4 + len(data)
    s_data[2] = cmd
    s_data[3] = cmd2
    s_data[4] = 0
    checksum = cmd+cmd2
    k = 5
  else:
    s_data = bytearray(len(data)+7)
    s_data[0] = 15
    s_data[1] = 3 + len(data)
    s_data[2] = cmd
    s_data[3] = 0
    checksum = cmd
    k = 4

  for i,b in enumerate(data):
    s_data[i+k] = b
    checksum += b
  s_data[k+len(data)] = checksum % 256
  s_data[k+len(data)+1] = 255
  s_data[k+len(data)+2] = 255
  dev.write(0x1, s_data)

def recvPacket():
  data = dev.read(0x81, 64, timeout=150)
  packet_length = data[1]
  checksum = 0
  for i in range(2, packet_length+1):
    checksum += data[i]

  if checksum%256 != data[packet_length+1]:
    sys.exit("Checksum error " % str(checksum%256) % " " % str(data[packet_length+1]))
  return data[4:packet_length+1]

def recvReply():
  data = dev.read(0x81, 64, timeout=150)
  return (data[0] == 240 and data[1] == 255 and data[2] == 255)

def getSystemFeed():
  sendPacket(90, [])
  data = recvPacket()
  ret_data = {}
  ret_data["cycle_time"] = data[0]
  ret_data["time_limit_enable"] = data[1]
  ret_data["time_limit"] = (data[2]*256) + data[3]
  ret_data["cap_limit_enable"] = data[4]
  ret_data["cap_limit"] = (data[5]*256) + data[6]
  ret_data["key_buzz"] = data[7]
  ret_data["sys_buzz"] = data[8]
  ret_data["in_dc_low"] = (data[9]*256) + data[10]
  # Some unknown data
  ret_data["temp_limit"] = data[13]
  ret_data["voltage"] = (data[14]*256) + data[15]
  ret_data["cell1"] = (data[16]*256) + data[17]
  ret_data["cell2"] = (data[18]*256) + data[19]
  ret_data["cell3"] = (data[20]*256) + data[21]
  ret_data["cell4"] = (data[22]*256) + data[23]
  ret_data["cell5"] = (data[24]*256) + data[25]
  ret_data["cell6"] = (data[26]*256) + data[27]
  ret_data["cell7"] = (data[28]*256) + data[29]
  ret_data["cell8"] = (data[30]*256) + data[31]
  return ret_data

def getData():
  sendPacket(85, [])
  data = recvPacket()
  #return (data)
  ret_data = {}
  ret_data["work_state"] = data[0]
  ret_data["charge_mah"] = (data[1]*256) + data[2]
  ret_data["charge_timer"] = (data[3]*256) + data[4]
  ret_data["out_voltage"] = (data[5]*256) + data[6]
  ret_data["current"] = (data[7]*256) + data[8]
  ret_data["ext_temp"] = data[9]
  ret_data["int_temp"] = data[10]
  ret_data["impendance"] = (data[11]*256) + data[12]
  ret_data["cell1"] = (data[13]*256) + data[14]
  ret_data["cell2"] = (data[15]*256) + data[16]
  ret_data["cell3"] = (data[17]*256) + data[18]
  ret_data["cell4"] = (data[19]*256) + data[20]
  ret_data["cell5"] = (data[21]*256) + data[22]
  ret_data["cell6"] = (data[23]*256) + data[24]
  ret_data["cell7"] = (data[25]*256) + data[26]
  ret_data["cell8"] = (data[27]*256) + data[28]
  return ret_data

# batt_type: [0: lipo, 1: LiIo, 2: LiFe, 3: NiMH, 4: NiCd, 5: Pb]
# mode: for Li** [0: Charge, 1: Discharge, 2: Storage, 3: Discharge, 4: Fast Charge, 5: Balance]
#       for Ni** [0: Charge, 1: Auto Charge, 2: Discharge, 3: Re-peak, 4: Cycle]
#       for Pb** [0: Charge, 1: Discharge]
# ccurrent: Charge current (mA)
# dcurrent: Discharge current (mA)
# cellvolt: Minimum voltage (3200 for LiPo) (mV)
# endvolt: End voltage (4200 for LiPo charge) (mV)
# trickle: ??
# r_peackcount: Resistance peak count???
# cycle_type: ???
# cycle_count: Amount of cycles
def startCharger(batt_type, cells, mode, ccurrent, dcurrent, cellvolt, endvolt,
  trickle = 0, r_peakcount = 1, cycle_type = 1, cycle_count = 1):
  packet = bytearray(17)
  packet[0] = batt_type
  packet[1] = cells
  packet[2] = mode
  packet[3] = ccurrent >> 8
  packet[4] = ccurrent % 256
  packet[5] = dcurrent >> 8
  packet[6] = dcurrent % 256
  packet[7] = cellvolt >> 8
  packet[8] = cellvolt % 256
  packet[9] = endvolt >> 8
  packet[10] = endvolt % 256
  if batt_type > 2 and batt_type < 5 and mode == 3:
    packet[11] = r_peakcount
    packet[12] = 0
  elif batt_type > 2 and batt_type < 5 and mode == 4:
    packet[11] = cycle_type
    packet[12] = cycle_count
  else:
    packet[11] = 0
    packet[12] = 0
  packet[13] = trickle >> 8
  packet[14] = trickle % 256
  packet[15] = 0
  packet[16] = 0
  sendPacket(5, packet)
  return recvReply()

def setCycleTime(time):
  packet = bytearray(1)
  packet[0] = time
  sendPacket(17, packet, 0)
  return recvReply()

def setTimeLimit(enable, limit):
  packet = bytearray(3)
  packet[0] = enable
  packet[1] = limit >> 8
  packet[2] = limit % 256
  sendPacket(17, packet, 1)
  return recvReply()

def setCapLimit(enable, limit):
  packet = bytearray(3)
  packet[0] = enable
  packet[1] = limit >> 8
  packet[2] = limit % 256
  sendPacket(17, packet, 2)
  return recvReply()

def setSound(key_buzz, sys_buzz):
  packet = bytearray(2)
  packet[0] = key_buzz
  packet[1] = sys_buzz
  sendPacket(17, packet, 3)
  return recvReply()

def setTempLimit(temp):
  packet = bytearray(1)
  packet[0] = temp
  sendPacket(17, packet, 5)
  return recvReply()

def startChargeLipo(cells, ccurrent):
  return startCharger(0, cells, 0, ccurrent, ccurrent, 3200, 4200)

def stopCharge():
  sendPacket(254, [])



import time
# find our device (find_all=True)
dev = usb.core.find(idVendor=0x0000, idProduct=0x0001)
if dev is None:
  sys.exit("No IMAX B6 charger is found");

try:
  dev.set_configuration()
  dev.reset()
except usb.core.USBError as e:
  sys.exit("Cannot set configuration of the device: %s" % str(e))

#while True:
#  print(getData())
#  time.sleep(0.4)
#print(startChargeLipo(3, 2000))
#stopCharge()
#getStatusFeed()
#setTempLimit(70)
#setTimeLimit(True, 180)
#setSound(False, False)
#setCapLimit(1,8000)
