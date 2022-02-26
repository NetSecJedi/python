import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(36, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(38, GPIO.OUT, initial=GPIO.HIGH)

sleep(5)
GPIO.output(36, GPIO.LOW)
sleep(5)
GPIO.output(36, GPIO.HIGH)
sleep(5)
GPIO.output(38, GPIO.LOW)
sleep(5)
GPIO.output(38, GPIO.HIGH)
