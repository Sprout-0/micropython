from machine import Pin
from machine import PWM
import time
import utime


pwm = PWM(Pin(11))
pwm.deinit()


key = Pin(0, Pin.IN, Pin.PULL_DOWN) #输入模式，下拉模式



def main():#主线程
    pwm.duty_u16(32768)
    for i in range(300,540,20):
        time.sleep(1)
        pwm.freq(i)  #频率，单位Hz
        print(i)
        if i == 600:
           i = 300

def callback_1(Pin):
    time.sleep_ms(10)  # 软件消抖延迟
    if key.value()==1:
        print ('按键中断启动')
        pwm.freq(500)  #频率，单位Hz
        pwm.duty_u16(32768)
        time.sleep(5)
        print ('按键中断退出')
key.irq(trigger=Pin.IRQ_RISING, handler=callback_1)  #外部中断 ，上升沿触发 ，回到函数为callback_1

if __name__ == '__main__':
    while True:
        main()
