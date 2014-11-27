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
