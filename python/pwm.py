#!/usr/bin/env python3
# import time,os,logging,signal,sys,argparse,pickle
import time,argparse
from time import sleep
import RPi.GPIO as GPIO

parserPWM = argparse.ArgumentParser()
parserPWM.add_argument("-d", "--debug", help="Turn on debugging output to log file.", action="store_true")
parserPWM.add_argument("-p", "--pwm", help="Set the PWM dutycycle.", action="store")

argsPWM = parserPWM.parse_args()

if argsPWM.pwm:
    pVar = int(argsPWM.pwm)
    # logging.debug("PWM set to : " + str(pVar))
    print("PWM set to: " + str(pVar))
else:
    pVar = 100

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# GPIO 23 set up as input. It is pulled up to stop false signals
#GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.OUT)  # Set GPIO pin 18 to output mode.
fanPwm = GPIO.PWM(18, 100)   # Initialize PWM on fanPwm @ specified frequency in hz
fanPwm.start(pVar)

while pVar > 0:
    print('Set new pVar: ')
    pVar = int(input())
    fanPwm.ChangeDutyCycle(pVar)
    print('PWM duty cycle is now ' + str(pVar) + '.')

print("Cleaning up")
GPIO.cleanup()
