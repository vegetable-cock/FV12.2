from numpy import char

from puf import beidou
from CRC32 import crc32
temp = []
temp1 = crc32(beidou())  #temp1是32位的字符串
for i in range(0,28):
    temp.append(temp1[i:i+4])

def get_num(str):
    a = 8*int(str[0])+4*int(str[1])+2*int(str[2])+1*int(str[3])
    return a

print(temp)
print(list(map(get_num,temp)))

