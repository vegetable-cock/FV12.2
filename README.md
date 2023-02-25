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