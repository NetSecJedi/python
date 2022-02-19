# Author: NetSecJedi
# Date: 2/15/2022
# A Python script to read temperature from an AdaFruit SHT30 sensor via I2C on a Raspberry Pi
# and turn on a relay module powering an exhaust fan when the temperature reaches a threshold.
# Power in from mains or battery is connected to the common lug (middle) on the relay
# and the outbound lead to the fan connected to the default open lug.

# *** Ensure that I2C is turned on from the raspi-config menu otherwise Python will generate an
# error when calling board.I2C() function

import board
import adafruit_sht31d
import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False) # Turn off GPIO warnings
GPIO.setup(16, GPIO.OUT, initial=GPIO.LOW)  # Relay Signal, board pin 36 GPIO 16, default LOW
GPIO.setup(13, GPIO.OUT, initial=GPIO.LOW)  # An LED indicating fan on
GPIO.setup(26, GPIO.OUT, initial=GPIO.HIGH) # An LED indicating fan off

# Create sensor object to read temp and humidity from SHT30
i2c = board.I2C()
sensor = adafruit_sht31d.SHT31D(i2c)

tmp_th = 18.7 # Set our temperature threshold

while True: 
    print("\nTemperature: %0.1f C" % sensor.temperature)
    print("Humidity: %0.1f %%" % sensor.relative_humidity)
    
    relay_status = GPIO.input(16) # Check if relay is on, or set to HIGH (1)
    
    # SHT30 temperature values are in Centigrade, 32C is 90F
    # If temp is above 32C/90F turn on the relay powering our exhaust fan
    if relay_status == 0 and sensor.temperature > tmp_th:
        GPIO.output(16, GPIO.HIGH)
        GPIO.output(26, GPIO.LOW)
        GPIO.output(13, GPIO.HIGH)
        print("Cooling activated")
    elif relay_status == 1 and sensor.temperature < tmp_th:
        GPIO.output(16, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(26, GPIO.HIGH)
        print("Cooling Deactivated") 
    else:
        if relay_status == 1:
            print("Fan Running")
        else:
            print("Fan Off")     

    sleep(5)
