import machine
import time

class W25QXX:
    # W25QXX命令
    CMD_READ_ID = 0x9F
    CMD_READ_STATUS_REG1 = 0x05
    CMD_WRITE_STATUS_REG1 = 0x01
    CMD_READ_DATA = 0x03
    CMD_FAST_READ_DATA = 0x0B
    CMD_WRITE_ENABLE = 0x06
    CMD_SECTOR_ERASE = 0x20
    CMD_BLOCK_ERASE_32K = 0x52
    CMD_BLOCK_ERASE_64K = 0xD8
    CMD_CHIP_ERASE = 0xC7
    CMD_PAGE_PROGRAM = 0x02

    def __init__(self, spi, cs_pin, size_mb=16):
        self.spi = spi
        self.cs_pin = cs_pin
        self.size_mb = size_mb
        self.cs = machine.Pin(cs_pin, machine.Pin.OUT)

        self._size_in_bytes = size_mb * 1024 * 1024
        self._sector_size = 4 * 1024
        self._block_size_32k = 32 * 1024
        self._block_size_64k = 64 * 1024

    def _cs_low(self):
        self.cs.value(0)

    def _cs_high(self):
        self.cs.value(1)

    def _send_command(self, command, data=None, response_length=0):
        self._cs_low()
        self.spi.write(bytearray([command]))
        if data:
            self.spi.write(data)
        response = self.spi.read(response_length)
        self._cs_high()
        return response

    def _wait_busy(self):
        while True:
            status = self._send_command(W25QXX.CMD_READ_STATUS_REG1, response_length=1)
            if not status[0] & 0x01:
                break
            time.sleep_ms(1)

    def read_id(self):
        response = self._send_command(W25QXX.CMD_READ_ID, response_length=3)
        return tuple(response)

    def read_status_register(self):
        status = self._send_command(W25QXX.CMD_READ_STATUS_REG1, response_length=1)
        return status[0]

    def write_status_register(self, value):
        self._send_command(W25QXX.CMD_WRITE_STATUS_REG1, data=bytearray([value]))

    def read_data(self, address, length):
        data = self._send_command(W25QXX.CMD_READ_DATA, data=bytearray([address >> 16, address >> 8, address & 0xFF]), response_length=length)
        return data

    def write_enable(self):
        self._send_command(W25QXX.CMD_WRITE_ENABLE)

    def erase_sector(self, sector_address):
        self.write_enable()
        self._send_command(W25QXX.CMD_SECTOR_ERASE, data=bytearray([sector_address >> 16, sector_address >> 8, sector_address & 0xFF]))
        self._wait_busy()

    def erase_block_32k(self, block_address):
        self.write_enable()
        self._send_command(W25QXX.CMD_BLOCK_ERASE_32K, data=bytearray([block_address >> 16, block_address >> 8, block_address & 0xFF]))
        self._wait_busy()

    def erase_block_64k(self, block_address):
        self.write_enable()
        self._send_command(W25QXX.CMD_BLOCK_ERASE_64K, data=bytearray([block_address >> 16, block_address >> 8, block_address & 0xFF]))
        self._wait_busy()

    def erase_chip(self):
        self.write_enable()
        self._send_command(W25QXX.CMD_CHIP_ERASE)
        self._wait_busy()

    def program_page(self, address, data):
        self.write_enable()
        self._send_command(W25QXX.CMD_PAGE_PROGRAM, data=bytearray([address >> 16, address >> 8, address & 0xFF]) + data)
        self._wait_busy()

# 使用示例
spi = machine.SPI(1, baudrate=1000000, polarity=0, phase=0)
cs_pin = 5  # 请替换为您实际使用的CS引脚
flash = W25QXX(spi, cs_pin)

# 读取ID
id = flash.read_id()
print("Flash ID:", id)

# 读取状态寄存器
status = flash.read_status_register()
print("Status Register:", status)

# 擦除扇区
sector_address = 0x000000
flash.erase_sector(sector_address)
print("Sector Erased")

# 写入数据
data_to_write = bytearray([0xAA, 0xBB, 0xCC, 0xDD, 0xEE])
flash.program_page(sector_address, data_to_write)
print("Data Written")

# 读取数据
read_data = flash.read_data(sector_address, len(data_to_write))
print("Read Data:", read_data)
