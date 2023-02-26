# this file was used to generate the fuzzy vaults in vaults.py
# 合法用户及其简化的指纹信息
# 这些信息不应该明文存储，生成vault后就应该销毁这个文件
# 应该用PUF响应来代替
# 在模糊保险箱中用于组成多项式的

# people的数据类型属于“集合”，特点是无序、不包含重复元素
# 因为无序，所以访问时一般是用循环逐个读出
# people这个集合里的元素只是人名？那后面的列表是什么情况？
people = {
    "PUF response": [1.1, 2.2, 3.3, 4.4, 5.5,
                   6.6, 7.7, 8.8, 9.9, 11]
}

