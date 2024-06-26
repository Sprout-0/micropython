import time,utime
from machine import Pin,UART
import StepperMotor

led = Pin(25,Pin.OUT)

uart1 =UART(1,baudrate = 115200,bits = 8,parity = None,stop = 1 ,tx = Pin(4),rx = Pin(5))  
uart2 =UART(0,baudrate = 115200,bits = 8,parity = None,stop = 1 ,tx = Pin(12),rx = Pin(13))
#uart3 =UART(0,baudrate = 115200,bits = 8,parity = None,stop = 1 ,tx = Pin(16),rx = Pin(17))

while True:
    StepperMotor.Real_time_location()
'''
    data1, count1 = StepperMotor.Emm_V5_Receive_Data(uart1)
    data2, count2 = StepperMotor.Emm_V5_Receive_Data(uart2)
    utime.sleep(1)
    print("UART1 Data: ", data1, " Count: ", count1)
    print("UART2 Data: ", data2, " Count: ", count2)
    
'''
'''
    # 等待返回命令，命令数据缓存在数组rxCmd上，长度为rxCount
    rxCmd, rxCount = StepperMotor.Emm_V5_Receive_Data()
    #StepperMotor.Emm_V5_Read_Sys_Params(0x01, "S_VEL") #读取系统参数
    #StepperMotor.Emm_V5_Reset_CurPos_To_Zero(0x01) #将当前位置清零
    #StepperMotor.Emm_V5_Reset_Clog_Pro(0x01) #解除堵转保护
    #StepperMotor.Emm_V5_Modify_Ctrl_Mode(0x01, True, 2)#修改控制模式
    #StepperMotor.Emm_V5_En_Control(0x01, True, False)# 为地址为0x01的电机使能，并启用多机同步
    #StepperMotor.Emm_V5_Vel_Control(0x01, 0, 1000, 50, False)#速度模式 地址为0x01，设置方向为CW，速度为1000RPM，加速度为50，无多机同步
    #StepperMotor.Emm_V5_Pos_Control(0x01, 0, 1000, 50, 2000, False, False)#位置模式 地址为0x01，设置方向为CW，速度为1000RPM，加速度为50，脉冲数为2000，相对运动，无多机同步
    #StepperMotor.Emm_V5_Stop_Now(0x01, False)#地址为0x01的电机，不启用多机同步停止
    #StepperMotor.Emm_V5_Synchronous_motion(0x01)# 执行地址为0x01的电机多机同步运动命令
    #StepperMotor.Emm_V5_Origin_Set_O(0x01, True)# 为地址为0x01的电机设置单圈回零零点位置并存储设置
    #StepperMotor.Emm_V5_Origin_Modify_Params(0x01, True, 0, 0, 2000, 30000, 300, 1500, 100, False)#修改地址为 0x01 的电机回零参数
    #Emm_V5_Origin_Interrupt(0x01)#为地址为0x01的电机发送强制中断退出回零命令  
    time.sleep(1)
'''