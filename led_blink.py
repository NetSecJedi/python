import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(37, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(33, GPIO.OUT, initial=GPIO.HIGH)

while True:
    GPIO.output(37, GPIO.HIGH)
    GPIO.output(33, GPIO.LOW)
    sleep(.3)
    GPIO.output(37, GPIO.LOW)
    GPIO.output(33, GPIO.HIGH)
    sleep(.3)