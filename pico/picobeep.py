from machine import Pin
from machine import PWM
import time

'''
tones = {'_1':262,'_1#':277,'_2':294,'_2#':311,'_3':330,'_4':349,'_4#':370,'_5':392,'_5#':415,'_6':440,'_6#':466,'_7':494,
         '1':523,'1#':554,'2':587,'2#':622,'3':689,'4':698,'4#':740,'5':784,'5#':831,'6':880,'6#':932,'7':988,
         '1_':523,'1_#':554,'2_':587,'2_#':622,'3_':689,'4_':698,'4_#':740,'5_':784,'5_#':831,'6_':880,'6_#':932,'7':988,'-':0}
melody = "123"

delays = [100,200,400,800,]
'''
pwm = PWM(Pin(9))
pwm.deinit()
'''
def music_beep():
    pwm.init()
    pwm.freq(1)
    pwm.duty(512)
    for tone in melody:
        freq = tones[tone]
        if freq:
            pwm.init(duty=512, freq=freq)  # 调整PWM的频率，使其发出指定的音调
        else:pwm.duty(0)
        for i in range(1, len(melody)):
        time.sleep_ms(delays)
        pwm.duty(0)
        time.sleep_ms(50)
        '''
def beep_on():
    pwm.freq(4000)  #频率，单位Hz
    pwm.duty_u16(32768)  # 设定PWM的占空比，取值范围0~65535， 而32768大约是一半，也就是50%
     
def beep_off():
    pwm.freq(4000)  #频率，单位Hz
    pwm.duty_u16(0)  
def warning():
    beep_on()
    time.sleep_ms(200)
    beep_off()
    time.sleep_ms(100)
    beep_on()
    time.sleep_ms(200)
    beep_off()
    time.sleep_ms(100)
def shooting():
    beep_on()
    time.sleep_ms(50)
    beep_off()
    time.sleep_ms(50)
    beep_on()
    time.sleep_ms(50)
    beep_off()
    time.sleep_ms(50)
    beep_on()
    time.sleep_ms(50)
    beep_off()
    time.sleep_ms(50)
    beep_on()
    time.sleep_ms(50)
    beep_off()
    time.sleep_ms(50)
    beep_on()
    time.sleep_ms(50)
    beep_off()
    time.sleep_ms(50)
    beep_on()
    time.sleep_ms(50)
    beep_off()
    time.sleep_ms(50)
    beep_on()
    time.sleep_ms(50)
    beep_off()
    time.sleep_ms(50)
    beep_on()
    time.sleep_ms(50)
    beep_off()
    time.sleep_ms(50)
'''    
while 1:
    warning()
'''