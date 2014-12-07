#!/usr/bin/python

# Install using:
# sudo apt-get update
# sudo apt-get install python3-pip
# sudo sudo pip-3.2 install nxppy
# Enable SPI: raspi-conf or
# sudo vi /etc/modprobe.d/raspi-blacklist.conf
# Reboot or sudo modprobe spi-bcm2708

import http.client
import nxppy
import time
import settings
import _thread

class Battery():
    id = ''
    type = None
    cells = 0
    ccurrent = 0
    dcurrent = 0

def nfc_server(logserver_address, bat_handler):
    mifare = nxppy.Mifare()
    while True:
        try:
            uid = mifare.select()
        except nxppy.SelectError:
            continue
        if uid is None:
            continue
        uid = uid[1:]

        #try:
        conn = http.client.HTTPConnection(logserver_address, 80,timeout=10)
        conn.request("GET", "/charger.php?id=" + uid + "&action=info")
        res = conn.getresponse()
        data = res.read().decode('utf-8').split('|')

        # When we got a User
        if data[0] == 'USER':
            print('USER logged in')
        # When we got a battery
        elif len(data) == 4:
            battery = Battery()
            battery.id = uid
            battery.type = data[0]
            battery.cells = int(data[1])
            battery.ccurrent = int(data[2])
            battery.dcurrent = int(data[3])
            
            # TODO: Fix a nicer way
            while not bat_handler(battery):
                time.sleep(0.3)
        else:
            print('NFC TAG is not registered')
        #except:
        #    print('Could not connect to database')

        time.sleep(1)

def start(logserver_address, bat_handler):
    _thread.start_new_thread(nfc_server, (logserver_address, bat_handler))

if __name__ == '__main__':
    nfc_server()
