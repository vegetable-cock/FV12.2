## 相关函数用法与问题
### get_coefficients函数中的报错解决
python3中的除法是float型，保留小数，这会导致后面的错误。解决方法：除号/变成双除号//
### range函数用法
range函数：创建一个整数列表。
语法：`range(start, stop[, step])`，不包含stop的值，缺省从0开始、步长为1

Python3的range函数返回的是一个对象，所以要用`list`迭代得到列表

### enumerate函数用法
将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列

语法：`enumerate(sequence, [start=0])`

用例：
```
>>> seasons = ['Spring', 'Summer', 'Fall', 'Winter']
>>> list(enumerate(seasons))
[(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]
```
### ord()函数用法
返回一个字符对应的ASCII码

### round()函数用法
四舍五入到整数

### int()函数用法
强制类型转换为整型|向0取整

### zip函数用法
将可迭代的对象作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的对象

### try-except用法
try——except是一个异常捕捉语句。首先执行try子句，如果出现异常且和except的条件相同，执行except子句\
通常一个try会带有多个不同类型的except，用来反映不同类型的错误

### chr()函数用法
以一个整数（十进制或十六进制）为参数，返回对应的ASCII字符\
python3不支持unichr(),改用chr()

### if __name__ == '__main__':用法
python文件有两种执行方式：1.作为脚本直接执行；2.import到其他的python脚本中被调用执行。\
在if __name__ == '__main__'下的代码只能作为脚本直接执行。\
也就是说别的文件import了fuzzy_vault.py之后不会执行main函数\
原理：内置变量__name__的使用。\