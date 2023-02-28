from math import sqrt
from random import uniform

from fuzzy_vault import painting

r = 1000
min_dist = 1000
vault = [[8.8, 68529.51064169586], [5.5, 18115.14893192526], [2.2, 1671.4591475033424], [3.3, 4564.779102600267],
[11, 130504.55366714124], [7.7, 46763.595172516325], [6.6, 30196.129761880693], [4.4, 9808.687204786347],
[1.1, 416.76186163188737], [9.9, 96205.84164728293]]


chaff = []
max_x = max([x for [x, y] in vault])  # 限定在真实点边界范围内添加杂凑点
max_y = max([y for [x, y] in vault])


def dist(x1, y1, x2, y2, threshold):
    distance = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    if distance < threshold:
        return True
    else:
        return False


# 生成杂凑点并与真实点进行距离判断
# 经测试这一部分应该是没问题了
for i in range(10, r, 1):
    x_i = uniform(0, max_x * 1.1)
    y_i = uniform(0, max_y * 1.1)
    for rp in vault:
        f1 = False
        if not dist(x_i, y_i, rp[0], rp[1], min_dist):  # 如果不小于最小限制
            continue  # 进入与下一个真实点的距离判断，f1始终为False
        else:
            f1 = True
            break

    if not f1:
        chaff.append([x_i, y_i])
    else:
        continue

print("chaff的长度为", len(chaff))

tempx1 = []
tempy1 = []
for ch in chaff:
    tempx1.append(ch[0])
    tempy1.append(ch[1])
painting(tempx1, tempy1, 'blue')  # 整个vault的图


reg = []
j = len(chaff) - 1 # 初始化

while chaff:
    temp = chaff.pop()  # temp就是chaff[len(chaff)-1],也就是chaff的最后一位
    for c in range(0,len(chaff)):
        flag = False
        if not dist(temp[0],temp[1],chaff[c][0],chaff[c][1],min_dist):
            continue
        else:
            flag = True
            break

    if not flag:
        reg.append(temp)
    else:
        pass


print("reg里现有", reg)
print(len(reg))

tempx = []
tempy = []
for a in reg:
    tempx.append(a[0])
    tempy.append(a[1])
painting(tempx, tempy, 'red')  # 整个vault的图
