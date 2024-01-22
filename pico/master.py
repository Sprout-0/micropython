from machine import Pin, PWM, ADC, I2C
import machine
import time
import utime
import ssd1306
import picobeep
import picovadc

i2c=I2C(1,sda=Pin(2), scl=Pin(3),freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

#interruptCounter = 0  #计数器
#totalInterruptsCounter = 0  #计算中断次数

i = 0 #是否满足发射条件，1是，0否
k = 0 #是否解锁，1是，0否
b = 0 #B按键次数
#按键输入
key = Pin(2, Pin.IN, Pin.PULL_UP) #输入模式，上拉模式
key2 = Pin(3, Pin.IN, Pin.PULL_UP) #输入模式，上拉模式

#igbt触发
coil_1 = Pin(4, Pin.OUT)
coil_2 = Pin(5, Pin.OUT)
coil_3 = Pin(6, Pin.OUT)
coil_4 = Pin(7, Pin.OUT)

#zvs开关
zvs = Pin(8, Pin.OUT)

#电磁铁
citie = Pin(10, Pin.OUT)

#激光
jiguang = Pin(11, Pin.OUT)

#光电开关
light_1 = Pin(12, Pin.IN, Pin.PULL_DOWN)
light_2 = Pin(13, Pin.IN, Pin.PULL_DOWN)
light_3 = Pin(14, Pin.IN, Pin.PULL_DOWN)
light_4 = Pin(15, Pin.IN, Pin.PULL_DOWN)

picobeep.beep_off()

def callback_1(Pin):
    #global interruptCounter
    #interruptCounter = interruptCounter+1  #执行中断时 +1
    global i
    global k
    start = utime.ticks_ms()
    while key.value()==0:
            if utime.ticks_diff(utime.ticks_ms(), start) > 1000 : 
                if i == 0: #未充电，长按充电
                    if key.value()==1 :                      
                        #zvs启动代码                 
                        print('充电中')
                        i += 1        
                elif i == 1: #已充电，长按无动作
                    if key.value()==1 :
                        print('可以发射')
                        oled.show()
                        
            elif utime.ticks_diff(utime.ticks_ms(), start) < 1000 : 
                if i == 0:  #未充电，短按无动作
                    print('请充电')                 
                elif i == 1:  #已充电，短按发射
                    if k == 1 :#B已解锁，A短按发射
                        if key.value()==1 :
                            print('发射')
                            shoot ()
                            i == 0
                    elif k == 0 :#B没有解锁，无法发射
                        if key.value()==1 :
                            print('长按B解锁')

def callback_2(Pin):
    global b
    global k
    if b == 0 :
        start1 = utime.ticks_ms()
        while key2.value()==0:  #B长按解锁/上锁
            if utime.ticks_diff(utime.ticks_ms(), start1) > 1000 :#第一次按下按钮的时间长短
                if key2.value()==1:
                    if k == 1: #上锁
                        k = 0  
                    elif k == 0: #解锁
                        k += 1                
            if utime.ticks_diff(utime.ticks_ms(), start1) < 1000 :
                if key2.value()==1:
                    start2 = utime.ticks_ms()
                    b += 1 
    if b == 1 :
        while key2.value()==0:
            if utime.ticks_diff(utime.ticks_ms(), start2) < 1000 :#第一次按下与第二次按下的时间间隔
                if key2.value()==1:
                    if b == 2:
                        jiguang.toggle()
                        b = 0
            if utime.ticks_diff(utime.ticks_ms(), start2) > 1000 :
                if key2.value()==1:
                    print('没有长按解锁，且双击超时')
                    

def shoot ():  #线圈驱动
    #coil_1.value(1)
    print ("1")
    time.sleep_ms(1000)
    #coil_1.value(0)
    time.sleep_ms(1000)
    #coil_2.value(1)
    print ("2")
    time.sleep_ms(1000)
    #coil_2.value(0)
    time.sleep_ms(1000)
    #coil_3.value(1)
    print ("3")
    time.sleep_ms(1000)
    #coil_3.value(0)
    time.sleep_ms(1000)
    print ("4")
key.irq(trigger=Pin.IRQ_FALLING, handler=callback_1)  #外部中断 ，下降沿触发 ，回到函数为callback_1
key2.irq(trigger=Pin.IRQ_FALLING, handler=callback_2)  #外部中断 ，下降沿触发 ，回到函数为callback_2

'''
while True:
    if  interruptCounter > 0:
        state = machine.disable_irq()  #停用中断
        interruptCounter = interruptCounter-1  #初始化中断
        machine.enable_irq(state)  #启用中断
        totalInterruptsCounter = totalInterruptsCounter+1  #计数值+1
        print("Interrupt has occurred: " + str(totalInterruptsCounter))
'''


while 1:
    
    picovadc.VADC_1_value = picovadc.VADC_1.read_u16()
    picovadc.VADC_2_value = picovadc.VADC_2.read_u16()
    picovadc.VADC_3_value = picovadc.VADC_3.read_u16()
    picovadc.VADC_4_value = picovadc.VADC_4.read_u16()
    time.sleep_ms(10)
