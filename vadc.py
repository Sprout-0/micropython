from machine import Pin, PWM, ADC  #引入ADC模块
from time import sleep

VADC_1 = ADC(Pin(15))         #定义脚为ADC脚
VADC_1.width(ADC.WIDTH_12BIT) #读取的电压转为0-4096；ADC.WIDTH_9BIT：0-511
VADC_1.atten(ADC.ATTN_11DB)   #衰减设置范围：输入电压0-3.3v

VADC_2 = ADC(Pin(16))         #定义脚为ADC脚
VADC_2.width(ADC.WIDTH_12BIT) #读取的电压转为0-4096；ADC.WIDTH_9BIT：0-511
VADC_2.atten(ADC.ATTN_11DB)   #衰减设置范围：输入电压0-3.3v

VADC_3 = ADC(Pin(17))         #定义脚为ADC脚
VADC_3.width(ADC.WIDTH_12BIT) #读取的电压转为0-4096；ADC.WIDTH_9BIT：0-511
VADC_3.atten(ADC.ATTN_11DB)   #衰减设置范围：输入电压0-3.3v

VADC_4 = ADC(Pin(18))         #定义脚为ADC脚
VADC_4.width(ADC.WIDTH_12BIT) #读取的电压转为0-4096；ADC.WIDTH_9BIT：0-511
VADC_4.atten(ADC.ATTN_11DB)   #衰减设置范围：输入电压0-3.3v



