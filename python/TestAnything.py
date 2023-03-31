#!/usr/bin/env python3
import Adafruit_DHT,time,bme280,os,errno,psutil,statistics, smbus2, datetime,ADS1115,pickle


bus = smbus2.SMBus(1)
address = 0x76
calibration_params = bme280.load_calibration_params(bus, address)



DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 24
ads = ADS1115.ADS1115()
'''
 def readADCSingleEnded(self, channel=0, pga=6144, sps=250):
         
            Gets a single-ended ADC reading from the specified channel in mV. 
            The sample rate for this mode (single-shot) can be used to lower the noise 
            (low sps) or to lower the power consumption (high sps) by duty cycling, 
            see datasheet page 14 for more info. 
            The pga must be given in mV, see page 13 for the supported values. 
'''



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

def voltStat():
    uvs = ""
    # check for undervolt status
    while uvs == "":
        uvs = os.popen('/opt/vc/bin/vcgencmd get_throttled').readline()
        time.sleep(.5)
    uvsRtn = uvs.replace("\n","")
    return uvsRtn

iterVal = 0

def volts():
    # The ADS1115 module sets the mode at 6.144V, so calculations are required to convert the mV reading to 
    # the range of the device.
    # (("reading" / 6.144) * 5) * 0.001 is where we'll start.
    # More data from the web:
    # For ADS1115, when taking a single-ended measurement:
    # Vin,0 = x / 2^15 * FS
    #
    try:
        c0v = ads.readADCSingleEnded(channel=0,pga=6144,sps=250) * 0.001
        c0v2 = c0v/.950625098
        c1v = ads.readADCSingleEnded(channel=1,pga=6144,sps=250) * 0.001
        c1v2 = c1v/.950625098
        c2v = ads.readADCSingleEnded(channel=2,pga=6144,sps=250) * 0.001
        c2v2 = c2v/.950625098
        c3v = ads.readADCSingleEnded(channel=3,pga=6144,sps=250) * 0.001
        c3v2 = c3v/.950625098
        if c1v > 1:
            chState = "Not Charging"
        else:
            chState = "Charging"
    except OSError as e:
        if e.errno == 121:
            print('Caught Errno 121. Passing.')
            c0v,c1v,c2v,c3v,c0v2,c1v2,c2v2,c3v2,chState = volts()
            pass
        else:
            print('Caught an odd error: ' + str(e.strerror))
            c0v,c1v,c2v,c3v,c0v2,c1v2,c2v2,c3v2,chState = volts()
            pass
    return c0v,c1v,c2v,c3v,c0v2,c1v2,c2v2,c3v2,chState

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

def main():
    while True:
        try:
            iterStart = time.time()
            print("\nTime: {0:}".format(time.strftime("%H:%M:%S",time.localtime())))
            humidity,tempC,temp = getDHT()
            print("DHT: TempC={0:0.1f}C  TempF={1:0.1f}F  Humidity={2:0.1f}%".format(tempC, temp, humidity))
            inBoxTemp,pressure,tstart = bme()
            iBTempF = float(9/5 * inBoxTemp + 32.00)
            print("BME: inBox={0:0.1f}F Press={1:0.2f}in/Hg".format(iBTempF,pressure * 0.0295300))
            cpuT1,cpuT2 = cpuTemp()
            uvsRtn = voltStat()
            print("OS: CPU_C={0:0.1f}C  CPU_F={1:0.1f}F {2:}".format(cpuT1,cpuT2,uvsRtn))
            c0v,c1v,c2v,c3v,c0v2,c1v2,c2v2,c3v2,chState = volts()
            print("CH0: {:>5.3f} Raw: {:5.3f}".format(c0v2,c0v))
            print("CH1: {0:>5.3f} Raw: {1:5.3f} : {2:}".format(c1v2,c1v,chState))
            print("CH2: {:>5.3f} Raw: {:5.3f}".format(c2v2,c2v))
            print("CH3: {:>5.3f} Raw: {:5.3f}".format(c3v2,c3v))
            print("Iteration: " + str(iterVal) + " elapsed time: {0:0.2f} seconds.".format((time.time() - iterStart)))
            iterVal = iterVal + 1
            if iterVal >= 5:
                print("CPU useage: ", psutil.cpu_percent(4) )
                iterVal = 0
        except OSError as e:
            print(e)
            pass

