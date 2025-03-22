import math as m
import numpy as np

intervalo_t = np.arange(0,2*m.pi,0.0001)

ver = []
hor = []
verif = 0.008
for t in intervalo_t:
    xlinha = -7*m.sin(t) + 18*m.sin(6*t)
    ylinha = 7*m.cos(t) - 18*m.cos(6*t)

    errox = abs(xlinha)
    erroy = abs(ylinha)

    if errox <= verif:
        ver.append(t)
    
    if erroy <= verif:
        hor.append(t)

print(ver)
print(hor)