from machine import Pin, UART
import time

uart3 = UART(0, baudrate=115200, bits=8, parity=None, stop=1, tx=Pin(16), rx=Pin(17))
colors = ['green', 'red']  # 定义颜色列表

# 初始化坐标存储变量
latest_coords = {'green': None, 'red': None}

def Coordinate_Receive():
    data = ""
    while True:
        if uart3.any() > 0:
            data += uart3.read().decode()  # 读取数据并解码为字符串
            if "\n" in data:  # 如果数据中有换行符，表示一条消息的结束
                message = data[:data.index("\n")]  # 提取一条完整的消息
                color, x_coord, y_coord = message.split()  # 分割消息
                x_coord, y_coord = float(x_coord), float(y_coord)  # 转换坐标为浮点数
                print(f"{color} {x_coord} {y_coord}")
                latest_coords[color] = (x_coord, y_coord)  # 更新最新的坐标
                data = data[data.index("\n")+1:]  # 移除已处理的消息
        else:  # 串口没有数据
            time.sleep_ms(100)  # 没有数据时，稍微延迟一下，减少CPU使用率
    return latest_coords  # 返回最新的坐标

while True:
    latest_coords = Coordinate_Receive()
    print(f"The latest coordinates of the green object are {latest_coords['green']}")
    print(f"The latest coordinates of the red object are {latest_coords['red']}")
    time.sleep_ms(10)
