#!/usr/bin/env python3
#   outBgFan.py - Manage the 4-Wire Delta Electronics KDB050510HB recycled laptop cooling fan.
#                 This is intended to run as a standalone service to manage the speed of the fan based on the 
#                 CPU temperature.
#     Copyright (c) 2019,2020 - Gregory Allen Sanders.

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.

import time,os,logging,signal,sys,argparse
from time import sleep
import RPi.GPIO as GPIO

parserBGF = argparse.ArgumentParser()
parserBGF.add_argument("-d", "--debug", help="Turn on debugging output to log file.", action="store_true")
parserBGF.add_argument("-t", "--temperature", help="Set the temp to this value for testing.", action="store")
BGFHome = os.getcwd()
logger = logging.getLogger(__name__)
argsBGF = parserBGF.parse_args()
#
if argsBGF.debug:
    import traceback
    logging.basicConfig(filename=BGFHome + '/BGFan.log', format='[%(name)s]:%(levelname)s: %(message)s. - %(asctime)s', datefmt='%D %H:%M:%S', level=logging.DEBUG)
    logger.info(" - - - - Starting Up - - - - - - - - - Starting Up - - - - - - - ")
    logging.info("Debugging output enabled")
else:
    logging.basicConfig(filename=BGFHome + '/BGFan.log', format='%(asctime)s - %(message)s : %(name)s.', datefmt='%a, %d %b %Y %H:%M:%S', level=logging.INFO)
    logger.info(" - - - - Starting Up - - - - - - - - - Starting Up - - - - - - - ")
#    #

if argsBGF.temperature:
    dTemp = float(argsBGF.temperature)
    logging.debug("Debug temp set to: " + str(dTemp))
else:
    dTemp = 60

logger.info("  INITIAL CONFIGURATION COMPLETE  ")
logger.info("'HOME' path is: " + BGFHome)

dc = 60                  ## setting the first dutyCycle value here gets the fan spinning no matter what.

logger.info('dc initial value set to: ' + str(dc) + '.')
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)  # Set GPIO pin 18 to output mode.
fanPwm = GPIO.PWM(18, 100)   # Initialize PWM on fanPwm @ specified frequency in hz
fanPwm.start(dc)

elapse = 0
# pElapse = 0
lastDc = dc
def main(lastDc):
#   Grab CPU temp and set fan accordingly
    if argsBGF.temperature:
        cpuRtn = str(dTemp)
    else:
        ct = os.popen('vcgencmd measure_temp').readline()
        cpuRtn = ct.replace("temp=","").replace("'C\n","")
    temp1=float(cpuRtn)
    if temp1 < 30.0:
        dc=0
    if temp1 >= 30 and temp1 <= 40:
        dc=10
    if temp1 > 40 and temp1 <= 50:
        dc=20
    if temp1 > 50 and temp1 <= 60:
        dc=30
    if temp1 > 60 and temp1 <= 62:
        dc=40
    if temp1 > 62 and temp1 <= 65:
        dc=50
    if temp1 > 65 and temp1 <= 67:
        dc=70
    if temp1 > 67 and temp1 <= 68:
        dc=90
    if temp1 > 68:
        dc=100
    fanPwm.ChangeDutyCycle(dc)
    logger.debug('CPU: ' + cpuRtn + '. dc set to ' + str(dc))
    return lastDc, dc, temp1


def SignalHandler(signal, frame):
        logger.info("SignalHandler invoked. dc=" + str(dc))
        logger.info(" - - - - - - - - - - - - - - - - - - - - - ")
        logger.info("Cleaning up")
        GPIO.cleanup()
        logger.debug("Finished GPIO.cleanup() in SignalHandler")
        logger.info("Shutting down gracefully")
        logger.debug("Wrote to log in SignalHandler")
        logger.info("Finished SignalHandler")
        logger.info("That's all folks.  Goodbye")
        print("Exiting.")
        sys.exit(0)

if __name__ == "__main__":
        import traceback
        try:
            signal.signal(signal.SIGINT, SignalHandler)  ## This one catches CTRL-C from the local keyboard
            signal.signal(signal.SIGTERM, SignalHandler) ## This one catches the Terminate signal from the system
            logger.info(" Top of try")
            while True:
                lastDc,dc,temp1 = main(lastDc)
                if lastDc != dc:
                    print('CPU temp: ' + str(temp1) + '. dc changed to: ' + str(dc))
                    logger.info('CPU temp: ' + str(temp1) + '. dc changed to: ' + str(dc))
                lastDc = dc
                sleep(10)
            pass

            logger.info("Bottom of try")
            logger.flush()
        except Exception:
            error = traceback.print_exc()
            logger.debug(error)
            logger.info("That's all folks.  Goodbye")
            pass
