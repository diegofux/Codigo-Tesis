import numpy as np
from pulp import *
from Function1 import Sinergias

import time
#numero de iteraciones
x=2

inicio=time.time()
#Generacion solar 1kW seguimiento en 2 ejes 1/1/24
#Rad = [0,0,0,0,0,0,0.5664,0.6542,0.693,0.7073,0.7137,0.714,0.7127,0.705,0.7017,0.6866,0.658,0.5968,0.4617,0,0,0,0,0]

#Necesidad en kW del invernadero
#EI=[10,5.1737,4.8947,4.5343,0.3615,6.0981,3.7066,3.8197,2.9831,2.152,0,0,10,0,0,0,0,0,0,0,0,0.46364,0.88176,1.5069]

#lista de listas de input
inputRad=[]
inputEI=[]

#np.random.seed generator
np.random.seed(32)

#Necesito modificar este de manera que los input se muevan como un dia normal.
#generador de listas random de 24 elementos entre 0 y 1.
for j in range(0, x):
    Rad = np.random.rand(24)
    EI = np.random.rand(24)
    inputRad.append(Rad)
    inputEI.append(EI)



#Sinergia total conjunta del caso hibrido y conjunto.
STH=[]
STC=[]

#Bucle de calculo de sinergia de cada caso.
for i in range(0, x):
    SinergiaH, SinergiaC = Sinergias (inputRad[i], inputEI[i])
    STH.append(SinergiaH)
    STC.append(SinergiaC)
fin=time.time()

#print("inputRad:", inputRad)
#print("inputEI:", inputEI)
print("STH:", STH)
print("STC:", STC)
print("Tiempo de ejecucion:", fin-inicio)
#print("SinergiaC:", SinergiaC)