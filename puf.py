"""
函数：模拟PUF
功能：模拟固定长度的一串随机序列
"""
from CRC32 import crc32


# 要明确PUF的CRPs
# 32位CRC码输入进来，如何分组？
def puf():
    return crc32(beidou())


"""
函数：模拟定位模块给出的数据
参照买到的定位模块的数据格式
后续需要进行编码
"""


def beidou():
    return '03016613412000608151858269910'
