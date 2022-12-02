# Li Shiyang
# NUDT UniNAV
# November 1 2022

# to run: python fuzzy_vault.py (writes to vault file vault.py)


from random import (uniform, shuffle)
import matplotlib.pyplot as plt
import numpy as np
from numpy import polyfit
# import real
import test_real  # 暂时用我自己编的数

degree = 4  # 多项式阶数
t = 10  # 每个生物模板中特征点的数量
r = 40  # 杂凑点数量

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
    word = word.upper()  # 把字符串word中的小写字符转换成大写
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
[[0.5544237356825636, 29035.290998059405], [3.6774561140234336, 26734.93967792929], [3.332357096282071, 12308.300653080201], [1.6353128952050833, 8908.139614810714], [2.88596981053168, 4838.698875731978], [1.4805204685754583, 24844.506058385792], [0.22, 30.18036456743451], [0.03, 6.982976872848139], [1.5354547070954168, 5101.780493493393], [1.542763762415411, 16275.555351195128], [3.8259825996530137, 22207.813930365926], [2.5684221686171975, 12749.56661814522], [2.592766832116223, 25517.782874039774], [2.940724821843883, 32258.43270916669], [3.98, 30385.348125796954], [1.9156666891538225, 6667.774639864121], [1.1992438997395354, 33332.157048589026], [1.4101931528879237, 11150.482457689679], [0.2849735955672542, 23043.408707355706], [2.662745537379186, 16200.463076379867], [3.2797162947741354, 24556.505538658585], [2.3739660557602846, 16449.23263259057], [0.6624505998810856, 13308.152004144373], [0.33, 48.77683713838857], [1.23, 608.7678333628766], [2.32, 4374.847702030894], [3.0963148445035524, 24445.34084239656], [0.7973958915747482, 28825.926128539002], [2.03908642968339, 5923.683303281146], [0.34, 50.7139238279746], [1.254, 641.9385996028429], [2.342, 4518.608754537812], [2.4372695795365593, 20439.58828137034], [2.49779794744214, 3602.753967525543], [0.4687806029247048, 11517.040800112438], [1.2814941087494247, 10011.98042639607], [2.189831600280636, 25201.751052085787], [2.3076392293168784, 6854.581304739064], [3.7797773555810115, 12328.241571395742], [1.27, 664.8571423304546]]
[[0.9082839979988215, 264.9904668978981], [3.744005737992776, 2658.866869149744], [1.5524987533614607, 2924.431651662618], [0.8720371680827081, 3452.8683997694534], [0.001, 4.451043162396436], [2.983847272921842, 871.0517069443348], [1.8901387042314846, 819.3624786367546], [3.765216512418751, 4437.544265093449], [0.15380689179900509, 944.1383029973755], [3.8567261196887506, 2833.847302885926], [0.32, 13.59331080002034], [2.52, 1268.4266489912109], [3.576965894710917, 2836.558066721089], [1.32, 167.16702974559988], [1.43, 209.42013148923533], [2.452, 1154.99589370935], [1.233, 138.92101556873203], [2.2285404567800167, 2655.228439931167], [1.9919709934037042, 2114.4539467090876], [0.49, 22.144849477892148], [3.55, 4268.092331197526], [0.10002293231962633, 3860.1367561642105], [3.8347454547671083, 3214.5525937661105], [2.351986674344995, 2920.7005121266234], [2.3505038625458425, 2273.5687415095804], [2.3591156456010505, 3487.0406051753394], [1.932081315359505, 1791.3323114414222], [2.057903578280166, 3108.954394586873], [1.4895246016412655, 3434.4556624622005], [2.535892927941864, 1765.8714275705643], [0.221250999409781, 2397.580276312741], [1.5971292201854832, 1645.4988282103923], [3.493729037310426, 797.1031027486288], [0.6741704141721607, 1518.5591555921876], [2.2515529956162603, 3510.3754214699675], [2.1716520528934273, 1708.022836426864], [0.34, 14.424183602701667], [2.961523553174764, 2233.318085456376], [2.836387125077735, 3204.6853211188086], [0.5700906060620985, 1168.5595224429555]]
[[1.0401581312552584, 2822.1407706922496], [1.7531424435433296, 10805.865203211324], [3.638125571242945, 4520.539249011037], [1.558540086111627, 14565.698405137804], [2.321, 4558.217209689147], [3.306662876126835, 12615.751740301263], [3.1796770586548626, 3182.3040128770995], [3.86680090704338, 8286.78494387731], [1.3790065024538032, 7034.748998653139], [3.554, 20543.38893699642], [0.8394329410527512, 13092.60254632742], [3.8415391396147416, 9282.014799653056], [1.499683108549693, 3066.845816686916], [1.11, 478.9186058535482], [1.33, 787.3276543225517], [3.194180298298685, 16753.906356077357], [3.828494386973489, 10864.391467441057], [0.01, 5.360754398373315], [1.9872296536713727, 11235.32972256183], [3.0890929930695816, 12321.289298383394], [1.2375207561407848, 17594.716496967318], [0.12, 16.54296268593907], [2.4457813906448433, 4216.758506523839], [2.4775124337804604, 9106.852751661785], [3.4012772773799327, 14357.263674139984], [0.22, 29.396630032510117], [2.9045057911314944, 8260.553484473976], [2.1176806072231757, 4955.366098910126], [0.08249284931742001, 5317.17534378245], [2.228658190469679, 21820.367877303743], [2.9314741894184237, 1934.0597504958425], [1.282868146650402, 4789.409315429719], [2.91, 10007.541034644233], [0.45, 74.26687250784877], [1.5414019869827593, 426.4697031398959], [1.11, 478.9186058535482], [3.905501273320196, 6795.683446480141], [1.7523910188909184, 21237.885142575524], [3.4587603575060095, 14825.791700852462], [0.7119095037211624, 17999.339013706845]]
[[1.6124356341701427, 2591.4002529777827], [0.5325353308513898, 6545.2738406122], [3.3401931614048723, 14922.142965764264], [3.3674411418415793, 13138.421369197782], [1.33, 787.3276543225517], [2.124528893058624, 21968.0302729565], [1.2134774833605333, 8648.706744201358], [0.01, 5.360754398373315], [2.600240320412674, 7075.1479689450125], [1.11, 478.9186058535482], [0.3166024072617549, 13602.413827157854], [2.5369319623044113, 2163.8511605490726], [1.11, 478.9186058535482], [0.5766729179314921, 4744.279799984374], [3.019961015175283, 11183.644058726644], [3.554, 20543.38893699642], [1.2040274359883045, 20318.138531880337], [1.2716789566472282, 21102.033859726143], [2.321, 4558.217209689147], [1.8880898569260909, 10351.203546704353], [3.080225445340955, 18757.060088958926], [0.45, 74.26687250784877], [1.3133237079419011, 19619.391373701525], [0.9004964528241743, 17664.49192340019], [0.8394730154858575, 19123.21029701728], [0.12, 16.54296268593907], [3.762422621951581, 941.3828850616467], [2.973801409475599, 11052.091695167044], [0.25890837706042197, 4745.844143197347], [0.5393752663519394, 109.30283134146865], [2.2930051379032745, 20694.25592887801], [0.22, 29.396630032510117], [0.08878455358273199, 19121.138217260308], [3.677474624305866, 20498.830695894976], [2.277734701800604, 8525.101735262007], [1.3970166191710978, 15111.943306033918], [3.77256339508846, 19513.230267709652], [2.91, 10007.541034644233], [1.792363664630069, 3881.010095092519], [0.13502143877916434, 5182.493405780621]]
三个人对应的10个真实点和30个杂凑点
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
        # print(vault)
        # [[0.45, 74.26687250784877], [1.11, 478.9186058535482], [2.321, 4558.217209689147], [0.12, 16.54296268593907],
        # [1.11, 478.9186058535482], [0.22, 29.396630032510117], [2.91, 10007.541034644233], [3.554, 20543.38893699642],
        # [1.33, 787.3276543225517], [0.01, 5.360754398373315]]

        # point_x.append(point)
        # point_y.append(p_x(point, coeffs))
        # print(point_y)
    # plt.scatter(point_x, point_y)
    # plt.show()
    # 问题：纵坐标上万了，太大了，应该通过调整多项式或者折合有限域的方式弥补
    # 其实应该到main函数中去画图。但是那样好像还带着杂凑点？
    # 单独写一个画图函数吧

    # 添加杂凑点
    # max_x是模板中最大数，对应三个人分别为3.98,3.55,3.554
    max_x = max(template)
    max_y = max([y for [x, y] in vault])

    # range(t,r):[t,t+1,t+2....r-1]
    # t:真实点数量；r:杂凑点数量（其实应该是所有点的数量）
    # 这里并没有距离限制，这样可能导致某些杂凑点和真实点距离过近，解锁可能出问题。
    # 杂凑点生成规则肯定要大改。
    for i in range(t, r):  # 那这不是只加了30个杂凑点么？
        x_i = uniform(0, max_x * 1.1)  # uniform(x,y):生成一个在[x,y]内的随机浮点数
        y_i = uniform(0, max_y * 1.1)
        vault.append([x_i, y_i])
    shuffle(vault)  # shuffle()方法将序列的所有元素随机排序。
    return vault


'''
画图函数
输入应该是两个数组
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
template
返回：多项式系数列表

****************************************************************************'''


def unlock(template, vault):
    # given a biometric template and a fuzzy fault, return the coefficients
    # used to encode the secret or None if the template is not a match

    # 内嵌函数project：读取vault中的点，如果x与point[0]之间的距离小于0.001，返回坐标[x,point[1]]
    # 实际上point[0]是存在vault中的真实点，而x是用来验证的点，这是一个被的过程
    # point[0]是vault中所有点的横坐标
    # point[1]是vault中点的纵坐标
    # 返回值：对应于某一个x的备选点集。比如[2.1,4.55]  [2.1, 8.341]  [2.1,123.232]
    def project(x):
        for point in vault:
            if approx_equal(x, point[0], 0.001):  # 阈值过小合法用户可能不能解锁，阈值过大安全性下降
                return [x, point[1]]
        return None

    # *的作用：将任意个数的参数导入到函数当中
    # 如果project(point)存在，也就是说验证点point能够在vault中匹配到对应的横坐标
    # 则把template中能够匹配上的这些point打包（匹配不上的不管）
    # 则Q应该是备选点集打包成的元组
    # template应该是用来验证的生物特征模板（比如fingerprints\jayme2)
    Q = list(zip(*[project(point) for point in template if project(point) is not None]))
    # Q = list(zip([project(point) for point in template if project(point) is not None]))
    print("Q=", Q)
    print("Q[0]=", list(Q[0]))
    print("Q[1]=", Q[1])  # 为啥返回的东西是一个元组？？
    # zip函数：将可迭代的对象作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的对象
    # python中zip返回的是一个列表
    print("多项式系数列表为", polyfit(Q[0], Q[1], deg=degree))  # 测试用
    try:
        return polyfit(list(Q[0]), list(Q[1]), deg=degree)
    # polyfit是numpy中的拟合多项式函数，（x,y,阶数）,xy应该是列表
    # 返回一个列表，表中为拟合出的多项式系数，从高阶到低阶
    except IndexError:
        return None
    # try——except是一个异常捕捉语句。首先执行try子句，如果出现异常且和except的条件相同，执行except子句
    # 通常一个try会带有多个不同类型的except，用来反映不同类型的错误
    # 但这里为什么要搞一个我还没看明白，IndexError之后返回None吗？那不是白检测了。


'''****************************************************************************
函数decode：解码
输入：系数    
返回：
备注：
1. Python3 不支持 unichr()，改用 chr() 函数。
2. round()函数：四舍五入到整数
3. int()函数：强制类型转换为整型
****************************************************************************'''


def decode(coeffs):
    # given a set of coefficients, decode the secret word.
    # decode(get_coefficients(word)) == word
    # 是get_coefficients函数的反函数（？）
    # 如果用户解出来的coeffs是合法的，那么经过decode以后就会得到对应的word（人名）
    s = ""
    for c in coeffs:
        print("c=", c)
        num = int(round(c ** 3))  # num是系数某一位的三次方取整，对于c=19.46,num=7376
        print("num1", num)
        # int:将一个字符串或数字化成整形，向0取整
        if num == 0:
            continue  # num=0则跳出本次循环，开始读取下一阶系数
        while num > 0:
            print("num=", num)
            print("num%100=", num % 100)
            print("chr(num%100)=", chr(num % 100))
            print("str(chr(num%100))=", str(chr(num % 100)))
            # s += str(chr(num % 100)).lower() # 原代码，解不出name来,而且为什么变成lower了啊，明明真实姓名是有大写的
            # print("s=", s)
            # s += str(chr(int(num % 100))).lower()  # 测试用，能解出来乱码，其中包含真实姓名
            s += str(chr(int(num % 100)))# 测试用，不强制转为小写
            print("s=", s)
            # num /= 100 # 原代码
            #num = round(num/100) # 测试用
            num = num // 100 #测试用2
    return s  # 为什么读取一个字母就跳出循环了？

# 现在只能全小写或者全大写，之后再改


'''****************************************************************************
main函数：生成vault
输入：系数    

str函数：将参数转化为字符串。因为write()里必须是字符串，不能直接写入列表
****************************************************************************'''


def main():
    # 生成的vault为啥是三层嵌套的列表？
    # 因为real里有三个人
    # 每个人的指纹信息化成真实点对应了vault中的40个点，一共120个点
    # 这个形式应该取决于lock函数
    # vaults中一共就三个对象，每个对象对应了40个点（10个真实点30个杂凑点）

    with open('vaults.py', 'w+') as f:
        f.write('vaults = [')
        for p in test_real.people:
            # p应该是人名。
            f.write(str(lock(p, test_real.people[p])))
            f.write(',')
        f.write(']')

    # 画图：最后存的模糊保险箱的图
    tempx = []
    tempy = []
    for a in lock(p, test_real.people[p]):
        tempx.append(a[0])
        tempy.append(a[1])
    painting(tempx, tempy)


if __name__ == '__main__':  # python的初始化？
    main()
'''
作用：python文件有两种执行方式：1.作为脚本直接执行；2.import到其他的python脚本中被调用执行。
在if __name__ == '__main__'下的代码只能作为脚本直接执行。
也就是说别的文件import了fuzzy_vault.py之后不会执行main函数
原理：内置变量__name__的使用。

问题：是否多此一举？别的文件好像也没有直接import fuzzy_vault啊
'''
