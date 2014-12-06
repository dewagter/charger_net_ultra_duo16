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

class Tag():
    id = ''
    new = 0
    bat_type = None
    bat_cells = 0
    bat_ccurrent = 0
    bat_dcurrent = 0

tag = Tag()

def nfc_server():
    mifare = nxppy.Mifare()
    while True:
        try:
            uid = mifare.select()
        except nxppy.SelectError:
            continue
        if uid is None:
            continue
        uid = uid[1:]
        print('Found NFC tag: ' + uid)

        try:
            conn = http.client.HTTPConnection(settings.LOGSERVER_URL, 80,timeout=10)
            conn.request("GET", "/charger.php?id=" + uid + "&action=info")
            res = conn.getresponse()
            data = res.read().decode('utf-8').split('|')
            if data[0] == 'USER':
                print('USER logged in')
            elif len(data) == 4:
                tag.id = uid
                tag.new = 1
                tag.bat_type = data[0]
                tag.bat_cells = data[1]
                tag.bat_ccurrent = data[2]
                tag.bat_dcurrent = data[3]
                print("Found battery "+
                    str(tag.bat_type)+" "+
                    str(tag.bat_cells)+"S "+
                    str(tag.bat_ccurrent)+"mA/"+
                    str(tag.bat_dcurrent)+"mA")
            else:
                print('TAG not valid')
        except:
            print('Could not connect to database')

        time.sleep(1)


if __name__ == '__main__':
    nfc_server()
