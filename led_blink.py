import RPi.GPIO as GPIO
from time import sleep
import logging
import board

GPIO.setwarnings(False)
GPIO.setup(25, GPIO.OUT, initial=GPIO.HIGH)
logging.basicConfig(filename='fan.log', encoding='utf-8', level=logging.DEBUG)

def read_err_wait():
    logging.error("Excessive errors reading temperature sensor, waiting 30 seconds....")
    for x in range(30):
        GPIO.output(25, GPIO.LOW)
        sleep(0.5)
        GPIO.output(25, GPIO.HIGH)
        sleep(0.5)

read_err_wait()
