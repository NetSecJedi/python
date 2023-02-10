import board
import adafruit_sht31d
from time import sleep
#import logging
#import syslog
import os
import socket

# Set up UDP packet parameters
IP="airspy"
PORT=9999
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

# CPU Temp function, pilfered from https://www.pragmaticlinux.com/2020/06/check-the-raspberry-pi-cpu-temperature/
def get_cpu_temp():
    """
    Obtains the current value of the CPU temperature.
    :returns: Current value of the CPU temperature if successful, zero value otherwise.
    :rtype: float
    """
    # Initialize the result.
    result = 0.0
    # The first line in this file holds the CPU temperature as an integer times 1000.
    # Read the first line and remove the newline character at the end of the string.
    if os.path.isfile('/sys/class/thermal/thermal_zone0/temp'):
        with open('/sys/class/thermal/thermal_zone0/temp') as f:
            line = f.readline().strip()
        # Test if the string is an integer as expected.
        if line.isdigit():
            # Convert the string with the CPU temperature to a float in degrees Celsius.
            result = float(line) / 1000
    # Give the result back to the caller.
    return result

def send_udp(MESSAGE):
    sock.sendto(MESSAGE.encode(),(IP,PORT))


# Set up INFO and DEBUG log files
#logging.basicConfig(filename='/home/pi/temp_hum.log', encoding='utf-8', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

# Create sensor object to read temp and humidity from SHT30
i2c = board.I2C()
sensor = adafruit_sht31d.SHT31D(i2c)

try: 
    temp = sensor.temperature # read temperature 
    humidity = sensor.relative_humidity # read humidity
except:
    ERROR="Error reading sensor, in use"
    #logging.error(ERROR)
    #syslog.syslog(syslog.LOG_ERR, ERROR)
    send_udp(ERROR)

TEMP="Temperature: %0.1f C" % temp
HUM="Humidity: %0.1f %%" % humidity
T_CPU="CPU Temp: {:.2f} C".format(get_cpu_temp())

send_udp(TEMP)
send_udp(HUM)
send_udp(T_CPU)

#logging.info("Temperature: %0.1f C" % temp)
#syslog.syslog(syslog.LOG_INFO, "Temperature: %0.1f C" % temp)
#logging.info("Humidity: %0.1f %%" % humidity)
#syslog.syslog(syslog.LOG_INFO, "Humidity: %0.1f %%" % humidity)
#logging.info("CPU Temp: {:.2f} C".format(get_cpu_temp()))
#syslog.syslog(syslog.LOG_INFO, "CPU Temp: {:.2f} C".format(get_cpu_temp()))