# to use: python authenticate.py fingerprints/PUF_response

from vaults import vaults
from fuzzy_vault import (unlock, decode)
from sys import argv
import warnings
## 出问题了，现在的容错性太强了，改变好多位还是能解出来
# 是不是多项式阶数太少了？
known = ['OnNYNAzJX','onnynazjx']

warnings.filterwarnings("ignore")


# 那里的*到底代表引入多个参数还是解压？zip(*zip(a,b))=a,b  有这样一种用法
def main():
    with open("fingerprints/p1", 'r') as template:
        # with open(argv[1], 'r') as f:  #with关键字会自动调用f.close()
        # open()返回了一个file，格式为open(filename, mode)，'r'表示只读

        template = [float(t) for t in template]
        # 为什么要把t转换成浮点数？

    for vault in vaults:  # vaults能用是因为上面import过了，这里循环应该是对三个人一一做循环,相当于和三个人解出的系数一一比对
        coeffs = unlock(template, vault)
        #  print("验证时的多项式", coeffs)  # 跟锁定时的完全一样，按道理应该是能解出来的
        try:
            trad_password = decode(coeffs)
            if trad_password in known:  # 解锁出密钥来的验证环节
                print("成功解锁，恢复出的传统密钥为",trad_password)
                return
        except TypeError:
            pass
    print("Unknown user")


if __name__ == '__main__':
    main()
