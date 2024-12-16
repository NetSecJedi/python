import board
import adafruit_sht31d
from datetime import datetime, date, time, timezone
from time import sleep
from prometheus_client import Gauge, start_http_server
import os
import socket
import json

# Set up UDP packet parameters
IP="airspy"
PORT=10000
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

def send_udp(MESSAGE):
    sock.sendto(MESSAGE.encode(),(IP,PORT))

def format_json(TEMP,HUM):
    ts = datetime.now(timezone.utc)
    jsonstr = { "Timestamp" : ts.isoformat(), "Service" : "ENV", "Temperature" : TEMP, "Humidity" : HUM }
    return json.dumps(jsonstr)

# Create sensor object to read temp and humidity from SHT30
i2c = board.I2C()
sensor = adafruit_sht31d.SHT31D(i2c)

# Set up Prometheus Gauges and metrics http server
temp_g = Gauge('shop_temp_gauge', 'Shop Temperature')
humid_g = Gauge('shop_hum_gauge', 'Shop Humidity')
start_http_server(8000)

while True:

    try: 
        temp = sensor.temperature # read temperature 
        humidity = sensor.relative_humidity # read humidity
    except:
        ts = datetime.now(timezone.utc)
        ERROR = { "Timestamp" : ts.isoformat(), "Error" : "Error reading sensor, in use" }
        send_udp(json.dumps(ERROR))

    TEMP="%0.1f C" % temp
    HUM="%0.1f %%" % humidity
    temp = (temp * 1.8) + 32
    temp_g.set(temp)
    humid_g.set(humidity)
    send_udp(format_json(TEMP,HUM))

    sleep(15)