import socket
import network
from time import sleep

from secrets import WIFI_NAME, WIFI_PASS

ssid = WIFI_NAME
password = WIFI_PASS

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print(f'Connecting to SSID: {ssid}\n')
        print('Waiting for connection...')

        sleep(5)
        wlan.connect(ssid, password)
        
    print("Connected on:")
    print(wlan.ifconfig())


connect()
