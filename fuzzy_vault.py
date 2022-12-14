# Li Shiyang
# NUDT UniNAV
# November 1 2022

# to run: python fuzzy_vault.py (writes to vault file vault.py)
# Q1：指纹生成。应当有一个模拟PUF的部分
# Q2：身份认证————密钥保护。现在保护的文本实际上是人名，后续用来和人名库进行比对
# Q3：编码。
# 拉格朗日插值法拟合多项式

from random import (uniform, shuffle)
import matplotlib.pyplot as plt
import numpy as np
from numpy import polyfit

import Lagrange as lg
import real

degree = 4  # 多项式阶数
t = 10  # 每个生物模板中特征点的数量
r = 40  # 杂凑点数量（好像应该是总点数？）

'''****************************************************************************
    函数get_coefficients:将要保护的密钥编码为多项式的系数
    输入：密钥字符串
    返回：多项式系数列表，从高阶到低阶
    
    函数内部问题：
    1. python3中的除法是float型，保留小数，这会导致后面的错误
    解决方法：除号/变成双除号//
    2. range函数：创建一个整数列表
    语法：range(start, stop[, step])，不包含stop的值，缺省从0开始、步长为1
    Python3的range函数返回的是一个对象，所以要用list迭代得到列表
    3. enumerate函数：将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列
    语法：enumerate(sequence, [start=0])
    用例：>>> seasons = ['Spring', 'Summer', 'Fall', 'Winter']
    >>> list(enumerate(seasons))
    [(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]
    4. ord函数：返回一个字符对应的ASCII码
    5. 创建多项式的时候用for直接写的，但之后如果不是每阶都有的时候可能要改
    或者在系数列表对应位置0
    6.这个函数已经过测试，基本好用，之后要对多项式的常数项部分再修改一下，可能有问题
    7.print发现输出了4个列表，正常来讲应该一共3个啊，第4个是把第3个又输出了一遍，排查一下是什么问题
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
输入：横坐标x、系数列表coeffs
返回：x代入多项式后对应的纵坐标
****************************************************************************'''


def p_x(x, coeffs):
    y = 0
    degree = len(coeffs) - 1

    for coeff in coeffs:
        y += x ** degree * coeff  # y=cx^4+cx^3+cx^2+cx
        degree -= 1

    return y  # y=f(x),即x代入多项式里对应的纵坐标值


'''****************************************************************************
函数lock：用于生成一个fuzzy vault，
lock在main函数里被调用
输入：密钥secret、生物特征模板template
secret=p, 是合法用户的人名（为啥secret会是人名啊真nm离谱）
template=real.people[p]（合法用户对应的指纹模板，就是列表
[0.22, 1.23, 2.342, 0.33, 1.27, 0.34, 2.32, 3.98, 1.254, 0.03]
返回：锁定好的vault,以嵌套列表形式返回
三个人对应的10个真实点和30个杂凑点
问题：1.杂凑点生成规则没有距离限制，纯随机生成
****************************************************************************'''


def lock(secret, template):
    vault = []
    point_x = []  # 暂时
    point_y = []  # 暂时
    coeffs = get_coefficients(secret)

    # 对于指纹模板中的每个点（横坐标），在vault里添加(x,f(x))，即真实点
    # 对于一个用户而言，真实点只有10个
    for point in template:
        vault.append([point, p_x(point, coeffs)])

    # 添加杂凑点
    max_x = max(template)  # 限定在真实点边界范围内添加杂凑点
    max_y = max([y for [x, y] in vault])
    for i in range(t, r):  # r应该是总点数吧
        x_i = uniform(0, max_x * 1.1)  # uniform(x,y):生成一个在[x,y]内的随机浮点数
        y_i = uniform(0, max_y * 1.1)
        vault.append([x_i, y_i])
    shuffle(vault)  # shuffle()方法：打乱
    return vault


'''
画图函数
输入应该是两个数组
亟待完善呐
'''


def painting(x, y):
    plt.scatter(x, y)
    plt.show()


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
template:用来验证的生物特征模板（比如fingerprints\jayme2)
返回：多项式系数列表
问题：1.polyfit是numpy中的拟合多项式函数，应被替换为拉格朗日拟合
2.zip函数：将可迭代的对象作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的对象
3.try——except是一个异常捕捉语句。首先执行try子句，如果出现异常且和except的条件相同，执行except子句
  通常一个try会带有多个不同类型的except，用来反映不同类型的错误
  但这里为什么要搞一个我还没看明白，IndexError之后返回None吗？那不是白检测了。
4.内嵌函数project：读取vault中的点，如果x与vault中真实点point[0]之间的距离小于0.001，返回坐标[x,point[1]]
  其返回的[x,point[1]]组成了用来尝试重构的备选点集（对于某个x值来说）
5.在try-except外调用拟合函数langr时，会出现list index out of range错误。
****************************************************************************'''


def unlock(template, vault):
    def project(x):
        for point in vault:
            if approx_equal(x, point[0], 0.001):  # 阈值过小合法用户可能不能解锁，阈值过大安全性下降
                return [x, point[1]]
        return None

    Q = list(zip(*[project(point) for point in template if project(point) is not None]))
    try:  # *的作用：将任意个数的参数导入到函数当中
        # return polyfit(list(Q[0]), list(Q[1]), deg=degree)
        print("lagrange多项式系数列表为", lg.langr(list(Q[0]), list(Q[1]), degree + 1))
        return lg.langr(list(Q[0]), list(Q[1]), degree + 1)
    except IndexError:
        return None


'''****************************************************************************
函数decode：解码
如果用户解出来的coeffs是合法的，那么经过decode以后就会得到对应的word（人名）
本函数与前面的get_coefficients函数是互逆操作
输入：系数    
返回：
备注：
1. Python3 不支持 unichr()，改用 chr() 函数。
2. round()函数：四舍五入到整数
3. int()函数：强制类型转换为整型|向0取整
****************************************************************************'''


def decode(coeffs):
    s = ""
    for c in coeffs:
        num = int(round(c ** 3))  # num是系数某一位的三次方取整，对于c=19.46,num=7376
        if num == 0:
            continue  # num=0则跳出本次循环，开始读取下一阶系数
        while num > 0:
            s += str(chr(int(num % 100))).lower()
            print("s=", s)
            num = num // 100  # 双除号//向下取整
    return s  # 为什么读取一个字母就跳出循环了？


'''****************************************************************************
main函数：生成vault
输入：系数    
生成的vault是三层嵌套的列表，vault中元素的个数=real里的人数，每个元素又是一个列表，存放了这个人的指纹信息
str函数：将参数转化为字符串。因为write()里必须是字符串，不能直接写入列表
****************************************************************************'''


def main():
    with open('vaults.py', 'w+') as f:
        f.write('vaults = [')
        for p in real.people:
            f.write(str(lock(p, real.people[p])))
            f.write(',')
        f.write(']')

    # 画图：最后存的模糊保险箱的图
    tempx = []
    tempy = []
    for a in lock(p, real.people[p]):
        tempx.append(a[0])
        tempy.append(a[1])
    painting(tempx, tempy)


if __name__ == '__main__':
    main()
'''
作用：python文件有两种执行方式：1.作为脚本直接执行；2.import到其他的python脚本中被调用执行。
在if __name__ == '__main__'下的代码只能作为脚本直接执行。
也就是说别的文件import了fuzzy_vault.py之后不会执行main函数
原理：内置变量__name__的使用。

问题：是否多此一举？别的文件好像也没有直接import fuzzy_vault啊
'''
