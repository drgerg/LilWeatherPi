#!/usr/bin/env python3
import Adafruit_DHT,time
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 24
while True:
    time.sleep(3)
    humidity, tempC = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and tempC is not None:
        temp = float(9/5 * tempC + 32.00)
        print("TempC={0:0.1f} TempF={1:0.1f}  Humidity={2:0.1f}%".format(tempC, temp, humidity))
    else:
        print("Failed to retrieve data from humidity sensor")



# print('Temperature: {} degrees C'.format(sensor.temperature)) 
# print('Pressure: {}hPa'.format(sensor.pressure))