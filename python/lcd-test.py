#!/usr/bin/env python3
import I2C_LCD_driver,time,socket,fcntl,struct
# from time import *


mylcd = I2C_LCD_driver.lcd()

def getHost(ifname):
    h_name = socket.gethostname()
    IP_addres = socket.gethostbyname(h_name)
    print("Host Name is:" + h_name)
    return h_name

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def displayAll():
    locTime = time.localtime()
    print(str(locTime.tm_hour))
    if locTime.tm_hour >= 17 or locTime.tm_hour <= 5:
        print("turning it off")
        mylcd.backlight(0)
        print("done")
    else:
        print("turning it on")
        mylcd.lcd_clear()
        mylcd.backlight(0)
        mylcd.lcd_display_string("IP: " + get_ip(), 1) 
        mylcd.lcd_display_string("Hostname: " + getHost('wlan0'), 2)
        mylcd.lcd_display_string("Time: %s" %time.strftime("%H:%M"), 3)
        mylcd.lcd_display_string("Date: %s" %time.strftime("%m/%d/%Y"), 4)
        time.sleep(5)

# mylcd.lcd_display_string(get_ip_address('eth0'), 2)

def td():
    while True:
        mylcd.lcd_display_string("Time: %s" %time.strftime("%H:%M:%S"), 3)
        mylcd.lcd_display_string("Date: %s" %time.strftime("%m/%d/%Y"), 4)

if __name__ == "__main__":
    try:
        displayAll()
    except  ValueError as errVal:
        print(errVal)
        pass