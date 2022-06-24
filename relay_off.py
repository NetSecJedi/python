import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(36, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(38, GPIO.OUT, initial=GPIO.HIGH)