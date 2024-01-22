import time

class Switch:
    def __init__(self, Pin, active_level = 1, long_press_time_ms = 1000, press_interval_time_ms = 1000):
        # 默认高电平有效
        # 默认判定长按的阈值为1s
        # 默认连续按下间隔最长为1s
        self.pin = Pin
        self.active_level = active_level
        self.long_press_time_ms = long_press_time_ms
        self.press_interval_time_ms = press_interval_time_ms
        self.last_press_times = 1
        
        self.no_press_func = lambda: self.pass_func()  # 先将所有按下的动作函数注册为pass
        self.short_press_func = lambda: self.pass_func()
        self.double_press_func = lambda: self.pass_func()
        self.triple_press_func = lambda: self.pass_func()
        self.long_press_func = lambda: self.pass_func()
        
    def pass_func(self):
        pass
    
    def scan(self):  # 按键扫描函数
        press_times = 0  # 按下次数
        for i in range(0,3):
            if self.pin.value() == self.active_level:
                start_time_ns = time.time_ns()
                time.sleep_ms(10)  # 软件消抖延迟
                if self.pin.value() == self.active_level:
                    press_times+=1
                    
                    while self.pin.value() == self.active_level:  # 按键按下的过程
                        time.sleep_ms(100)
                        if time.time_ns()-start_time_ns >= self.long_press_time_ms*1e6:  # 按下时间超过长按阈值，判定为长按
                            long_press_flag = 1
                            self.long_press_func()
                            while self.pin.value() == self.active_level:
                                pass
                            press_times = 0  # 按下次数清零，防止同时触发短按（包括单击、双击、三击）功能
                            i = 3
                            break
                        
                    while self.pin.value() != self.active_level:  # 按键抬起后未按下的过程
                        time.sleep_ms(100)
                        if time.time_ns()-start_time_ns >= self.press_interval_time_ms*1e6:
                            i = 3  # 当按键抬起时间时间过长时，跳到按键次数判断部分
                            
                            break
            else:  # 检测到未按下立刻退出，确保每次按下时i均为1，能够正常判断按下次数
                break
        if press_times == 0:
            self.no_press_func()
        elif press_times == 1:
            self.short_press_func()
        elif press_times == 2:
            self.double_press_func()
        elif press_times == 3:
            self.triple_press_func()