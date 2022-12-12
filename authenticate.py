# to use: python authenticate.py fingerprints/jayme

from vaults import vaults
from fuzzy_vault import (unlock, decode)
from sys import argv
import warnings

known = ['jayme woogerd', 'norman ramsey', 'ming chow', 'Li Shiyang', 'LI SHIYANG','li shiyang']

warnings.filterwarnings("ignore")



# 那里的*到底代表引入多个参数还是解压？zip(*zip(a,b))=a,b  有这样一种用法
def main():
    #with open("fingerprints\jayme", 'r') as template:  # jayme这个文件应该就是用户用来验证的指纹
    with open("fingerprints\/norman2", 'r') as template:
        # 现在只要用其他人的指纹解锁就会报list index out of range 错

        # with open(argv[1], 'r') as f:  #with关键字会自动调用f.close()
        # open()返回了一个file，格式为open(filename, mode)，'r'表示只读
        # argv[1]实则指的是执行程序时使用者输入的第一个参数。
        # 直接在Spyder中运行因为没有参数传入，就会报list index out of range的错误

        template = [float(t) for t in template]
        # 为什么要把t转换成浮点数？

        '''for vault in vaults:
            coeffs = unlock(template, vault)
            name = decode(coeffs)
            print("Hello")
            if name in known:  # 解锁出密钥来的验证环节
                print('Hello, %s!' % name.title())'''

    for vault in vaults:  # vaults能用是因为上面import过了，这里循环应该是对三个人一一做循环,相当于和三个人解出的系数一一比对
        coeffs = unlock(template, vault)
        print("验证时的多项式", coeffs)  # 跟锁定时的完全一样，按道理应该是能解出来的
        try:
            name = decode(coeffs)
            if name in known:  # 解锁出密钥来的验证环节
                print('Hello, %s!' % name.title())
                return
        except TypeError:
            pass
    print("Unknown user")  # 为什么跳出循环之后要输出一个Unknown User？





if __name__ == '__main__':
    main()
