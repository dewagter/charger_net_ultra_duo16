import RPi.GPIO as GPIO

GREEN = 7
ORANGE = 11
RED = 15


ON = True
OFF = False


def init():
    # Setup LEDs
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    
    GPIO.setup(GREEN, GPIO.OUT)
    GPIO.setup(ORANGE, GPIO.OUT)
    GPIO.setup(RED, GPIO.OUT)
    
    GPIO.output(GREEN,False)
    GPIO.output(ORANGE,False)
    GPIO.output(RED,False)


def set(led,value):
    GPIO.output(led, value)

def toggle(led):
    GPIO.output(led,not GPIO.input(led))


def blink():
    # Boot sequence
    for i in range(0, 5):
        set(GREEN,ON)
        set(ORANGE,ON)
        set(RED,ON)
        time.sleep(0.2)
        set(GREEN,OFF)
        set(ORANGE,OFF)
        set(RED,OFF)
        time.sleep(0.2)

import time

if __name__ == '__main__':
    init()
    blink()
