import board
import adafruit_sht31d
import adafruit_shtc3
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

def format_json(TEMP,HUM,SERVICE):
    ts = datetime.now(timezone.utc)
    jsonstr = { "Timestamp" : ts.isoformat(), "Service" : SERVICE, "Temperature" : TEMP, "Humidity" : HUM }
    return json.dumps(jsonstr)

# Create sensor objects to read temp and humidity from SHT sensors
i2c = board.I2C()
sdr_sensor = adafruit_sht31d.SHT31D(i2c) # SHT31D Sensor located inside SDR Enclosure
#attic_sensor = adafruit_shtc3.SHTC3(i2c) # SHTC3 Sensor exposed to attic cavity

# Set up Prometheus Gauges and metrics http server
sdr_temp_g = Gauge('sdr_temp_gauge', 'SDR Enclosure Temperature')
sdr_humid_g = Gauge('sdr_hum_gauge', 'SDR Enclosure Humidity')
#attic_temp_g = Gauge('attic_temp_gauge', 'Attic Temperature')
#attic_humid_g = Gauge('attic_hum_gauge', 'Attic Enclosure Humidity')
start_http_server(8000)

while True:

    try: 
        # Read SDR SHT31C Sensor
        sdr_temp = sdr_sensor.temperature # read temperature 
        sdr_humidity = sdr_sensor.relative_humidity # read humidity
        sleep(.5)
        #Read Attic Sensor
        #attic_temp, attic_relh = attic_sensor.measurements

    except:
        ts = datetime.now(timezone.utc)
        ERROR = { "Timestamp" : ts.isoformat(), "Error" : "Error reading sensor, in use" }
        send_udp(json.dumps(ERROR))

    # SDR Enclosure environment processing
    TEMP="%0.1f C" % sdr_temp
    HUM="%0.1f %%" % sdr_humidity
    SERVICE="SDR"
    temp = (sdr_temp * 1.8) + 32
    sdr_temp_g.set(temp)
    sdr_humid_g.set(sdr_humidity)
    send_udp(format_json(TEMP,HUM,SERVICE))

    # Attic environment processing
    #TEMP="%0.1f C" % attic_temp
    #HUM="%0.1f %%" % attic_relh
    #SERVICE="ATTIC"
    #temp = (attic_temp * 1.8) + 32
    #attic_temp_g.set(temp)
    #attic_humid_g.set(attic_relh)
    #send_udp(format_json(TEMP,HUM,SERVICE))

    sleep(59.5)