# Li Shiyang
# NUDT UniNAV
# Start time: November 1, 2022

import math
from random import shuffle
import matplotlib.pyplot as plt
import numpy as np
from numpy import polyfit
import Lagrange as lg
import real
import vaults
from add_chaff import add_chaff

degree = 4  # 多项式阶数
t = 10  # 每个生物模板中特征点的数量
r = 400  # 杂凑点数量（好像应该是总点数？）
min_dist = 0.1  # 杂凑点与真实点的最小距离
real_point=[]
'''****************************************************************************
    函数get_coefficients:将要保护的密钥编码为多项式的系数
    输入：密钥字符串
    返回：多项式系数列表，从高阶到低阶

    problem：
    创建多项式的时候用for直接写的，但之后如果不是每阶都有的时候可能要改，或者在系数列表对应位置0
****************************************************************************'''


def get_coefficients(word):
    word = word.upper()  # 转换成大写。为啥要这么操作？
    n = len(word) // degree  # n为系数的长度
    if n < 1: n = 1  # 如果n<1就拉到1
    substrings = [word[i:i + n] for i in list(range(0, len(word), n))]

    coeffs = []
    for substr in substrings:
        num = 0
        for x, char in enumerate(substr):
            num += ord(char) * 100 ** x
        coeffs.append(num ** (1 / 3.0))
    return coeffs


'''****************************************************************************
函数p_x：计算x代入多项式后对应的纵坐标
输入：某个横坐标值x、系数列表coeffs（从高阶到低阶）
返回：该x代入多项式后对应的纵坐标值
****************************************************************************'''


def p_x(x, coeffs):
    y = 0
    d = len(coeffs) - 1
    for coeff in coeffs:
        y += x ** d * coeff  # y=cx^4+cx^3+cx^2+cx
        d -= 1
    return y  # y=f(x),即x代入多项式里对应的纵坐标值


'''****************************************************************************
函数lock：用于生成一个fuzzy vault，
lock在main函数里被调用，访问的是real中的传统密钥和PUF响应(CRC编码分组后的)
输入：传统密钥secret、生物特征模板template
返回：锁定好的vault,以嵌套列表形式返回
三个人对应的10个真实点和30个杂凑点
****************************************************************************'''


def lock(secret, template):
    global real_point
    vault = []
    coeffs = get_coefficients(secret)
    # print('coeffs=', coeffs)
    # 对于PUF响应中的每个点（横坐标），在vault里添加(x,f(x))，即真实点
    for point in template:
        vault.append([point, p_x(point, coeffs)])

    print("真实点", vault)  # 这里的真实点是没问题的
    tempx = []
    tempy = []
    for v in vault:
        tempx.append(v[0])
        tempy.append(v[1])
    plt.scatter(tempx, tempy, color='blue')
    plt.show()

    real_point=vault    #生成一个真实点列表用来画图

    chaff_point = add_chaff(r, t, vault, 1000)
    vault = vault + chaff_point  # 这样直接加会不会比较慢？查一下
    shuffle(vault)  # shuffle()方法：打乱
    return vault






'''****************************************************************************
函数approx_equal：在unlock函数的内嵌函数project中用来判断点距离
输入：
返回：bool值。|a-b|小于epsilon时返回True，否则返回False。
****************************************************************************'''


def approx_equal(a, b, epsilon):
    return abs(a - b) < epsilon


'''****************************************************************************
函数unlock：给定一个生物模板和一个模糊保险箱，匹配则返回系数，不匹配则返回none
输入：参数vault：设备存储的vault
template:用来验证的PUF响应模板（比如fingerprints\PUF_response)
返回：多项式系数列表
4.内嵌函数project：读取vault中的点，如果x与vault中真实点point[0]之间的距离小于0.001，返回坐标[x,point[1]]
  其返回的[x,point[1]]组成了用来尝试重构的备选点集（对于某个x值来说）
****************************************************************************'''


def unlock(template, vault):
    def project(x):
        for point in vault:
            if approx_equal(x, point[0], 0.001):  # 阈值过小合法用户可能不能解锁，阈值过大安全性下降
                return [x, point[1]]
        return None

    Q = list(zip(*[project(point) for point in template if project(point) is not None]))
    try:  # *的作用：将任意个数的参数导入到函数当中
        print("lagrange多项式系数列表为", lg.langr(list(Q[0]), list(Q[1]), degree + 1))
        return lg.langr(list(Q[0]), list(Q[1]), degree + 1)
    except IndexError:  # 我总觉得这种强制忽略某种错误的方式不太合适呢
        return None


'''****************************************************************************
函数decode：解码
如果用户解出来的coeffs是合法的，那么经过decode以后就会得到对应的word（人名）
本函数与前面的get_coefficients函数是互逆操作
输入：系数    
返回：
****************************************************************************'''


def decode(coeffs):
    s = ""
    for c in coeffs:
        num = int(round(c ** 3))  # num是系数某一位的三次方取整，对于c=19.46,num=7376
        if num == 0:
            continue  # num=0则跳出本次循环，开始读取下一阶系数
        while num > 0:
            s += str(chr(int(num % 100))).lower()
            print(s)
            num = num // 100  # 双除号//向下取整
    return s


'''****************************************************************************
main函数：生成vault
输入：系数    
str函数：将参数转化为字符串。因为write()里必须是字符串，不能直接写入列表
****************************************************************************'''


def main():
    with open('vaults.py', 'w+') as f:
        f.write('vaults = ')
        for p in real.people:
            f.write(str(lock(p, real.people[p])))
            f.write(',')
        f.close()

        for ap in vaults.vaults:
            tempx = []
            tempy = []
            for pp in ap:
                tempx.append(pp[0])
                tempy.append(pp[1])
            plt.scatter(tempx, tempy, color='red')
        tempx = []
        tempy = []
        for v in real_point:
            tempx.append(v[0])
            tempy.append(v[1])
        plt.scatter(tempx, tempy, color='blue')
        plt.show()
    # 真实点画图



if __name__ == '__main__':
    main()
