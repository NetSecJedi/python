import board
import adafruit_sht31d
from datetime import datetime, date, time, timezone
import os
import socket
import json

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

def format_json(TEMP,HUM,CPU):
    ts = datetime.now(timezone.utc)
    jsonstr = { "Timestamp" : ts.isoformat(), "Temperature" : TEMP, "CPU Temp": CPU, "Humidity" : HUM }
    return json.dumps(jsonstr)

# Create sensor object to read temp and humidity from SHT30
i2c = board.I2C()
sensor = adafruit_sht31d.SHT31D(i2c)

try: 
    temp = sensor.temperature # read temperature 
    humidity = sensor.relative_humidity # read humidity
except:
    ts = datetime.now(timezone.utc)
    ERROR = { "Timestamp" : ts.isoformat(), "Error" : "Error reading sensor, in use" }
    send_udp(json.dumps(ERROR))

TEMP="%0.1f C" % temp
HUM="%0.1f %%" % humidity
T_CPU="{:.2f} C".format(get_cpu_temp())

send_udp(format_json(TEMP,HUM,T_CPU))