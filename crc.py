from crcmod import *


def crc16_maxim(read):
    r = bytes(bytearray(read))
    crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
    crc_hex = hex(crc16(r))
    crc = divmod(int(crc_hex, 16), 0x100)
    return [crc[1], crc[0]]


if __name__ == '__main__':
    r = [1, 3, 0, 0, 0, 2]
    rs_crc = crc16_maxim(r)
    full_rs = r + rs_crc
    print(full_rs)  # [1, 3, 0, 0, 0, 2, 196, 11]
