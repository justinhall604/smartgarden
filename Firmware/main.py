import time
import board
import busio
import digitalio
import microcontroller 
from analogio import AnalogIn
import adafruit_dht
from circuitpython_nrf24l01.fake_ble import (
    chunk,
    FakeBLE,
    UrlServiceData,
    UrlServiceData,
    BatteryServiceData,
    TemperatureServiceData,
)

# Exponential Moving Average for Rain Events
# Averaged over 1 hour
g_rain_per_hour_percent = 0
collection_interval_seconds = 10
collection_counter = 0

# change these (digital output) pins accordingly
ce = digitalio.DigitalInOut(board.GP5)
csn = digitalio.DigitalInOut(board.GP1)
pin_rain = digitalio.DigitalInOut(board.GP17)
pin_rain.direction = digitalio.Direction.INPUT
pin_rain.switch_to_input(pull=digitalio.Pull.UP)

# nRF24L01 Pins and definitions
#               SCK        MOSI       MISO 
spi = busio.SPI(board.GP2, board.GP3, board.GP0)  # init spi bus object
nrf = FakeBLE(spi, csn, ce)
nrf.pa_level = -12

# analog pins
light_sensor = AnalogIn(board.GP26)
soil_sensor = AnalogIn(board.GP27)
batt_pin = AnalogIn(board.GP28)

sleep_timer = 2.0
retries = 5
samples = 1
dhtDevice = adafruit_dht.DHT11(board.GP7)

def sample_and_avg_DHT(sleep_timer, retries, samples):
    valid = 0
    invalid = 0
    temperature_c = 0
    humidity = 0
    time.sleep(2)
    while valid < samples:
        try:
            temperature_c = temperature_c + dhtDevice.temperature
            humidity = humidity + dhtDevice.humidity
            valid += 1
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            dhtDevice.exit()
            raise error
            #time.sleep(sleep_timer)
        if invalid > retries:
            return(0,0)
    return (round(temperature_c/valid, 0), round(humidity/valid,0))

def send_packet(data):
    """Send Out Advirtising Packet"""
    byteArrayObject = bytearray(data)
    byteObject = bytes(byteArrayObject)
    #ble.name = b"Garden"
    ble.mac = b"\xA5\xA5\xA5\xA5\xA5\xA5"  #Little Indian
    ble.advertise(byteObject, 0x16)
    ble.hop_channel()

print("    Garden Sensor Program Begin")

g_rain_per_hour_major = 0

while True:
    list_sensor_data = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    
    print("***LOGGING VALUES***")
    # Get SHT Temp and Humidity
    sht_temp, sht_hum = sample_and_avg_DHT(sleep_timer, retries, samples)
    # battery volatage
    batt = int(batt_pin.value / 65535 * 100)
    print("Battery Level:{}%".format(batt))
    list_sensor_data[0] = batt
    # SHT Humidity
    sht_hum = int(sht_hum)
    print("Humidity:{}%".format(sht_hum))
    list_sensor_data[1] = sht_hum
    sht_temp = int(sht_temp) 
    # Soil Moisture
    soil_moist = int(soil_sensor.value / 65535 * 100)
    print("Soil Sensor:{}%".format(soil_moist))
    list_sensor_data[2] = round(soil_moist,0)
    # SHT Temperature
    print("Temperature:{}C".format(sht_temp))
    list_sensor_data[3] = sht_temp
    # Pico Temperature
    pico_temp = int(microcontroller.cpu.temperature)
    print("Pico Temperature:{}C".format(pico_temp))
    list_sensor_data[4] = pico_temp
    
    # Light Level
    light_val = int((65535 - light_sensor.value) / 65535 * 100)
    print("Light Level:{}%".format(light_val))
    list_sensor_data[5] = int(round(light_val,0))
    
    # Rain
    if pin_rain.value: g_rain_per_hour_major = (599 * g_rain_per_hour_major) + 0
    else: g_rain_per_hour_major = (599 * g_rain_per_hour_major) + 1
    g_rain_per_hour_major = g_rain_per_hour_major / 600
    g_rain_per_hour_minor = (g_rain_per_hour_major % 1) * 100
    print("Rain Event:{} Major:{}% Minor:{}%".format(pin_rain.value,
    g_rain_per_hour_major, g_rain_per_hour_minor))
    
    # Rain Events
    list_sensor_data[6] = int(round(g_rain_per_hour_major, 0))
    list_sensor_data[7] = int(round(g_rain_per_hour_minor, 0))
        
    with nrf as ble:
        send_packet(list_sensor_data)
    time.sleep(2)