from math import sqrt
from random import uniform

'''****************************************************************************
函数dist:判断两点之间的最小距离
输入：x1,y1,x2,y2,最小距离阈值threshold
返回值：小于最小距离，则返回True；大于最小距离，返回False
****************************************************************************'''


def dist(x1, y1, x2, y2, threshold):
    distance = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    if distance < threshold:
        return True
    else:
        return False


'''****************************************************************************
函数add_chaff:添加杂凑点，实现杂凑点与真实点、杂凑点之间的最小距离限制
输入：
p_num: 初始生成的杂凑点的数量
real_point：真实点集
min_dist:最小距离限制
t:PUF响应的点数
返回值：列表chaff,存放有已经调制过的杂凑点
****************************************************************************'''


def add_chaff(p_num, t, real_point, min_dist):
    chaff = []
    max_x = max([x for [x, y] in real_point])  # 限定在真实点边界范围内添加杂凑点
    max_y = max([y for [x, y] in real_point])

    for i in range(t, p_num, 1):
        x_i = round(uniform(0, max_x * 1.1))
        y_i = round(uniform(0, max_y * 1.1))
        for rp in real_point:
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

    reg = []
    j = len(chaff) - 1  # 初始化

    while chaff:
        temp = chaff.pop()  # temp就是chaff[len(chaff)-1],也就是chaff的最后一位
        for c in range(0, len(chaff)):
            flag = False
            if not dist(temp[0], temp[1], chaff[c][0], chaff[c][1], min_dist):
                continue
            else:
                flag = True
                break

        if not flag:
            reg.append(temp)
        else:
            pass
    return reg
