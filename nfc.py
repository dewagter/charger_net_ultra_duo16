# Install using:
# sudo apt-get update
# sudo apt-get install python3-pip
# sudo sudo pip-3.2 install nxppy
# Enable SPI: raspi-conf or
# sudo vi /etc/modprobe.d/raspi-blacklist.conf
# Reboot or sudo modprobe spi-bcm2708

import nxppy
import time
import RPi.GPIO as GPIO

class Tag():
    id = ''
    new = 0


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
        tag.id = uid
        tag.new = 1
        print('Found NFC tag: ' + uid)
        GPIO.output(15,not GPIO.input(15))
        time.sleep(1)


if __name__ == '__main__':
    nfc_server()
