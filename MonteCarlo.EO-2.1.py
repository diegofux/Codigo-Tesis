import numpy as np
from pulp import *
from FunctionEO import SinergiasEO
import matplotlib.pyplot as plt

import time
#numero de iteraciones
x=100

inicio=time.time()
#Generacion eolica de 1k instalados segun  el explorador eolico. Escalado de la generacion de 10k de Bergey-ExcelS
Viento = np.array([0.33,0.16,0.35,0.50,0.45,0.24,0.18,0.34,0.52,0.50,0.35,0.54,0.25,0.93,0.76,1.06,0.37,0.23,0.09,0.42,0.45,0.55,0.56,0.79,0.33])
#Necesidad en kW del invernadero
#EI=[10,5.1737,4.8947,4.5343,0.3615,6.0981,3.7066,3.8197,2.9831,2.152,0,0,0,0,0,0,0,0,0,0,0,0.46364,0.88176,1.5069,10] # esta es la de 40m^2
EI=np.array([20,11.27,10.945,8.0476,9.2937,9.9981,6.6946,7.5851,9.2656,9.6665,10.101,10.34,10.754,7.6663,7.5095,8.9385,9.9239,10.274,9.9329,9.2882,8.847,11.419,10.573,9.7364,20])

#lista de listas de input
inputViento=[]
inputEI=[]
inputFac=[]

#np.random.seed generator
np.random.seed(32)

#Necesito modificar este de manera que los input se muevan como un dia normal.
#generador de listas random de 24 elementos entre 0 y 1.
for j in range(0, x):
    factor=np.random.uniform(-0.25, 0.25)
    VientoR = Viento*(1+factor)
    EIR = EI*(1-factor)
    inputViento.append(VientoR)
    inputEI.append(EIR)
    inputFac.append(round(1+factor,3))    #redondeo a 3 decimales. Correpsonde al valro por el que se multiplica la radiacion.



#Sinergia total conjunta del caso hibrido y conjunto.
STH=[]
STC=[]

#Bucle de calculo de sinergia de cada caso.
for i in range(0, x):
    SinergiaH, SinergiaC = SinergiasEO (inputEI[i],inputViento[i])
    STH.append(round(SinergiaH, 3))     #redondeo a 3 decimales.
    STC.append(round(SinergiaC, 3))     #redondeo a 3 decimales.
fin=time.time()

#print("inputViento:", inputViento)
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
