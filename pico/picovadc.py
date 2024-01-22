from machine import Pin,PWM,ADC  #引入ADC模块
import utime


temp = ADC(4)

VADC_1 = ADC(Pin(26))
VADC_2 = ADC(Pin(27))
VADC_3 = ADC(Pin(28))
VADC_4 = ADC(Pin(29))
'''
while True:
    read_voltage = VADC_1.read_u16()*3.3/65535
    read_temp_voltage = temp.read_u16()*3.3/65535
    temperature = 27-(read_temp_voltage-0.706)/0.001721
    print("ADC voltage = {0:.3f}V \t\t temperature = {1:.3f}°C \r\n".format(read_voltage,temperature))
    utime.sleep(1)
'''

