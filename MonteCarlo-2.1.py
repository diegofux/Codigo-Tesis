import numpy as np
from pulp import *
from Function2 import Sinergias
import matplotlib.pyplot as plt

import time
#numero de iteraciones
x=100

inicio=time.time()
#Generacion solar 1kW seguimiento en 2 ejes 1/1/24
Rad = np.array([0,0,0,0,0,0,0.5664,0.6542,0.693,0.7073,0.7137,0.714,0.7127,0.705,0.7017,0.6866,0.658,0.5968,0.4617,0,0,0,0,0])

#Necesidad en kW del invernadero
EI=np.array([10,5.1737,4.8947,4.5343,0.3615,6.0981,3.7066,3.8197,2.9831,2.152,0,0,0,0,0,0,0,0,0,0,0,0.46364,0.88176,1.5069])

#lista de listas de input
inputRad=[]
inputEI=[]
inputFac=[]

#np.random.seed generator
np.random.seed(32)

#Necesito modificar este de manera que los input se muevan como un dia normal.
#generador de listas random de 24 elementos entre 0 y 1.
for j in range(0, x):
    factor=np.random.uniform(-0.25, 0.25)
    RadR = Rad*(1+factor)
    EIR = EI*(1-factor)
    inputRad.append(RadR)
    inputEI.append(EIR)
    inputFac.append(round(1+factor,3))    #redondeo a 3 decimales. Correpsonde al valro por el que se multiplica la radiacion.



#Sinergia total conjunta del caso hibrido y conjunto.
STH=[]
STC=[]

#Bucle de calculo de sinergia de cada caso.
for i in range(0, x):
    SinergiaH, SinergiaC = Sinergias (inputEI[i],inputRad[i])
    STH.append(round(SinergiaH, 3))     #redondeo a 3 decimales.
    STC.append(round(SinergiaC, 3))     #redondeo a 3 decimales.
fin=time.time()

#print("inputRad:", inputRad)
#print("inputEI:", inputEI)
print("inputFac:", inputFac)
print("STH:", STH)
print("STC:", STC)
print("Tiempo de ejecucion:", fin-inicio)

# Graficar STC por separado
plt.figure(figsize=(10, 6))
plt.plot(STC, label="STC (Sinergia Conjunta)", marker='o', linestyle='-', color='blue', alpha=0.7)
plt.title("Sinergia Conjunta (STC)")
plt.xlabel("Iteración")
plt.ylabel("Porcentaje de Sinergia (%)")
plt.legend()
plt.grid(True)
plt.tight_layout()

# Graficar STH por separado
plt.figure(figsize=(10, 6))
plt.plot(STH, label="STH (Sinergia Híbrida)", marker='s', linestyle='--', color='green', alpha=0.7)
plt.title("Sinergia Híbrida (STH)")
plt.xlabel("Iteración")
plt.ylabel("Porcentaje de Sinergia (%)")
plt.legend()
plt.grid(True)
plt.tight_layout()

# Mostrar ambos gráficos
plt.show()
