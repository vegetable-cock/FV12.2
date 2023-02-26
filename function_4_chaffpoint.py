from math import sqrt
from random import uniform

from fuzzy_vault import painting

r = 40
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


for i in range(10, r):
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

print(chaff)
print(len(chaff))
-
tempx1 = []
tempy1 = []
for ch in chaff:
    tempx1.append(ch[0])
    tempy1.append(ch[1])
painting(tempx1, tempy1, 'blue')  # 整个vault的图

# print(dist(chaff[0][0],chaff[0][1],chaff[1][0],chaff[1][1],min_dist))
reg = []
# 现在index out of range的原因是内循环乘外循环大于390，即chaff点数时就超过
# 也就是说后面的删除把所有项都删除了
i = len(chaff) - 2
while chaff:
    temp = chaff.pop()
    try:
        while i != 0:
            flag = False
            i = i - 1
            if dist(temp[0], temp[1], chaff[i][0], chaff[i][1], min_dist):  # 如果距离小于最小限制
                break
            else:
                flag = True
                continue

        if flag:
            reg.append(temp)
    except:
        pass
print("chaff里还剩", chaff)
print("reg里现有", reg)
print(len(reg))

tempx = []
tempy = []
for a in reg:
    tempx.append(a[0])
    tempy.append(a[1])
painting(tempx, tempy, 'red')  # 整个vault的图
