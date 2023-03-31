#!/usr/bin/env python3
#
## wxDisplay.py - Retrieve and display weather data provided by Brilliant.
## 2021 - Gregory A. Sanders - dr.gerg@drgerg.com
#
import I2C_LCD_driver,time
#,socket,fcntl,struct
# from time import *


mylcd = I2C_LCD_driver.lcd()

def main(**wxData):
    locTime = time.localtime()
    if locTime.tm_hour >= 21 or locTime.tm_hour <= 5:
        mylcd.backlight(0)
    else:
        mylcd.lcd_clear()
        mylcd.lcd_display_string("T: " + wxData['outTemp'] + chr(223),1,0)
        mylcd.lcd_display_string("| ",1,9)
        mylcd.lcd_display_string("H: " + wxData['outHumidity'] + "%",1,11)
        mylcd.lcd_display_string("W: " + wxData['windSpeed'],2,0)
        mylcd.lcd_display_string("| ",2,9)
        mylcd.lcd_display_string("G: " + wxData['windGust'],2,11)
        mylcd.lcd_display_string("D: "+ wxData['winddir'],3,0)
        mylcd.lcd_display_string("| ",3,9)
        mylcd.lcd_display_string("B: " + wxData['pressNA'],3,11)
        mylcd.lcd_display_string("R: " + wxData['inchRain'],4,0)
        mylcd.lcd_display_string("| ",4,9)
        mylcd.lcd_display_string("P: " + wxData['ptIn'] + chr(223),4,11)

#
## SCROLL FROM RIGHT TO LEFT CONTINUOUSLY
#
# str_pad = " " * 16
# my_long_string = "This is a string that needs to scroll"
# my_long_string = str_pad + my_long_string

# while True:
#     for i in range (0, len(my_long_string)):
#         lcd_text = my_long_string[i:(i+16)]
#         mylcd.lcd_display_string(lcd_text,1)
#         sleep(0.4)
#         mylcd.lcd_display_string(str_pad,1)
