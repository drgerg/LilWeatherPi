#!/usr/bin/env python3
import Adafruit_DHT,time,bme280,os,errno,psutil,statistics, smbus2, datetime,pickle


bus = smbus2.SMBus(1)
address = 0x76
calibration_params = bme280.load_calibration_params(bus, address)

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 24

def bme(): 
    tstart = time.time()
    data = bme280.sample(bus,address,calibration_params)
    inBoxTemp = data.temperature
    pressure = data.pressure
    return inBoxTemp,pressure,tstart

def cpuTemp():
    ct = ""
    # Return CPU temperature in C and F
    while ct == "":
        ct = os.popen('vcgencmd measure_temp').readline()
        time.sleep(.5)

    cpuRtn = ct.replace("temp=","").replace("'C\n","")
    cpuT1=float(cpuRtn)
    cpuT2=float(9/5 * cpuT1 + 32.00)
    return cpuT1,cpuT2

def getDHT():
        humidity = None
        tempC = None
        temp = None
        while humidity == None or tempC == None:
            try:
                humidity, tempC = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
                temp = float(9/5 * tempC + 32.00)
            except:
                pass
            time.sleep(2)
        return humidity,tempC,temp

def envStats():
    taHome = os.path.abspath(os.path.dirname(__file__))
    humidity,tempC,temp = getDHT()
    inBoxTemp,pressure,tstart = bme()
    cpuTC,cpuTF = cpuTemp()
    lwpStats = {"lwph":humidity,"lwpt":temp,"lwpp":pressure,"lwpc":cpuTF}
    with open(taHome + '/LilWPEnvStats.pkl', 'wb') as lwpOut:
        pickle.dump(lwpStats,lwpOut, pickle.HIGHEST_PROTOCOL)
    print("Environmental Stats are pickled.")



