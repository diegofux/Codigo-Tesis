import numpy as np
from pulp import *
from FunctionMpEO import Sinergias
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import matplotlib.cm as cm

import time
#numero de iteraciones
#((1.96*4.38)/(0.5))^2=294,7 es decir error absoluto de 0.5 y 95% de confianza.
Niteraciones=400

#Lo modificamos para que sea eolico
inicio=time.time()
Viento0=np.array([0.33,0.16,0.35,0.50,0.45,0.24,0.18,0.34,0.52,0.50,0.35,0.54,0.25,0.93,0.76,1.06,0.37,0.23,0.09,0.42,0.45,0.55,0.56,0.79,0.33])
#//
# 1/4 intermedio alto
Viento1 = np.array([0.905132, 0.44416, 0.234971, 0.305277, 0.562511, 0.824427, 0.62593, 0.706662, 0.586962, 1.056215, 1.085657, 1.063077, 0.939174, 0.8946, 1.072787, 0.963692, 0.679081, 0.676322, 1.039084, 1.063999, 1.04985, 1.086141, 0.767282, 1.080359
])
#generacion 8/8 intemedio bajo
Viento2=np.array([1.106425, 1.088424, 0.746549, 0.598073, 0.675161, 0.924556, 0.78571, 1.054824, 1.086607, 1.082486, 1.082976, 1.070134, 1.048209, 1.064867, 0.759242, 0.629792, 0.479417, 0.627273, 0.559565, 0.476944, 0.355148, 0.141167, 0.637445, 0.571461
])
#1/11 alto
Viento3=np.array([1.085098, 1.088741, 1.078314, 1.087304, 1.080169, 0.62206, 0.535874, 0.592648, 0.684561, 1.047044, 1.08924, 1.06543, 1.079813, 0.834908, 0.709914, 0.888161, 1.026492, 0.862917, 0.793166, 0.711313, 0.447892, 0.49689, 0.793379, 1.066304])
#1/10 bajo
Viento4=np.array([0.346372, 0.402548, 0.422926, 0.386962, 0.243794, 0.39346, 0.363812, 0.463903, 0.311487, 0.289391, 0.238925, 0.333945, 0.130579, 0.082424, 0.127895, 0.11731, 0.040044, 0.04121, 0.004112, 0.33976, 0.282843, 0.217342, 0.344759, 0.47105])



YRad=[Viento0, Viento1, Viento2, Viento3, Viento4]

#Necesidad en kW del invernadero
# eolico 
EI0=np.array([12.10, 11.22, 11.95, 9.39, 9.34, 8.06, 9.66, 8.96, 9.90, 9.12, 7.31, 9.41, 10.56, 10.86, 10.85, 10.56, 10.52, 10.14, 7.81, 9.43, 10.50, 10.25, 9.83, 9.96, 9.51])
## 1/4 intermedio alto      
EI1=np.array([14.337, 6.4365, 3.4246, 4.4925, 5.8276, 5.6275, 3.1684, 4.6692, 5.1311, 5.1868, 5.8238, 6.5397, 8.5069, 9.0448, 9.1571, 9.0787, 9.1373, 9.325, 8.5644, 8.5415, 8.9853, 8.9542, 8.3834, 7.6364, 6.8527])
# 8/8 intemedio bajo
EI2=np.array([12.169, 10.38, 10.43, 9.1484, 8.6224, 9.1905, 6.7825, 8.5057, 9.994, 10.825, 12.206, 10.343, 11.8, 10.658, 10.054, 10.471, 10.627, 10.831, 11.056, 10.481, 10.342, 10.841, 8.4306, 9.4446, 8.7292])
#1/11 alto
EI3=np.array([11.463, 5.0892, 6.956, 5.2849, 1.8071, 1.894, 3.942, 2.8751, 5.453, 9.5299, 7.7736, 8.9361, 9.1629, 9.2619, 10.033, 10.09, 9.7933, 9.3419, 7.7261, 9.0252, 5.8874, 5.1765, 5.254, 7.0922, 6.7752])
#1/10 bajo
EI4=np.array([11.733, 6.4854, 8.1852, 4.3587, 4.1676, 2.4682, 1.1028, 1.4773, 6.148, 8.6617, 9.1151, 9.2677, 9.3489, 9.6432, 10.399, 10.335, 9.8222, 9.883, 10.277, 10.237, 10.206, 9.4881, 8.7649, 8.1354, 7.5084])
YEI=[EI0, EI1, EI2, EI3, EI4]

#generador de lista de indices entre 0 y 4
np.random.seed(32)
numeros_aleatorios = np.random.randint(0, 5, Niteraciones)



#Sinergia total conjunta del caso hibrido y conjunto.
STH=[]
STC=[]
VInputs= [] #inputs variables de la funcion sinergia.
ZBase_values = []  # Lista para almacenar los valores de ZBase
InEI=[]

# Listas para almacenar resultados adicionales
Conjunto_values = []
Hibrido_values = []
AhorroH=[]

#Bucle de calculo de sinergia de cada caso.
for i in range(0, Niteraciones):
    Xei = numeros_aleatorios[i]
    SinergiaH, SinergiaC, ZBase, Xinputs, Conjunto, Hibrido = Sinergias(YEI[Xei], YRad[Xei])
    STH.append(round(SinergiaH, 3))     #redondeo a 3 decimales.
    STC.append(round(SinergiaC, 3))     #redondeo a 3 decimales.
    VInputs.append(Xinputs)  # Almacenar los inputs variables de la función Sinergias
    ZBase_values.append(ZBase)
    Conjunto_values.append(Conjunto)
    Hibrido_values.append(Hibrido)
    AhorroH.append(ZBase-Hibrido)

# Suponiendo que VInputs es una lista de listas, cada sublista tiene 9 elementos
VInputs_colnames = [
    "eta_E", "eta_C", "Rec", "fracc_M", "fracc_m", "CE", "CPV", "Ccal",
    "CB0", "CB1", "CB2", "CB3", "CB4"
]

# Crear DataFrame con los resultados principales
df = pd.DataFrame({
    "numeros_aleatorios": numeros_aleatorios,
    "Base": ZBase_values,
    "Conjunto": Conjunto_values,
    "Hibrido": Hibrido_values,
    "STC": STC,
    "STH": STH    
})

# Expandir VInputs en columnas separadas y unir al DataFrame
VInputs_df = pd.DataFrame(VInputs, columns=VInputs_colnames)
df = pd.concat([df, VInputs_df], axis=1)

# Mostrar las primeras filas del DataFrame
#print(df.head())
print("Hibrido_values", Hibrido_values)
print("ZBase_values", ZBase_values)
print("AhorroH",AhorroH)


# Exportar a Excel
df.to_excel(r"C:\Users\beatr\Desktop\resultados_montecarlo_1.35EO.xlsx", index=False)

#Resumen de resultados
fin=time.time()
#print("STH:", STH)
#rint("STC:", STC)
#print("ZBase", ZBase_values)
print("Tiempo de ejecucion:", fin-inicio)

# Obtener los valores de eta_E
eta_E_values = [vin[0] for vin in VInputs]

# Graficar STC con eta_E en el eje horizontal y color por Xei
plt.figure(figsize=(10, 6))
sc1 = plt.scatter(eta_E_values, STC, c=numeros_aleatorios, cmap='tab10', alpha=0.7)
plt.title("Sinergia Conjunta (STC) vs Eficiencia eta_E")
plt.xlabel("Eficiencia eta_E")
plt.ylabel("Porcentaje de Sinergia (%)")
plt.legend(*sc1.legend_elements(), title="Dia utilizado")
plt.grid(True)
plt.tight_layout()
#plt.colorbar(sc1, label="Xei utilizado")

# Graficar STH con eta_E en el eje horizontal y color por Xei
plt.figure(figsize=(10, 6))
sc2 = plt.scatter(eta_E_values, STH, c=numeros_aleatorios, cmap='tab10', alpha=0.7)
plt.title("Sinergia Híbrida (STH) vs Eficiencia eta_E")
plt.xlabel("Eficiencia eta_E")
plt.ylabel("Porcentaje de Sinergia (%)")
plt.legend(*sc2.legend_elements(), title="Dia utilizado")
plt.grid(True)
plt.tight_layout()
#lt.colorbar(sc2, label="Xei utilizado")

# Graficar STC con ZBase en el eje horizontal y color por Xei
plt.figure(figsize=(10, 6))
sc3 = plt.scatter(ZBase_values, STC, c=numeros_aleatorios, cmap='tab10', alpha=0.7)
plt.title("Sinergia Conjunta (STC) vs Costo Base (ZBase)")
plt.xlabel("Costo Base (ZBase)")
plt.ylabel("Porcentaje de Sinergia (%)")
plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
plt.legend(*sc3.legend_elements(), title="Dia utilizado")
plt.grid(True)
plt.tight_layout()
#plt.colorbar(sc3, label="Xei utilizado")

# Graficar STH con ZBase en el eje horizontal y color por Xei
plt.figure(figsize=(10, 6))
sc4 = plt.scatter(ZBase_values, STH, c=numeros_aleatorios, cmap='tab10', alpha=0.7)
plt.title("Sinergia Híbrida (STH) vs Costo Base (ZBase)")
plt.xlabel("Costo Base (ZBase)")
plt.ylabel("Porcentaje de Sinergia (%)")
plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
plt.legend(*sc4.legend_elements(), title="Dia utilizado")
plt.grid(True)
plt.tight_layout()
#plt.colorbar(sc4, label="Xei utilizado")

# Graficar Hibrido_values vs eta_E_values y color por día utilizado
plt.figure(figsize=(10, 6))
sc_h = plt.scatter(eta_E_values, Hibrido_values, c=numeros_aleatorios, cmap='tab10', alpha=0.7)
plt.title("Costo Híbrido vs Eficiencia eta_E")
plt.xlabel("Eficiencia eta_E")
plt.ylabel("Costo Híbrido")
plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))  # <-- Formato de miles en eje Y
#plt.colorbar(sc_h, label="Día utilizado (Xei)")
plt.legend(*sc4.legend_elements(), title="Dia utilizado")
plt.grid(True)
plt.tight_layout()

# Graficar STH (vertical) vs AhorroH (horizontal) y color por día utilizado
#plt.figure(figsize=(10, 6))
#sc_ah1 = plt.scatter(AhorroH, STH, c=numeros_aleatorios, cmap='tab10', alpha=0.7)
#plt.title("Sinergia Híbrida (STH) vs Ahorro Híbrido")
#plt.xlabel("Ahorro Híbrido (ZBase - Hibrido)")
#plt.ylabel("Porcentaje de Sinergia Híbrida (STH)")
#plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))

#plt.grid(True)
#plt.tight_layout()

# Graficar AhorroH (vertical) vs eta_E (horizontal) y color por día utilizado
plt.figure(figsize=(10, 6))
sc_ah2 = plt.scatter(eta_E_values, AhorroH, c=numeros_aleatorios, cmap='tab10', alpha=0.7)
plt.title("Ahorro Híbrido vs Eficiencia eta_E")
plt.xlabel("Eficiencia eta_E")
plt.ylabel("Ahorro Híbrido (ZBase - Hibrido)")
plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
#plt.colorbar(sc_ah2, label="Día utilizado (Xei)")
plt.legend(*sc4.legend_elements(), title="Dia utilizado")
plt.grid(True)
plt.tight_layout()

plt.show()

