from machine import Pin
from time import sleep

led = Pin("LED", Pin.OUT)
print("Blinking LED Example")

while True:
    led.toggle()
    sleep(1)
