from crcmod import *

import gpio
import serial
import time

rs_control = 6
gpio.setup(rs_control, 'out')  # TR Pin


def crc16_maxim(read):
    r = bytes(bytearray(read))
    crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
    crc_hex = hex(crc16(r))
    crc = divmod(int(crc_hex, 16), 0x100)
    return [crc[1], crc[0]]


if __name__ == '__main__':
    r = [31, 3, 0, 0, 0, 2]
    rs_crc = crc16_maxim(r)
    full_rs = r + rs_crc
    print(full_rs)  # [31, 3, 0, 0, 0, 2, 199, 181]
    py_serial = serial.Serial("/dev/ttyS1", baudrate=9600, timeout=0.5, writeTimeout=0.5, bytesize=8, parity='N', stopbits=1, rtscts=True, dsrdtr=True)
    read_count = full_rs[5] * 2 + 5  # 計算接收字數
    gpio.set(rs_control, 1)  # RS485 切換成 out 送出
    py_serial.write(full_rs)  # 寫入資料
    # py_serial.flush()
    time.sleep(0.001 * (len(full_rs)))  # 計算寫入等待時間 字數*鮑率
    gpio.set(rs_control, 0)  # RS485 切換成 in 接收
    read_data = b''
    while 1:
        r = py_serial.read()
        read_data += r
        if len(r) == 0:
            break
        else:
            py_serial.timeout = 0.001 * 10
    print(list(read_data))  # [31, 3, 4, 0, 25, 0, 25, 20, 63]
