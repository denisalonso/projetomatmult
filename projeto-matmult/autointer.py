import math as m
import numpy as np

intervalo_t = np.arange(0,2*m.pi,0.01)

verif = 0.00000000000000001

def x(t):
    return m.cos(t)-3*m.cos(6*t)

def y(t):
    return m.sin(t)-3*m.sin(6*t)

pontos = []
inter = []
for t in intervalo_t:
    if len(pontos) != 0:
        ponto_novo = [x(t),y(t)]
        pontos.append(ponto_novo)
        for i in range(len(pontos)):
            difx = abs(pontos[i][0]-ponto_novo[0])
            dify = abs(pontos[i][1]-ponto_novo[1])
            #print([difx,dify])
            if (difx <= 0.01) and (dify <= 0.01):
                #print([difx,dify])
                inter.append(t)
    else:
        pontos.append([x(t),y(t)])

print(pontos)

# print(inter)