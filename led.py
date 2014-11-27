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
