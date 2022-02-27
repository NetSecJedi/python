import board
import adafruit_sht31d
from time import sleep
import logging

# Set up log file
logging.basicConfig(filename='fan.log', encoding='utf-8', level=logging.DEBUG)

# Create sensor object to read temp and humidity from SHT30
i2c = board.I2C()
sensor = adafruit_sht31d.SHT31D(i2c)

while True: 

    try: 
        temp = sensor.temperature # read temperature value 
        humidity = sensor.relative_humidity
        logging.info("Temperature: %0.1f C" % temp)
        logging.info("Humidity: %0.1f %%" % humidity)
    except:
        logging.ERROR("Error reading sensor, retrying....")

    sleep(2)