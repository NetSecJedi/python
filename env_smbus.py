import board
import smbus
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

# Create smbus sensor object to read temp and humidity from SHT30
bus = smbus.SMBus(1)

# Set up Prometheus Gauges and metrics http server
temp_g = Gauge('sdr_temp_gauge', 'SDR Enc Temperature')
humid_g = Gauge('sdr_hum_gauge', 'SDR Enc Humidity')
start_http_server(8000)

while True:

    try: 
        # SHT31 address, 0x44(68)
        bus.write_i2c_block_data(0x44, 0x2C, [0x06]) # write to SHT31 address 0x44(68)
        # SHT31 address, 0x44(68)
        # Read data back from 0x00(00), 6 bytes after half a second
        # Temp MSB, Temp LSB, Temp CRC, Humididty MSB, Humidity LSB, Humidity CRC
        sleep(0.5)
        data = bus.read_i2c_block_data(0x44, 0x00, 6)
    except:
        ts = datetime.now(timezone.utc)
        ERROR = { "Timestamp" : ts.isoformat(), "Error" : "Error reading sensor, in use" }
        send_udp(json.dumps(ERROR))

    i2c_temp = data[0] * 256 + data[1]
    #ctemp = -45 + (175 * i2c_temp / 65535.0)
    ftemp = -49 + (315 * i2c_temp / 65535.0)
    humidity = 100 * (data[3] * 256 + data[4]) / 65535.0
    TEMP="%0.1f C" % ftemp
    HUM="%0.1f %%" % humidity
    temp_g.set(ftemp)
    humid_g.set(humidity)
    send_udp(format_json(TEMP,HUM))

    sleep(60)