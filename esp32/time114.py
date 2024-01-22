from machine import Pin

coil = machine.Pin(9,machine.Pin.OUT)

time0 = machine.Timer(0) #esp32定时器 timer 0~3 ，当大于3时取余（例如timer10 ,10%4=2 ，就是timer2）

def handle_callback(timer):
    led.value( not led.value() )
    
tim0.init(period=500, mode=machine.Timer.PERIODIC, callback=handle_callback) #period 最小单位为ms
