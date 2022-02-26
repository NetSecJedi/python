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
import logging

# Set up log file
logging.basicConfig(filename='fan.log', encoding='utf-8', level=logging.DEBUG)

GPIO.setwarnings(False) # Turn off GPIO warnings
GPIO.setup(16, GPIO.OUT, initial=GPIO.HIGH)  # Relay signal IN1, board pin 36 GPIO 16, default HIGH (off)
GPIO.setup(25, GPIO.OUT, initial=GPIO.HIGH)  # Green LED indicating System On
GPIO.setup(24, GPIO.OUT, initial=GPIO.LOW) # Blue LED indicating fan on

# Create sensor object to read temp and humidity from SHT30
i2c = board.I2C()
sensor = adafruit_sht31d.SHT31D(i2c)

tmp_th_max = 21.5 # Set temperature max threshold
tmp_th_min = 19.0 # Set temperature min threshold

while True: 
    print("\nTemperature: %0.1f C" % sensor.temperature)
    print("Humidity: %0.1f %%" % sensor.relative_humidity)
    
    relay_status = GPIO.input(16) # Check if relay is on, or set to LOW (0)
    
    # SHT30 temperature values are in Centigrade, 32C is 90F
    # If temp is above tmp_th_max turn on the relay powering our exhaust fan
    # until temp reaches tmp_th_min
    if relay_status == 1 and sensor.temperature > tmp_th_max:
        GPIO.output(16, GPIO.LOW)
        GPIO.output(24, GPIO.LOW)
        logging.warning('Fan activated at %0.1f C' % sensor.temperature)
    elif relay_status == 0 and sensor.temperature < tmp_th_min:
        GPIO.output(16, GPIO.HIGH)
        GPIO.output(24, GPIO.HIGH)
        logging.warning('Fan Deactivated at %0.1f C' % sensor.temperature) 
    else:
        if relay_status == 0:
            logging.INFO('Fan Running')     

    sleep(5)
