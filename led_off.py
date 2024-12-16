import RPi.GPIO as GPIO
from time import sleep
import board

GPIO.setwarnings(False)
#GPIO.setup(37, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(24, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(25, GPIO.OUT, initial=GPIO.HIGH)
#GPIO.output(37, GPIO.LOW)
GPIO.output(24, GPIO.LOW)
GPIO.output(25, GPIO.LOW)