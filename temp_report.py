import board
import adafruit_sht31d
from time import sleep
import logging

# Set up INFO and DEBUG log files
logging.basicConfig(filename='/home/pi/temp_hum.log', encoding='utf-8', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
err_logger = logging.getLogger()
err_logger.basicConfig(filename='/home/pi/temp_hum_err.log', encoding='utf-8', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)


# Create sensor object to read temp and humidity from SHT30
i2c = board.I2C()
sensor = adafruit_sht31d.SHT31D(i2c)

try: 
    temp = sensor.temperature # read temperature 
    humidity = sensor.relative_humidity # read humidity
except:
    err_logger.error("Error reading sensor, in use")

logging.info("Temperature: %0.1f C" % temp)
logging.info("Humidity: %0.1f %%" % humidity)
