from machine import Pin, PWM, ADC, SoftI2C
import machine
import time
import utime
import ssd1306
import beep
import vadc
i2c = SoftI2C(scl=Pin(1),sda=Pin(0))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

#interruptCounter = 0  #计数器
#totalInterruptsCounter = 0  #计算中断次数

s = 0 #是否充电,1是，0否
i = 0 #是否满足发射条件，1是，0否
b = 0 #发射计数

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

beep.beep_off()

def callback_1(Pin):
    #global interruptCounter
    #interruptCounter = interruptCounter+1  #执行中断时 +1
    global s 
    global i 
    start = utime.ticks_ms()
    while key.value()==0:
            if utime.ticks_diff(utime.ticks_ms(), start) > 1000 : 
                if i == 0: #未充电，长按充电
                    if key.value()==1 :
                        s = 1
                        oled.clear()
                        oled.chinese("充电中",0,0)
                        oled.show()
                        time.sleep(3)
                        oled.clear()
                        oled.chinese("充电完毕",0,0)
                        print(vadc.VADC_1_value)
                        oled.show()
                        i += 1
                elif i == 1: #已充电，长按无动作
                    if key.value()==1 :
                        s = 0
                        oled.clear()
                        oled.chinese("电力充足",0,0)
                        oled.chinese("短按发射",0,16)
                        print(vadc.VADC_1_value)
                        oled.show()
            elif utime.ticks_diff(utime.ticks_ms(), start) < 1000 : 
                if i == 0:  #未充电，短按无动作
                    if key.value()==1 :
                        s = 0
                        oled.clear()
                        oled.chinese("电压过低",0,0)
                        oled.chinese("长按充电",0,16)
                        print(vadc.VADC_1_value)
                        oled.show()
                        beep.warning()
                elif i == 1:  #已充电，短按发射
                    if key.value()==1 :
                        
                        oled.clear()
                        oled.chinese("中中中中中中",0,0)
                        print(vadc.VADC_1_value)
                        oled.show()
                        beep.shooting()
                        shoot ()
                        i -= 1
                        
def shoot ():  #线圈驱动
    global b
    #coil_1.value(1)
    print("1")
    time.sleep_ms(1000)
    #coil_1.value(0)
    time.sleep_ms(1000)
    #coil_2.value(1)
    print("2")
    time.sleep_ms(1000)
    #coil_2.value(0)
    time.sleep_ms(1000)
    #coil_3.value(1)
    print("3")
    time.sleep_ms(1000)
    #coil_3.value(0)
    time.sleep_ms(1000)
    print ("已经一滴不剩了")
    b += 1
    
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
    
    vadc.VADC_1_value = vadc.VADC_1.read()
    time.sleep_ms(10)
    vadc.VADC_2_value = vadc.VADC_2.read()
    time.sleep_ms(10)
    vadc.VADC_3_value = vadc.VADC_3.read()
    time.sleep_ms(10)
    vadc.VADC_4_value = vadc.VADC_4.read()
    time.sleep_ms(10)
