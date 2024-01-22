from machine import Pin
import time
import utime
import _thread

key = Pin(0, Pin.IN, Pin.PULL_DOWN) #输入模式，下拉模式
led1 = Pin(25, Pin.OUT)
led = Pin(13, Pin.OUT)

press = 0
active_level = 1
long_press_time_ms = 1000
press_interval_time_ms = 1000

def run_on_core1():#线程程序测试
    while True:
        led1.value(1)
        time.sleep(0.5)
        led1.value(0)
        time.sleep(0.5)

def main():#主线程
        led.value(1)
        time.sleep(0.5)
        led.value(0)
        time.sleep(0.5)
     
def callback_1(Pin):
    global press
    print ('按键中断启动')
    time.sleep_ms(10)  # 软件消抖延迟
    if key.value()==active_level:
        start = utime.ticks_ms() #开始计时
        while key.value()==active_level: #按键按下不抬起
            if utime.ticks_diff(utime.ticks_ms(), start) > long_press_time_ms : #计算按下时长
                #运行长按程序？
                print('长按')
                if key.value()==active_level:
                    break
            
        while key.value() != active_level:  # 按键抬起后未继续按下的过程
            Double_click = utime.ticks_ms()
            if utime.ticks_diff(utime.ticks_ms(), start) > press_interval_time_ms : #计算松开时长
                if key.value()!=active_level:
                    print('单击')
                    break
               
    else:
        pass
    print ('按键中断关闭')
    
key.irq(trigger=Pin.IRQ_RISING, handler=callback_1)  #外部中断 ，上升沿触发 ，回到函数为callback_1
_thread.start_new_thread(run_on_core1, ( ))


if __name__ == '__main__':
    while True:
        main()
