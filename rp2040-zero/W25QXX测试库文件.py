import machine
import time

class W25QXX:
    def __init__(self, spi, cs_pin):
        self.spi = spi
        self.cs_pin = cs_pin
        self.cs = machine.Pin(cs_pin, machine.Pin.OUT)

    def _cs_low(self):
        self.cs.value(0)

    def _cs_high(self):
        self.cs.value(1)

    def _send_command(self, command):
        self._cs_low()
        self.spi.write(bytearray([command]))
        self._cs_high()

    def read_data(self, address, length):
        self._cs_low()
        self.spi.write(bytearray([0x03, (address >> 16) & 0xFF, (address >> 8) & 0xFF, address & 0xFF]))
        data = self.spi.read(length)
        self._cs_high()
        return data

    def write_data(self, address, data):
        self._cs_low()
        self.spi.write(bytearray([0x02, (address >> 16) & 0xFF, (address >> 8) & 0xFF, address & 0xFF]))
        self.spi.write(data)
        self._cs_high()

    def erase_sector(self, sector_address):
        self._cs_low()
        self.spi.write(bytearray([0x20, (sector_address >> 16) & 0xFF, (sector_address >> 8) & 0xFF, sector_address & 0xFF]))
        self._cs_high()

# 使用示例
spi = machine.SPI(1, baudrate=1000000, polarity=0, phase=0)
cs_pin = 5  # 请替换为您实际使用的CS引脚
flash = W25QXX(spi, cs_pin)

# 读取数据
address = 0x000000
data = flash.read_data(address, 10)
print("Read data:", data)

# 写入数据
data_to_write = bytearray([0xAA, 0xBB, 0xCC, 0xDD, 0xEE])
flash.write_data(address, data_to_write)
print("Data written")

# 擦除扇区
sector_address_to_erase = 0x000000
flash.erase_sector(sector_address_to_erase)
print("Sector erased")
