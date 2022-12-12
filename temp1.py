import sympy as sp
x = sp.Symbol('x')
pL=19.4658618128069*x**4 + 20.2729253138818*x**3 + 19.4623424018191*x**2 + 18.7473477729909*x + 19.2901002501021

a=sp.poly(pL,x)
print(a.coeffs())