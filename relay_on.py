import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(36, GPIO.OUT, initial=GPIO.LOW)

GPIO.output(36, GPIO.HIGH)
sleep(3)
GPIO.output(36, GPIO.LOW)