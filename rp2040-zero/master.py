from machine import Pin, PWM, ADC, I2C ,UART
import ustruct
import machine
import time
import utime
import ssd1306
import picobeep
import picovadc

uart =UART(1,baudrate = 115200,bits = 8,parity = None,stop = 1 ,tx = Pin(8),rx = Pin(9))  #无线串口传输数据
i2c=I2C(1,sda=Pin(2), scl=Pin(3),freq=400000) # i2c oled屏
oled = ssd1306.SSD1306_I2C(128, 64, i2c)


i = 0 #是否满足发射条件，1是，0否
k = 0 #是否解锁，1是，0否
b = 0 #B按键次数
start2 = 0 #双击计时器

#定时器0~4，测量四个线圈的加速
rank_1 = 0
rank_2 = 0
rank_3 = 0
rank_4 = 0

first_time = 0
second_time = 0
third_time = 0
fourth_time = 0
#按键输入
key = Pin(0, Pin.IN, Pin.PULL_UP) #输入模式，上拉模式
key2 = Pin(1, Pin.IN, Pin.PULL_UP) #输入模式，上拉模式

#igbt触发
coil_1 = Pin(4, Pin.OUT)
coil_2 = Pin(5, Pin.OUT)
coil_3 = Pin(6, Pin.OUT)
coil_4 = Pin(7, Pin.OUT)

#zvs开关
#zvs = Pin(8, Pin.OUT)
zvs = PWM(Pin(8))
zvs.deinit()


def zvs_control(pin_lv,zhan_kong_bi) : 
    zvs.freq(pin_lv)  #频率，单位Hz
    zvs.duty_u16(zhan_kong_bi)  # 设定PWM的占空比，取值范围0~65535， 而32768大约是一半，也就是50%
    
                   

#电磁铁
citie = Pin(10, Pin.OUT)

#激光
jiguang = Pin(11, Pin.OUT)

#光电开关
light_1 = Pin(12, Pin.IN, Pin.PULL_DOWN)
light_2 = Pin(13, Pin.IN, Pin.PULL_DOWN)
light_3 = Pin(14, Pin.IN, Pin.PULL_DOWN)
light_4 = Pin(15, Pin.IN, Pin.PULL_DOWN)

#picobeep.beep_off()

#全光电模式
'''
def callback_light_1(Pin):
    global rank_1
    global rank_2
    global first_time
    global second_time
    coil_1.value(0)
    first_time = utime.ticks_diff(utime.ticks_ms(), rank_1)
    coil_2.value(1)
    print ("rank_2")
    rank_2 = utime.ticks_ms()

def callback_light_2(Pin):
    global rank_2
    global rank_3
    global second_time
    coil_2.value(0)
    second_time = utime.ticks_diff(utime.ticks_ms(), rank_2)
    coil_3.value(1)
    print ("rank_3")
    rank_3 = utime.ticks_ms()

def callback_light_3(Pin):
    global rank_3
    global rank_4
    global third_time
    coil_3.value(0)
    third_time = utime.ticks_diff(utime.ticks_ms(), rank_3)
    coil_4.value(1)
    print ("rank_4")
    rank_4 = utime.ticks_ms()
    
def callback_light_4(Pin):
    global rank_4
    global fourth_time
    coil_4.value(0)
    fourth_time = utime.ticks_diff(utime.ticks_ms(), rank_4)
'''

#时开光关模式
'''
def callback_light_1(Pin):
    global rank_1
    global rank_2
    global first_time
    coil_1.value(0)
    first_time = utime.ticks_diff(utime.ticks_ms(), rank_1)
    rank_2 = utime.ticks_ms()

def callback_light_2(Pin):
    global rank_2
    global rank_3
    global second_time
    coil_2.value(0)
    second_time = utime.ticks_diff(utime.ticks_ms(), rank_2)
    rank_3 = utime.ticks_ms()

def callback_light_3(Pin):
    global rank_3
    global rank_4
    global third_time
    coil_3.value(0)
    third_time = utime.ticks_diff(utime.ticks_ms(), rank_3)
    rank_4 = utime.ticks_ms()
    
def callback_light_4(Pin):
    global rank_4
    global fourth_time
    coil_4.value(0)
    fourth_time = utime.ticks_diff(utime.ticks_ms(), rank_4)

def time_on_light_off_mode():
    coil_1.value(1)
    print ("rank_1")
    time.sleep_ms(1000)
    coil_2.value(1)
    print ("rank_2")
    time.sleep_ms(1000)
    coil_3.value(1)
    print ("rank_3")
    time.sleep_ms(1000)
    coil_4.value(1)
    print ("rank_4")
'''
#全时序控制模式
def callback_light_1(Pin):
    global rank_1
    global rank_2
    global first_time
    first_time = utime.ticks_diff(utime.ticks_ms(), rank_1)
    rank_2 = utime.ticks_ms()

def callback_light_2(Pin):
    global rank_2
    global rank_3
    global second_time
    second_time = utime.ticks_diff(utime.ticks_ms(), rank_2)
    rank_3 = utime.ticks_ms()

def callback_light_3(Pin):
    global rank_3
    global rank_4
    global third_time
    third_time = utime.ticks_diff(utime.ticks_ms(), rank_3)
    rank_4 = utime.ticks_ms()
    
def callback_light_4(Pin):
    global rank_4
    global fourth_time
    fourth_time = utime.ticks_diff(utime.ticks_ms(), rank_4)

def all_time_mode (): 
    time.sleep_ms(1000)
    coil_1.value(0)
    time.sleep_ms(1000)
    coil_2.value(1)
    print ("rank_2")
    time.sleep_ms(1000)
    coil_2.value(0)
    time.sleep_ms(1000)
    coil_3.value(1)
    print ("rank_3")
    time.sleep_ms(1000)
    coil_3.value(0)
    time.sleep_ms(1000)
    print ("rank_4")
    
    
def callback_1(Pin):
    global i
    global k
    global rank_1
    start = utime.ticks_ms()
    while key.value()==0:
            if utime.ticks_diff(utime.ticks_ms(), start) > 1000 : 
                if i == 0: #未充电，长按充电
                    if k == 1:
                        if key.value()==1 :    #此处以下都没加按键防抖，zvs充电没加pid                
                            #zvs启动代码
                            if picovadc.VADC_1.read_u16()*443/65535 < 50 : #电压下限 50
                                zvs_control(10000,4000)
                                print('充电中')
                                oled.fill(0)
                                oled.chinese("充电中",0,0)
                                oled.show()
                                time.sleep(1) #充电时间1秒
                                zvs_control(0,0)
                                if picovadc.VADC_1.read_u16()*443/65535 > 100 : #电压上限 100
                                    zvs_control(0,0)
                                    print('电力充足')
                                    oled.fill(0)
                                    oled.chinese("电力充足",0,0)
                                    oled.show()
                                i = 1  
                elif i == 1: #已充电，长按无动作
                    if k == 1:
                        if key.value()==1 :
                            print('可以发射')
                            oled.fill(0)
                            oled.chinese("请短按发射",0,0)
                            oled.show()
                            
            elif utime.ticks_diff(utime.ticks_ms(), start) < 1000 : 
                if i == 0:  #未充电，短按无动作
                    if k == 1:
                        if key.value()==1 :
                            print('请充电')
                            picobeep.warning2()
                            oled.fill(0)
                            oled.chinese("请长按充电",0,0)
                            oled.show()
                    if k == 0:
                        if key.value()==1 :
                            picobeep.warning()
                            print('长按B解锁')
                            oled.fill(0)
                            oled.chinese("长按解锁",0,0)
                            oled.show()
                        
                elif i == 1:  #已充电，短按发射
                    if k == 1 :#B已解锁，A短按发射
                        if key.value()==1 :
                            i = 0
                            print('发射')
                            rank_1 = utime.ticks_ms()
                            print ("rank_1")
                            oled.fill(0)
                            oled.chinese("发射",0,0)
                            oled.show()
                            picobeep.warning()
                            #此处写发射函数
                            
                            #此处写发射函数
                            
                    elif k == 0 :#B没有解锁，无法发射
                        if key.value()==1 :
                            picobeep.warning()
                            print('长按B解锁')
                            oled.fill(0)
                            oled.chinese("长按解锁",0,0)
                            oled.show()
def callback_2(Pin):
    global b
    global k
    global start2
    if b == 0 :
        start1 = utime.ticks_ms()
        while key2.value()==0:  #B长按解锁/上锁
            if utime.ticks_diff(utime.ticks_ms(), start1) > 1000 :#第一次按下按钮的时间长短
                if key2.value()==1:
                    if k == 1: #上锁
                        k = 0
                        print('上锁')
                        oled.fill(0)
                        oled.chinese("已锁定",0,0)
                        oled.show()
                    elif k == 0: #解锁
                        k += 1
                        print('解锁')
                        oled.fill(0)
                        oled.chinese("已解锁",0,0)
                        oled.show()
            if utime.ticks_diff(utime.ticks_ms(), start1) < 1000 :
                if key2.value()==1:
                    start2 = utime.ticks_ms()
                    b = 1
                    print('连击次数1')
                    
    if b == 1 :
        while key2.value()==0:
            if utime.ticks_diff(utime.ticks_ms(), start2) < 1000 :#第一次按下与第二次按下的时间间隔
                if key2.value()==1:
                    if b == 1:
                        print('连击次数2')
                        print('翻转激光电平')
                        oled.fill(0)
                        oled.chinese("翻转激光电平",0,0)
                        oled.show()
                        b = 0
                    

    
key.irq(trigger=Pin.IRQ_FALLING, handler=callback_1)  #外部中断 ，下降沿触发 ，回到函数为callback_1
key2.irq(trigger=Pin.IRQ_FALLING, handler=callback_2) 

light_1.irq(trigger=Pin.IRQ_RISING, handler=callback_light_1) #外部中断 ，上升沿触发 ，回到函数为callback_light_1
light_2.irq(trigger=Pin.IRQ_RISING, handler=callback_light_2)
light_3.irq(trigger=Pin.IRQ_RISING, handler=callback_light_3)
light_4.irq(trigger=Pin.IRQ_RISING, handler=callback_light_4)



while 1:

    if b == 1 :
        if utime.ticks_diff(utime.ticks_ms(), start2) > 1000 :
            b = 0
            print('归零')
'''
    VADC_1_value = picovadc.VADC_1.read_u16()*443/65535 #443v电容电压模拟量细分65535份
    VADC_2_value = picovadc.VADC_2.read_u16()*443/65535
    VADC_3_value = picovadc.VADC_3.read_u16()*443/65535
    VADC_4_value = picovadc.VADC_4.read_u16()*443/65535
    temperature = picovadc.temp.read_u16()*3.3/65535 #内部温度传感器，电压0~3.3v模拟量细分65535份
    data = bytearray(16)
    ustruct.pack_into('<ffff', data, 0, VADC_1_value, VADC_2_value, VADC_3_value, VADC_4_value)
    uart.write(data)
    tail = bytearray([0x00, 0x00, 0x80, 0x7f])
    uart.write(tail)
    print("ADC1 = {0:.0f} \nADC2 = {1:.0f} \nADC3 = {2:.0f} \nADC4 = {3:.0f} \ntemperature = {4:.0f}" .format(VADC_1_value,VADC_2_value,VADC_3_value,VADC_4_value,temperature)) #{0:.3f}其中 0 代表format(0,1,2,3,4)中数值位置 .3f表示三位小数
    time.sleep_ms(1)
 '''