from time import sleep
from urllib.urequest import urlopen
import ntptime
import machine
from machine import Pin, Timer

# from machine import Pin, WDT

#change config2 for config.py in production
from draco.config2 import (
    WIFI_SSID,
    WIFI_PASSWD,
    MQTT_BROKER_PORT,
    MQTT_BROKER_IP,
    WATERPUMP_TOPIC,
    DRACO_HB_TOPIC,
    MQTT_CLIENT,
    WATERPUMP_PIN_OUT,
    REFILL_TANK_PIN_OUT,
    HEALTHCHECKSIO_ENABLE,
    HEALTHCHECKIO_URL,
    HEALTHCHECKIO_TIME_MS,

)
from draco.wificonnection import wifiConnection
from draco.mqtt_interface import mqttInterface


def healhbit(t):
    """method that will send a healhbith to homeassistant each 30 seconds"""
    mqtt.publish(topic=DRACO_HB_TOPIC, payload="1")

def healhchecks(t):
    """
    Method that will send a healhbith to healchecks.io each HEALTHCHECKIO_TIME_MS config variable
    for more information check it out:
    https://github.com/healthchecks/healthchecks
    """
    try:
        urlopen(HEALTHCHECKIO_URL)
    except OSError as e:
        """
        CPython used to have a socket.error exception which is now deprecated, and is an alias of OSError. In MicroPython, use OSError directly.
        """
        # Log ping failure here...
        print(f"Ping failed: {e}")


success = True
try:
    waterpump = Pin(WATERPUMP_PIN_OUT, Pin.OUT, value=0)
    refill = Pin(REFILL_TANK_PIN_OUT, Pin.OUT, value=0)
    led=Pin("LED", Pin.OUT, value=0)
    Wifi = wifiConnection()
    Wifi.init(WIFI_SSID=WIFI_SSID, WIFI_PASSWD=WIFI_PASSWD,led=led)
    sleep(0.5)
    ip = Wifi.connect()
    sleep(0.5)
    ntptime.settime()  # set the time to NTP
    mqtt = mqttInterface()
    mqtt.connectMQTT(
        client_id=MQTT_CLIENT, server=MQTT_BROKER_IP, port=MQTT_BROKER_PORT
    )
    mqtt.subscribe(topic=WATERPUMP_TOPIC)
    timer = Timer()
    timer.init(period=30000, mode=Timer.PERIODIC, callback=healhbit)
    if HEALTHCHECKSIO_ENABLE:
        timer_healthChecks = Timer()
        timer_healthChecks.init(period=HEALTHCHECKIO_TIME_MS, mode=Timer.PERIODIC, callback=healhchecks)
except Exception:
    machine.reset()

while success:
    try:
        mqtt.client.check_msg()
        if mqtt.waterPump:
            waterpump.on()
            led.on()
        else:
            waterpump.off()
            led.off()
        if False:
            #TODO: make the refill with a phisical switch and another pump
            refill.on()
        else:
            refill.off()
        sleep(1)
    except Exception:
        success = False
        waterpump.off()
        print("Error in main loop")
        mqtt.disconnect()
        machine.reset()
