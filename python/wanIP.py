#!/usr/bin/env python3

import upnpclient

devices = upnpclient.discover()
print(devices)

if(len(devices) > 0):
    d = devices[0]
    extStat = d.WANIPConn1.GetStatusInfo()
    #externalIP = d.WANIPConn1.GetExternalIPAddress()
    #print(externalIP)
    print(extStat)
else:
    print('No Connected network interface detected')

