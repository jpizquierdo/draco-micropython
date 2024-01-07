import mip
from machine import Pin
from time import sleep
from draco.config2 import (
    WIFI_SSID,
    WIFI_PASSWD,
)
from draco.wificonnection import wifiConnection
led=Pin("LED", Pin.OUT, value=0)
Wifi = wifiConnection()
Wifi.init(WIFI_SSID=WIFI_SSID, WIFI_PASSWD=WIFI_PASSWD, led=led)
sleep(0.5)
ip = Wifi.connect()
sleep(0.5)
mip.install("umqtt.simple")
