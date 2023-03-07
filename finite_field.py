import galois

def x_2_xgf(x):
    GF = galois.GF(2 ** 8)
    m = galois.Poly([1, 0, 0, 0, 1, 1, 1, 0, 1], field=GF)  # 本原多项式84320

    # 函数：将一个整数转换为以2为底的多项式形式
    def cal_xdeNcifang(x):  # x的取值是在0-255
        coeff_gf = []
        b_x = bin(x)
        bx_pure_num = b_x[2:]
        for i in range(0, len(bx_pure_num)):
            coeff_gf.append(bx_pure_num[i])
        return coeff_gf  # 这个函数似乎可以用GF([17, 4]).vector()方法取代？

    y = 0
    temp = list(pow(galois.Poly(GF(cal_xdeNcifang(x))), 1, m) .nonzero_degrees)
    for t in temp:
        y+=2**t
    return y

