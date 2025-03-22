import math as m
import numpy as np

intervalo_t = np.arange(0,2*m.pi,0.01)

tol = 0.08

def x(t):
    return 7*m.cos(t)-3*m.cos(6*t)

def y(t):
    return 7*m.sin(t)-3*m.sin(6*t)

pontos = []
inter = []
for t in intervalo_t:
    pontos.append([x(t),y(t)])

for i in range(len(pontos)):
    ponto_comparacao = pontos[i]
    for j in range(len(pontos)):
        if i != j:
            difx = abs(pontos[i][0]-pontos[j][0])
            dify = abs(pontos[i][1]-pontos[j][1])
            if (difx <= tol) and (dify <= tol):
                inter.append(intervalo_t[j])
#print(pontos)

print(inter)