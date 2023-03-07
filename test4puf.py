from numpy import char

from puf import beidou
from CRC32 import crc32
temp = []
temp1 = crc32(beidou())  #temp1是32位的字符串
print("temp1=",temp1)
for i in range(0,24):
    temp.append(temp1[i:i+8])

def get_num(str):
    a = 128*int(str[0])+64*int(str[1])+32*int(str[2])+16*int(str[3])\
    +8*int(str[4])+4*int(str[5])+2*int(str[6])+1*int(str[7])
    return a

print("temp=",temp)
print(list(map(get_num,temp)))
print("横坐标的位数为：",len(list(map(get_num,temp))))



