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
from datetime import datetime, date, time, timezone
from time import sleep
import socket
import syslog
import json

# Set up UDP packet parameters
IP="airspy" #send to our Node Red server
PORT=10000
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

def send_udp(MESSAGE):
    sock.sendto(MESSAGE.encode(),(IP,PORT))

def format_json(action,msg):
    ts = datetime.now(timezone.utc)
    if action == "Error":
        jsonstr = { "Timestamp" : ts.isoformat(), "Action" : action, "Message": msg }
    else:
        jsonstr = { "Timestamp" : ts.isoformat(), "Action" : action, "Temperature": msg}   
    return json.dumps(jsonstr)

# Indicate script is starting
syslog.syslog(syslog.LOG_INFO, "Starting Exhaust Fan system...")
syslog.syslog(syslog.LOG_INFO, "Initializing GPIO ports...")

GPIO.setwarnings(False) # Turn off GPIO warnings
GPIO.setup(16, GPIO.OUT, initial=GPIO.HIGH)  # Relay signal IN1, board pin 36 GPIO 16, default HIGH (off)
GPIO.setup(25, GPIO.OUT, initial=GPIO.HIGH)  # Green LED indicating System On
GPIO.setup(24, GPIO.OUT, initial=GPIO.LOW) # Blue LED indicating fan on

syslog.syslog(syslog.LOG_INFO, "Initializing Adaruit SHT30 I2C sensor...")
# Create sensor object to read temp and humidity from SHT30
i2c = board.I2C()
sensor = adafruit_sht31d.SHT31D(i2c)

syslog.syslog(syslog.LOG_INFO, "Setting Temp max and min values.....")
tmp_th_max = 29.5 # Set temperature max threshold
tmp_th_min = 27.0 # Set temperature min threshold
read_errors = 0 # track read errors

MESSAGE=""

syslog.syslog(syslog.LOG_INFO, "Entering system loop, stay fresh!")
# Wait for 30 seconds when 10 read errors in succession and blink Green LED in half second intervals
def read_err_wait():
    MESSAGE="Excessive errors reading temperature sensor, waiting 60 seconds...."
    #syslog.syslog(syslog.LOG_ERR, MESSAGE )
    send_udp(format_json("Error",MESSAGE))
    for x in range(60):
        GPIO.output(25, GPIO.LOW)
        sleep(0.5)
        GPIO.output(25, GPIO.HIGH)
        sleep(0.5)

while True: 
        
    relay_status = GPIO.input(16) # Check if relay is on, or set to LOW (0)

    try:
        temp = sensor.temperature # read temperature value
        read_errors = 0
        # SHT30 temperature values are in Centigrade, 32C is 90F
        # If temp is above tmp_th_max activate the relay powering our exhaust fan
        # until temp reaches tmp_th_min
        if relay_status == 1 and temp > tmp_th_max:
            GPIO.output(16, GPIO.LOW) # turn on fan relay
            GPIO.output(24, GPIO.HIGH)
            TEMP='%0.1f C' % temp
            send_udp(format_json("Activated",TEMP))
        elif relay_status == 0 and temp < tmp_th_min:
            GPIO.output(16, GPIO.HIGH) # turn off fan relay
            GPIO.output(24, GPIO.LOW)
            TEMP='%0.1f C' % temp
            send_udp(format_json("Deactivated",TEMP))
    except:
        MESSAGE="Error reading sensor, retrying...."
        #syslog.syslog(syslog.LOG_ERR, MESSAGE)
        send_udp(format_json("Error",MESSAGE))
        read_errors += 1
        if read_errors == 10:
            read_err_wait()

    sleep(30)