import servo
from machine import Pin
import math
p_1=Pin(0,Pin.OUT)
my_servo=servo.SERVO(p_1)

while True:
    my_servo.servo_writefx(degrees=0,sleep=1000)
    my_servo.servo_writefx(degrees=45,sleep=1000)
    my_servo.servo_writefx(degrees=90,sleep=1000)
    my_servo.servo_writefx(degrees=135,sleep=1000)
    my_servo.servo_writefx(degrees=180,sleep=1000)