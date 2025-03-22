import math as m
import numpy as np

intervalo_t = np.arange(0,2*m.pi,0.01)

tol = 0.05

def x(t):
    return 7*m.cos(t)-3*m.cos(6*t)

def y(t):
    return 7*m.sin(t)-3*m.sin(6*t)

def f(b, k):
    return (-14 * m.sin(((-2*m.pi/5) * k) / 2) * m.sin(b)) - (6 * m.cos(((-2*m.pi/5) * k) * 3) * m.sin(3*b))

valores_k = [-1, -2, -3, -4, -5]


pontos = []
inter = []
for t in intervalo_t:
    pontos.append([x(t),y(t)])

"""
for i in range(len(pontos)):
    for j in range(len(pontos)):
        if i != j:
            difx = abs(pontos[i][0]-pontos[j][0])
            dify = abs(pontos[i][1]-pontos[j][1])
        
            if (difx <= tol) and (dify <= tol):
                inter.append(intervalo_t[i])
"""

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