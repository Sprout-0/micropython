import time
from machine import Pin,UART

def ABS(x):
    return x if x > 0 else -x

# 初始化LED灯
led_pin = Pin(25, Pin.OUT)
led_pin.value(0)  # 将LED灯关闭
# 初始化串口
uart =UART(1,baudrate = 115200,bits = 8,parity = None,stop = 1 ,tx = Pin(4),rx = Pin(5))  #无线串口传输数据
#uart1 =UART(0,baudrate = 115200,bits = 8,parity = None,stop = 1 ,tx = Pin(12),rx = Pin(13))


class SysParams:
    S_VER = 0      # 读取固件版本和对应的硬件版本
    S_RL = 1       # 读取读取相电阻和相电感
    S_PID = 2      # 读取PID参数
    S_VBUS = 3     # 读取总线电压
    S_CPHA = 5     # 读取相电流
    S_ENCL = 7     # 读取经过线性化校准后的编码器值
    S_TPOS = 8     # 读取电机目标位置角度
    S_VEL = 9      # 读取电机实时转速
    S_CPOS = 10    # 读取电机实时位置角度
    S_PERR = 11    # 读取电机位置误差角度
    S_FLAG = 13    # 读取使能/到位/堵转状态标志位
    S_Conf = 14    # 读取驱动参数
    S_State = 15   # 读取系统状态参数
    S_ORG = 16     # 读取正在回零/回零失败状态标志位


def Emm_V5_Read_Sys_Params(addr, s): #调用函数读取系统参数
    cmd = bytearray(16)

    # 装载命令
    i = 0
    cmd[i] = addr
    i += 1

    # 功能码
    if s == "S_VER":
        cmd[i] = 0x1F
    elif s == "S_RL":
        cmd[i] = 0x20
    elif s == "S_PID":
        cmd[i] = 0x21
    elif s == "S_VBUS":
        cmd[i] = 0x24
    elif s == "S_CPHA":
        cmd[i] = 0x27
    elif s == "S_ENCL":
        cmd[i] = 0x31
    elif s == "S_TPOS":
        cmd[i] = 0x33
    elif s == "S_VEL":
        cmd[i] = 0x35
    elif s == "S_CPOS":
        cmd[i] = 0x36
    elif s == "S_PERR":
        cmd[i] = 0x37
    elif s == "S_FLAG":
        cmd[i] = 0x3A
    elif s == "S_ORG":
        cmd[i] = 0x3B
    elif s == "S_Conf":
        cmd[i] = 0x42
        i += 1
        cmd[i] = 0x6C
    elif s == "S_State":
        cmd[i] = 0x43
        i += 1
        cmd[i] = 0x7A

    i += 1
    cmd[i] = 0x6B  # 校验字节

    # 发送命令
    uart.write(cmd[:i+1])

    
def Emm_V5_Reset_CurPos_To_Zero(addr): #将当前位置清零
    cmd = bytearray(4)
    
    cmd[0] =  addr                         # 地址
    cmd[1] =  0x0A                          # 功能码
    cmd[2] =  0x6D                          # 辅助码
    cmd[3] =  0x6B                          # 校验字节
    
    uart.write(cmd)
    
def Emm_V5_Reset_Clog_Pro(addr): #解除堵转保护
    cmd = bytearray(4)

    cmd[0] =  addr                         # 地址
    cmd[1] =  0x0E                          # 功能码
    cmd[2] =  0x52                          # 辅助码
    cmd[3] =  0x6B                          # 校验字节
  
    # 发送命令
    uart.write(cmd)


def Emm_V5_Modify_Ctrl_Mode(addr, svF, ctrl_mode):#调用函数修改控制模式
    # 定义命令数组
    cmd = bytearray(6)
    
    # 装载命令
    cmd[0] = addr          # 地址
    cmd[1] = 0x46          # 功能码
    cmd[2] = 0x69          # 辅助码
    cmd[3] = 0x01 if svF else 0x00  # 是否存储标志, 1为存储, 0为不存储
    cmd[4] = ctrl_mode     # 控制模式
    cmd[5] = 0x6B          # 校验字节
    
    # 发送命令
    uart.write(cmd)        # 使用UART发送命令


def Emm_V5_En_Control(addr, state, snF):# 为地址为0x01的电机使能，并启用多机同步
    # 定义命令数组，使用字节数组，大小为 16
    cmd = bytearray(16)
    
    # 装载命令
    cmd[0] = addr               # 地址
    cmd[1] = 0xF3               # 功能码
    cmd[2] = 0xAB               # 辅助码
    cmd[3] = 0x01 if state else 0x00  # 使能状态，true为0x01，false为0x00
    cmd[4] = 0x01 if snF else 0x00    # 多机同步运动标志，true为0x01，false为0x00
    cmd[5] = 0x6B               # 校验字节
    
    # 发送命令, 只发送前6个字节
    uart.write(cmd[:6])


def Emm_V5_Vel_Control(addr, dir, vel, acc, snF):# 地址为0x01的电机，设置方向为CW，速度为1000RPM，加速度为50，无多机同步
    # 定义命令数组，使用字节数组，大小为 16
    cmd = bytearray(16)
    
    # 装载命令
    cmd[0] = addr                  # 地址
    cmd[1] = 0xF6                  # 功能码
    cmd[2] = dir                   # 方向，0为CW，其余值为CCW
    cmd[3] = (vel >> 8) & 0xFF     # 速度(RPM)高8位字节
    cmd[4] = vel & 0xFF            # 速度(RPM)低8位字节
    cmd[5] = acc                   # 加速度，注意：0是直接启动
    cmd[6] = 0x01 if snF else 0x00 # 多机同步运动标志，true为0x01，false为0x00
    cmd[7] = 0x6B                  # 校验字节
    
    # 发送命令, 只发送前8个字节
    uart.write(cmd[:8])


def Emm_V5_Pos_Control(addr, dir, vel, acc, clk, raF, snF):# 地址为0x01的电机，设置方向为CW，速度为1000RPM，加速度为50，脉冲数为2000，相对运动，无多机同步
    # 定义命令数组，使用字节数组，大小为 16
    cmd = bytearray(16)
    
    # 装载命令
    cmd[0] = addr                      # 地址
    cmd[1] = 0xFD                      # 功能码
    cmd[2] = dir                       # 方向
    cmd[3] = (vel >> 8) & 0xFF         # 速度(RPM)高8位字节
    cmd[4] = vel & 0xFF                # 速度(RPM)低8位字节 
    cmd[5] = acc                       # 加速度，注意：0是直接启动
    cmd[6] = (clk >> 24) & 0xFF        # 脉冲数高8位字节(bit24 - bit31)
    cmd[7] = (clk >> 16) & 0xFF        # 脉冲数(bit16 - bit23)
    cmd[8] = (clk >> 8) & 0xFF         # 脉冲数(bit8  - bit15)
    cmd[9] = clk & 0xFF                # 脉冲数低8位字节(bit0  - bit7)
    cmd[10] = 0x01 if raF else 0x00    # 相位/绝对标志，true为0x01，false为0x00
    cmd[11] = 0x01 if snF else 0x00    # 多机同步运动标志，true为0x01，false为0x00
    cmd[12] = 0x6B                     # 校验字节
    
    # 发送命令, 只发送前13个字节
    uart.write(cmd[:13])


def Emm_V5_Stop_Now(addr, snF):#地址为0x01的电机，不启用多机同步停止
    # 定义命令数组，使用字节数组，大小为 5（实际发送的大小）
    cmd = bytearray(5)
    
    # 装载命令
    cmd[0] = addr               # 地址
    cmd[1] = 0xFE               # 功能码
    cmd[2] = 0x98               # 辅助码
    cmd[3] = 0x01 if snF else 0x00  # 多机同步运动标志，true为0x01，false为0x00
    cmd[4] = 0x6B               # 校验字节
    
    # 发送命令
    uart.write(cmd)


def Emm_V5_Synchronous_motion(addr):# 执行地址为0x01的电机多机同步运动命令
    # 定义命令数组，使用字节数组，大小为 4（实际发送的大小）
    cmd = bytearray(4)
    
    # 装载命令
    cmd[0] = addr               # 地址
    cmd[1] = 0xFF               # 功能码
    cmd[2] = 0x66               # 辅助码
    cmd[3] = 0x6B               # 校验字节
    
    # 发送命令
    uart.write(cmd)


def Emm_V5_Origin_Set_O(addr, svF):# 为地址为0x01的电机设置单圈回零零点位置并存储设置
    # 定义命令数组，使用字节数组，大小为 5（实际发送的大小）
    cmd = bytearray(5)
    
    # 装载命令
    cmd[0] = addr               # 地址
    cmd[1] = 0x93               # 功能码
    cmd[2] = 0x88               # 辅助码
    cmd[3] = 0x01 if svF else 0x00  # 是否存储标志，true为0x01，false为0x00
    cmd[4] = 0x6B               # 校验字节
    
    # 发送命令
    uart.write(cmd)

def Emm_V5_Origin_Modify_Params(addr, svF, o_mode, o_dir, o_vel, o_tm, sl_vel, sl_ma, sl_ms, potF): #修改地址为 0x01 的电机回零参数
    # 定义命令数组，使用字节数组，大小合适即可（根据命令结构确定）
    cmd = bytearray(20)
    
    # 装载命令
    cmd[0] = addr                             # 地址
    cmd[1] = 0x4C                             # 功能码
    cmd[2] = 0xAE                             # 辅助码
    cmd[3] = 0x01 if svF else 0x00            # 是否存储标志，true为0x01，false为0x00
    cmd[4] = o_mode                           # 回零模式
    cmd[5] = o_dir                            # 回零方向
    cmd[6] = (o_vel >> 8) & 0xFF              # 回零速度高8位字节
    cmd[7] = o_vel & 0xFF                     # 回零速度低8位字节
    cmd[8] = (o_tm >> 24) & 0xFF              # 回零超时时间高8位字节
    cmd[9] = (o_tm >> 16) & 0xFF              # 回零超时时间次高8位字节
    cmd[10] = (o_tm >> 8) & 0xFF              # 回零超时时间次低8位字节
    cmd[11] = o_tm & 0xFF                     # 回零超时时间低8位字节
    cmd[12] = (sl_vel >> 8) & 0xFF            # 无限位碰撞检测转速高8位字节
    cmd[13] = sl_vel & 0xFF                   # 无限位碰撞检测转速低8位字节
    cmd[14] = (sl_ma >> 8) & 0xFF             # 无限位碰撞检测电流高8位字节
    cmd[15] = sl_ma & 0xFF                    # 无限位碰撞检测电流低8位字节
    cmd[16] = (sl_ms >> 8) & 0xFF             # 无限位碰撞检测时间高8位字节
    cmd[17] = sl_ms & 0xFF                    # 无限位碰撞检测时间低8位字节
    cmd[18] = 0x01 if potF else 0x00          # 上电自动触发回零，true为0x01，false为0x00
    cmd[19] = 0x6B                            # 校验字节
    
    # 发送命令
    uart.write(cmd)


def Emm_V5_Origin_Trigger_Return(addr, o_mode, snF): #触发地址为0x01的电机回零，回零模式为0，不启用多机同步标志
    # 定义命令数组
    cmd = bytearray(5)
    
    # 装载命令
    cmd[0] = addr                            # 地址
    cmd[1] = 0x9A                            # 功能码
    cmd[2] = o_mode                          # 回零模式
    cmd[3] = 0x01 if snF else 0x00           # 多机同步运动标志，true为0x01，false为0x00
    cmd[4] = 0x6B                            # 校验字节
    
    # 发送命令
    uart.write(cmd)


def Emm_V5_Origin_Interrupt(addr): #为地址为0x01的电机发送强制中断退出回零命令
    cmd = bytearray(4)
    cmd[0] = addr      # 地址
    cmd[1] = 0x9C      # 功能码
    cmd[2] = 0x48      # 辅助码
    cmd[3] = 0x6B      # 校验字节
    
    uart.write(cmd)

'''
#方案一
def Emm_V5_Receive_Data(): #接收数据
    rxCmd = bytearray()       # 初始化接收数据的数组
    MAX_LENGTH = 128          # 定义最大接收长度，以防止数组溢出
    TIMEOUT = 100             # 设置超时时间（毫秒）
    start_time = time.ticks_ms()  # 记录当前时间

    # 开始接收数据
    while True:
        if uart.any() > 0:    # 检查串口中是否有数据
            new_byte = uart.read(1)  # 读取1字节数据
            if len(rxCmd) < MAX_LENGTH:
                rxCmd.extend(new_byte)  # 将接收到的数据追加到数组
                start_time = time.ticks_ms()  # 更新最后接收到数据的时间
        else:
            # 检查是否超时
            if time.ticks_diff(time.ticks_ms(), start_time) > TIMEOUT:
                break  # 如果超时，则结束数据接收

    rxCount = len(rxCmd)  # 接收到的数据长度
    return rxCmd, rxCount  # 返回接收到的数据和数据长度
    
#方案二
def Emm_V5_Receive_Data():
    rxCmd = bytearray()  # 初始化接收数组
    last_time = utime.ticks_ms()  # 记录初始时间

    while True:
        if uart.any() > 0:  # 串口有数据可读
            if len(rxCmd) < 128:  # 防止数组溢出
                rxCmd.append(uart.read(1))  # 读取一个字节数据

            last_time = utime.ticks_ms()  # 更新读取到数据的时间戳
        else:
            current_time = utime.ticks_ms()  # 获取当前时间戳
            if utime.ticks_diff(current_time, last_time) > 100:  # 100毫秒内没有数据
                break  # 接收完成，退出循环
    # 返回收到的数据和数据长度
    return rxCmd, len(rxCmd)

# 在你的主程序中，使用以下方式调用：
# received_data, received_count = Emm_V5_Receive_Data()
# print("Received data:", received_data)
# print("Count of received data:", received_count)

#方案三
def Emm_V5_Receive_Data():
    rxCmd = bytearray(128)  # 创建一个字节数组，长度128
    rxCount = 0
    lTime = utime.ticks_ms()  # 获取当前时间（毫秒）

    while True:
        if uart.any() > 0:  # 有新数据可读
            if rxCount < 128:  # 防止字节数组溢出
                rxCmd[rxCount] = uart.read(1)[0]  # 读一个字节数据
                rxCount += 1
                lTime = utime.ticks_ms()  # 更新上次接收数据的时间
        else:  # 无新数据
            cTime = utime.ticks_ms()  # 再次获取当前时间
            if utime.ticks_diff(cTime, lTime) > 100:  # 如果100ms内没有接收到数据
                break  # 结束函数执行并返回结果

    return (rxCmd[:rxCount], rxCount)  # 返回接收到的数据和数据长度

# 使用函数
data, count = emm_v5_receive_data()
print(data, count)

'''
#位置模式示例
while True:
    # 定义接收数据数组、接收数据长度
    rxCmd, rxCount = [], 0

    # 位置模式：地址为0x01的电机，设置方向0CW/1CCW，速度RPM，加速度，脉冲数，绝1/相0对运动，无多机同步
    Emm_V5_Pos_Control(1, 0, 100, 20, 0, 1, 0)

    # 等待返回命令，命令数据缓存在数组rxCmd上，长度为rxCount
    rxCmd, rxCount = Emm_V5_Receive_Data()

    #Emm_V5_Read_Sys_Params(0x01, "S_VEL") #读取系统参数
    #Emm_V5_Reset_CurPos_To_Zero(0x01) #将当前位置清零
    #Emm_V5_Reset_Clog_Pro(0x01) #解除堵转保护
    #Emm_V5_Modify_Ctrl_Mode(0x01, True, 2)#修改控制模式
    #Emm_V5_En_Control(0x01, True, False)# 为地址为0x01的电机使能，并启用多机同步
    #Emm_V5_Vel_Control(0x01, 0, 1000, 50, False)#速度模式 地址为0x01，设置方向为CW，速度为1000RPM，加速度为50，无多机同步
    #Emm_V5_Pos_Control(0x01, 0, 1000, 50, 2000, False, False)#位置模式 地址为0x01，设置方向为CW，速度为1000RPM，加速度为50，脉冲数为2000，相对运动，无多机同步
    #Emm_V5_Stop_Now(0x01, False)#地址为0x01的电机，不启用多机同步停止
    #Emm_V5_Synchronous_motion(0x01)# 执行地址为0x01的电机多机同步运动命令
    #Emm_V5_Origin_Set_O(0x01, True)# 为地址为0x01的电机设置单圈回零零点位置并存储设置
    #Emm_V5_Origin_Modify_Params(0x01, True, 0, 0, 2000, 30000, 300, 1500, 100, False)#修改地址为 0x01 的电机回零参数
    #Emm_V5_Origin_Trigger_Return(0x01, 0, False)#触发地址为0x01的电机回零，回零模式为0，不启用多机同步标志
    #Emm_V5_Origin_Interrupt(0x01)#为地址为0x01的电机发送强制中断退出回零命令
    
    # 打印接收到的数据到控制台（根据实际情况进行调整）
    print('接收数据数组:', rxCmd)
    print('接收数据长度:', rxCount)

    # 停止条件
    break  # 如果需要不断循环，请注释掉这一行

    time.sleep(1)
    
    
'''
#读取实时位置示例
while True:
    pos = 0.0
    Motor_Cur_Pos = 0.0
    rxCmd = bytearray(128)
    rxCount = 0

    Emm_V5_Pos_Control(1, 0, 1000, 0, 3200, 0, 0)

    # 这里假设驱动器会回复数据到串口
    rxCount = Emm_V5_Receive_Data(rxCmd, 128)

    if rxCount > 0 and rxCmd[rxCount - 1] == 0x6B:
        led_builtin.value(1)
    else:
        led_builtin.value(0)

    utime.sleep_ms(2000)

    Emm_V5_Read_Sys_Params(1, 'S_CPOS')
    
    rxCount = Emm_V5_Receive_Data(rxCmd, 128)

    if rxCount == 8 and rxCmd[0] == 1 and rxCmd[1] == 0x36:
        led_builtin.value(1)
        position_data = rxCmd[2:6]
        pos = int.from_bytes(position_data, 'big' if rxCmd[2] > 0 else 'little')
        Motor_Cur_Pos = pos * 360.0 / 65536.0
        if rxCmd[2]:
            Motor_Cur_Pos = -Motor_Cur_Pos
    else:
        led_builtin.value(0)

    # 用print来代替Arduino中的Serial.println
    print("Motor Current Position:" , Motor_Cur_Pos)

    utime.sleep_ms(2000)
'''
    
'''
#读取实时转速
while True:
    # 定义实时转速变量
    vel = 0.0 # 浮点型
    Motor_Vel = 0.0 # 浮点型

    # 定义接收数据数组、接收数据长度
    rxCmd = bytearray(128) # byte数组
    rxCount = 0 # integer型

    # 速度模式：方向CW，速度1000RPM，加速度0（不使用加减速直接启动）
    Emm_V5_Vel_Control(1, 0, 1000, 0, 0)

    # 等待返回命令，命令数据缓存在数组rxCmd上，长度为rxCount
    Emm_V5_Receive_Data(rxCmd, rxCount)

    # 验证校验字节，验证成功则点亮LED灯，否则熄灭LED灯
    if rxCmd[rxCount - 1] == 0x6B:
        led.value(1)
    else:
        led.value(0)

    # 延时1秒，等待转速到达
    utime.sleep(1)

    # 读取电机实时转速
    Emm_V5_Read_Sys_Params(1, 'S_VEL')

    # 等待返回命令，命令数据缓存在数组rxCmd上，长度为rxCount
    Emm_V5_Receive_Data(rxCmd, rxCount)

    # 校验地址、功能码、返回数据长度，验证成功则点亮LED灯，否则熄灭LED灯
    if rxCmd[0] == 1 and rxCmd[1] == 0x35 and rxCount == 6:
        led.value(1)
        # 拼接成uint16_t类型数据
        vel = (rxCmd[3] << 8) | rxCmd[4]
        # 实时转速
        Motor_Vel = vel
        # 检查是否有符号位
        if rxCmd[2]:
            Motor_Vel = -Motor_Vel
    else:
        led.value(0)

    # 调试使用，打印电机实时转速
    print("Motor Velocity: {:.1f} RPM".format(Motor_Vel))
'''