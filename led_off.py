import RPi.GPIO as GPIO
from time import sleep
import board

GPIO.setwarnings(False)
GPIO.output(37, GPIO.LOW)
GPIO.output(33, GPIO.LOW)
GPIO.output(25, GPIO.LOW)