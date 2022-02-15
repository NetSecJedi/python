# Test Py script to read temperature from the AdaFruit SHT30 sensor via I2C
# and turn close a relay switch via GPIO

import board
import adafruit_sht31d
import RPi.GPIO as GPIO
from time import sleep

# Set up the GPIO Relay using pin 36 (GPIO 16) set low by default
GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(13, GPIO.OUT, initial=GPIO.LOW)  # Red LED
GPIO.setup(26, GPIO.OUT, initial=GPIO.HIGH) # Green LED

# Create sensor object to read temp and humidity from SHT30
i2c = board.I2C()
sensor = adafruit_sht31d.SHT31D(i2c)

relay_status = 0

while True: 
    print("\nTemperature: %0.1f C" % sensor.temperature)
    print("Humidity: %0.1f %%" % sensor.relative_humidity)
    if relay_status == 0 and sensor.temperature > 32.222:
        GPIO.output(16, GPIO.HIGH)
        GPIO.output(26, GPIO.LOW)
        GPIO.output(13, GPIO.HIGH)
        relay_status = 1
        print("Cooling activated")
    elif relay_status == 1 and sensor.temperature < 32.222:
        GPIO.output(16, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(26, GPIO.HIGH)
        relay_status = 0
        print("Cooling Deactivated") 
    else:
        if relay_status == 1:
            print("Fan Running")
        else:
            print("Fan Off")     

    sleep(5)
