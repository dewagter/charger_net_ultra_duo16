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


def blink():
    # Boot sequence
    for i in range(0, 5):
        led.set(led.GREEN,led.ON)
        led.set(led.ORANGE,led.ON)
        led.set(led.RED,led.ON)
        time.sleep(0.2)
        led.set(led.GREEN,led.OFF)
        led.set(led.ORANGE,led.OFF)
        led.set(led.RED,led.OFF)
        time.sleep(0.2)

if __name__ == '__main__':
    init()
    blink()
