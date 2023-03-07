import re
a = 'ab10 v 32 r4'
s = [float(s) for s in re.findall(r'-?\d+\.?\d*', str(a))]  # 没有考虑x是1阶的时候
print(s)