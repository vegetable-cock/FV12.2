## 相关函数用法与问题
### 1. get_coefficients函数中的报错解决
python3中的除法是float型，保留小数，这会导致后面的错误。解决方法：除号/变成双除号//
### 2. range函数用法
range函数：创建一个整数列表。
语法：`range(start, stop[, step])`，不包含stop的值，缺省从0开始、步长为1

Python3的range函数返回的是一个对象，所以要用`list`迭代得到列表

### 3. enumerate函数用法
将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列

语法：`enumerate(sequence, [start=0])`

用例：
```
>>> seasons = ['Spring', 'Summer', 'Fall', 'Winter']
>>> list(enumerate(seasons))
[(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]
```
### ord函数用法
返回一个字符对应的ASCII码

### 