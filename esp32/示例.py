import machine
interruptCounter = 0#与主程序通信
totalInterruptsCounter = 0#计算中断事件次数
def callback(pin):#定义回调函数
  global interruptCounter#声明为全局变量
  interruptCounter = interruptCounter+1
p25 = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)#引脚编号、引脚模式下降沿以及是否存在相关拉电阻
p25.irq(trigger=machine.Pin.IRQ_FALLING, handler=callback)#触发中断，回调模式
while True:
  if interruptCounter>0:
    state = machine.disable_irq()#禁用计数器
    interruptCounter = interruptCounter-1
    machine.enable_irq(state)#重新启动计数器
    totalInterruptsCounter = totalInterruptsCounter+1
    print("Interrupt has occurred: " + str(totalInterruptsCounter))
