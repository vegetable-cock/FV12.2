### Fuzzy Vault Implementation

This code implements a very simple "biometric" authentication system using the
fuzzy vault algorithm as described by Juels and Sudan in ==原理来源==
[*A Fuzzy Vault Scheme*](http://people.csail.mit.edu/madhu/papers/2002/ari-journ.pdf). 
I have made some notable simplifications (in `fuzzy_vault.py`):

1. The "biometric" data is represented as a list of **ten floats**. Real fingerprint data is more complex.  生物数据做了简化，可以当做PUF响应
1. I have simplified the polynomial interpolation -- rather than using [Reed-Solomon codes](http://en.wikipedia.org/wiki/Reed%E2%80%93Solomon_error_correction),  I used the a polynomial fit function.
1. Chaff points are not thrown out弃掉 if they collide冲突 with genuine points on the polynomial.

To run the program, choose a fingerprint file from the `fingerprints` directory,
e.g. `ming` and run:

    python authenticate.py fingerprints/ming

#### 12.12更新：
1. 基于sympy包编写函数实现了拉格朗日插值法对多项式进行重构，不再使用numpy中的最小二次拟合polyfit
2. 解决了使用其他指纹进行解锁时的list Index out of range报错
3. 下一步关注多项式的选择、有限域以及画图问题。

#### 2.22更新：
1. 新增CRC32校验码的计算程序，后面把它和主体融合起来

#### 2.25更新：
1. 新增杂凑点生成过程中的距离限制算法.杂凑点最小距离如何选取？

#### 2.26更新：
1. 实现了生成随机点与真实点集的距离限制算法。
2. 现存的问题是杂凑点之间的距离限制，在使用循环的时候还是存在问题

#### 2.27
1. 实现了一种杂凑点间距离限制的解法，但太过冗余，运行时间也很长，后面做下优化

#### 2.28
1. 又做了一种杂凑点间距离限制的算法，效果还可以，目前先用这个吧
2. 把杂凑点函数封装了出来，增强可读性
3. 杂凑点最小距离min_dist应该综合考虑安全性和易用性（认证成功率）的需求

#### 3.1
1. bug处理：vault中存放的点和画图的点对不上，原因是画图函数又调用了一遍lock函数，导致重新生成了新的杂凑点。改为
访问vault文件进行画图

#### 3.2
1. 完成位置信息的CRC32编码、分组、转化为坐标，并进行了锁定和验证