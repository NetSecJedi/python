import RPi.GPIO as GPIO
from time import sleep
import board

GPIO.setwarnings(False)
GPIO.setup(25, GPIO.OUT, initial=GPIO.HIGH)

def read_err_wait():
    for x in range(30):
        GPIO.output(25, GPIO.LOW)
        sleep(0.5)
        GPIO.output(25, GPIO.HIGH)
        sleep(0.5)

read_err_wait()
GPIO.output(25, GPIO.LOW)