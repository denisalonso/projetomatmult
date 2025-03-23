import math as m
import numpy as np

intervalo_u = np.arange(0,2*m.pi,0.1)
intervalo_v = np.arange(0,2*m.pi,0.1)

tol = 0.001

def x(t):
    return 7*m.cos(t)-3*m.cos(6*t)

def y(t):
    return 7*m.sin(t)-3*m.sin(6*t)

inter = []
for u in intervalo_u:
    for v in intervalo_v:
        errox = abs(x(u)-x(v))
        erroy = abs(x(u)-x(v))
        if errox <= tol and erroy <= tol and u!=v:
            print(errox,erroy, [u,v])
            inter.append(u)
            # inter.append(v)

# for int in inter:
#     print(int)