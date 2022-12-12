import sympy as sp

# 变量声明
x = sp.Symbol('x')  # symbol函数返回一个对象，用于表示符号变量，具有name属性
i = 0
#a = [0]  # 用于重构的横坐标列表
#b = [0]  # 用于重构的纵坐标列表
a = [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 11]
b = [118.94484897949802, 826.5976037997699, 3330.146804352283, 9501.490129001544, 21896.52449483518, 43755.14605766396, 79001.2502120218, 132242.73159116576, 208771.4840670759, 314563.4007504556]
l = [x]
den = [1]
pl = x

degree = int(input('numero de datos数据数量 = '))  # 为什么把degree定义为阶数+1

ecu = x
# calculo de L's
for i in range(0, degree):
    if i == 0:
        for j in range(1, degree):
            print(l[0])
            if i == 1:
                l[0] = x - a[j]
                den[0] = a[0] - a[j]
            else:
                l[0] = (l[0]) * (x - a[j])
                den[0] = den[0] * (a[0] - a[j])
        l[0] = l[0] / x

    else:
        l.append(x)
        den.append(1)
        for j in range(0, degree):
            if i == 0:
                l[i] = x - a[0]
                den[i] = a[i] - a[j]
            else:
                if j != i:
                    l[i] = (l[i]) * (x - a[j])
                    den[i] = den[i] * (a[i] - a[j])
        l[i] = l[i] / x
    l[i] = l[i] / den[i]
    print('Calculo de L', i)
    print(sp.expand(l[i]))
    print(' ')

# Calculo de PL
print('PL :')
for i in range(0, degree):
    if i == 0:
        pl = b[0] * l[0]
    else:
        pl = pl + (b[i] * l[i])
print(sp.simplify(pl))
