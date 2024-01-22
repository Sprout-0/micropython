from machine import UART ,Pin
import utime
import math
import ustruct
import picovadc

#uart =UART(0,baudrate = 115200,bits = 8,parity = None,stop = 1 ,tx = Pin(0),rx = Pin(1))
uart =UART(1,baudrate = 115200,bits = 8,parity = None,stop = 1 ,tx = Pin(8),rx = Pin(9))

key = Pin(2, Pin.IN, Pin.PULL_UP) #输入模式，上拉模式
coil_1 = Pin(10, Pin.OUT)


def callback_light_1(Pin):
    utime.sleep(0.1)
    if key.value() == 0:
        
        coil_1.value(1)
        utime.sleep_ms(500)
        coil_1.value(0)
        utime.sleep_ms(500)
        print ("rank_1")



key.irq(trigger=Pin.IRQ_FALLING, handler=callback_light_1)
  
while True:
    VADC_1_value = picovadc.VADC_1.read_u16()*443/65535 #443v电容电压模拟量细分65535份
    VADC_2_value = picovadc.VADC_2.read_u16()*443/65535
    VADC_3_value = picovadc.VADC_3.read_u16()*443/65535
    VADC_4_value = picovadc.VADC_4.read_u16()*443/65535
    
    data = bytearray(16)
    ustruct.pack_into('<ffff', data, 0, VADC_1_value, VADC_2_value, VADC_3_value, VADC_4_value)
    uart.write(data)
    tail = bytearray([0x00, 0x00, 0x80, 0x7f])
    uart.write(tail)
    
    count = uart.any() #接收
    if count > 0:
        read = uart.read(count)
        print(read)
    utime.sleep_ms(50)

