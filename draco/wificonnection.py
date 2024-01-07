import network
from machine import Pin
from time import sleep


class wifiConnection(object):
    def __init__(self):
        self.ip = ""

    def init(self, WIFI_SSID:str, WIFI_PASSWD:str, led:Pin):
        self.led = led
        self.led.value(0)
        self.WIFI_SSID = WIFI_SSID
        self.WIFI_PASSWD = WIFI_PASSWD

    def connect(self):
        # Connect to WLAN
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(self.WIFI_SSID, self.WIFI_PASSWD)
        while wlan.isconnected() == False:
            print("Waiting for connection...")
            self.led.toggle()
            sleep(0.2)
        self.ip = wlan.ifconfig()[0]
        print(f"Connected on {self.ip}")
        self.led.value(1)
        return self.ip
