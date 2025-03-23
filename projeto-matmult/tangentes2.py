import math as m
import numpy as np

intervalo_t = np.arange(0,2*m.pi,0.0001)

ver = []
hor = []
verif = 0.005

for t in intervalo_t:
    xlinha = -7*m.sin(t) + 18*m.sin(6*t)
    ylinha = 7*m.cos(t) - 18*m.cos(6*t)

    errox = abs(xlinha)
    erroy = abs(ylinha)

    if errox <= verif and erroy > verif:
        ver.append(t)
    
    if erroy <= verif and errox > verif:
        hor.append(t)

# print(ver)
# print(hor)

for u in ver:
    print(u, end=' / ')
print()
print('---------------------------------------------------')

for v in hor:
    print(v, end=' / ')