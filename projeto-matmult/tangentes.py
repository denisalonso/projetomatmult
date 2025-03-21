import math
import numpy as np
from scipy.integrate import odeint as od
import matplotlib.pyplot as plt

"""
def curva(intervalo):
    xlinha = []
    zeros = []
    auto_intersecoes = {}

    for x in valores:
        valor = 18 * 2 * (16*math.cos(x)**5 - 16*math.cos(x)**3 - 3*math.cos(x)) - 7
        x_linha2 = -7 * math.cos(x) + 108 * math.cos(6*x)

        valores = odeint()
        if ((valor <= 0.0001 and valor >= 0.0001) or valor == 0):
            zeros.append(valor)"

    return zeros
"""
derivada_vertical = []
derivada_horizontal = []

def modelo(x, t):
    x_linha2 = (-7 * math.cos(t)) + 108 * math.cos(6*t)
    y_linha2 = (-7 * math.sin(t)) + 108 * math.sin(6*t)
    return [x_linha2, y_linha2]

valores = np.arange(0, math.pi*2, 0.0001)

xlinha = od(modelo, [4,0], valores)

for i in range(len(valores)):
   
    if ((abs(xlinha[i][0]) <= 0.01 and abs(xlinha[i][0]) >= 0.001) or xlinha[i][0] == 0):
        derivada_vertical.append(valores[i])

    if ((abs(xlinha[i,1]) <= 0.00001 and abs(xlinha[i,1]) >= 0.000001) or xlinha[i,1] == 0):
        derivada_horizontal.append(valores[i])

print(xlinha[:][1])
print(derivada_horizontal)

#plt.plot(valores, xlinha)
#plt.show()




#print(curva([0,2*math.pi]))