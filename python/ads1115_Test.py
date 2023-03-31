#!/usr/bin/env python3

import time, board, busio, os, errno
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)

# Create single-ended input on channel 0
# chan = AnalogIn(ads, ADS.P0)

# Create differential input between channel 0 and 1
chan0 = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)
chan2 = AnalogIn(ads, ADS.P2)
chan3 = AnalogIn(ads, ADS.P3)

while True:
    try:
        if chan1.voltage > 1:
            chState = "Not Charging"
        else:
            chState = "Charging"
        print("CH0: {:>5.3f}".format(chan0.voltage))
        print("CH1: {0:>5.3f} : {1:}".format(chan1.voltage,chState))
        print("CH2: {:>5.3f}".format(chan2.voltage))
        print("CH3: {:>5.3f}".format(chan3.voltage))
        print("")
        time.sleep(10)
    except OSError as e:
        if e.errno == 121:
            print('Caught Errno 121. Passing.')
            pass
        else:
            print('Caught an odd error: ' + str(e.strerror))
            pass