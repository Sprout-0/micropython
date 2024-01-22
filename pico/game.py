from machine import Pin,I2C
from tcs34725 import TCS34725
import time

i2c = I2C(1,scl = Pin(27),sda = Pin(26),freq = 400_000)
tcs = TCS34725(i2c,0x29)
huancun = ""

while 1:
    r,g,b,c = tcs.read(True)
    print(tcs.read(True))
    time.sleep_ms(1)