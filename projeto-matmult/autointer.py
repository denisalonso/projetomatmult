import math as m
import numpy as np

intervalo_t = np.arange(0,2*m.pi,0.0008)

tol = 0.001

inter = []

def f(b, k):
    return (-14 * m.sin(((-2*m.pi/5) * k) / 2) * m.sin(b)) - (6 * m.cos(((-2*m.pi/5) * k) * 3) * m.sin(3*b))

valores_k = [-1, -2, -3, -4, -5]

for b in intervalo_t:
    for k in valores_k:
        func = f(b,k)
        if (func == 0) or (func <= 0 + tol and func >= 0 - tol):
            y = ((-2*m.pi*k/5) - b) / 2
            x = (-2*m.pi*k/5) - y

            if x != y:
                inter.append([x,y])

#print(pontos)

print(inter)
