# 树莓派 Pico OLED Display Test
# Uses ssd1306 module
# display-ssd1306-test.py
 
# DroneBot Workshop 2021
# https://dronebotworkshop.com
 
import machine
import utime
 
sda=machine.Pin(2)
scl=machine.Pin(3)
 
i2c=machine.I2C(1, sda=sda, scl=scl, freq=400000)
 
from ssd1306 import SSD1306_I2C
oled = SSD1306_I2C(128, 64, i2c)
 
print(i2c.scan())


oled.fill(1)
oled.show()
utime.sleep(2)
oled.fill(0)
oled.show()
 
while True:
    oled.chinese("注意",0,0)
    oled.chinese("已锁定，请解锁",0,16)
    oled.text("Hello World",0,32)
    for i in range (0, 164):
        oled.scroll(1,0)
        oled.show()
        utime.sleep(0.01)