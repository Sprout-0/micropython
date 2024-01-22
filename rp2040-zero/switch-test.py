from switch import Switch
from machine import Pin
import time
 
switch = Switch(Pin(0, Pin.IN, Pin.PULL_DOWN))  # 时间参数均采用默认值，
last_num = 1
def my_print(num):
    global last_num
    if num != 0 or last_num != 0:  # 避免连续打印0刷屏
        print(num)
    last_num = num
# 按键未按下、单击、双击、三击、长按分别输出0~5
switch.no_press_func = lambda: my_print(0)
switch.short_press_func = lambda: my_print(1)
switch.doble_press_func = lambda: my_print(2)
switch.triple_press_func = lambda: my_print(3)
switch.long_press_func = lambda: my_print(4)
while True:
    switch.scan()
    time.sleep(0.01)
 