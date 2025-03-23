import math as m
import numpy as np

int_t = np.arange(0,2*m.pi,0.01)
int_u = np.arange(0,2*m.pi,0.01)
int_v = np.arange(0,2*m.pi,0.01)

tol = 0.01
list =[]
for u in int_u:
    for v in int_v:
        if u !=v :
            compare = abs(m.tan((u+v)/2)-m.tan(3*(u+v)))
            if compare <= tol:
                list.append([u,v])

for item in list:
    print(list)