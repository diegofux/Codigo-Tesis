import numpy as np
from pulp import *
from FunctionMp import Sinergias
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

import time
#numero de iteraciones
#((1.96*4.38)/(0.5))^2=294,7 es decir error absoluto de 0.5 y 95% de confianza.
Niteraciones=400

inicio=time.time()
#17-6 dia frio
Rad0=np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0.3834, 0.4488, 0.4406, 0.4102, 0.4, 0.4175, 0.4422, 0.4261, 0.3133, 0, 0, 0, 0, 0, 0])
#Generacion solar 1kW  13/4/24
Rad1 = np.array([0,0,0,0,0,0,0,0,0.39,0.5252,0.5649,0.5524,0.5291,0.5236,0.5359,0.5548,0.538,0.4497,0.1465,0,0,0,0,0,0])
#generacion 1-1 dia calido
Rad2=np.array([0, 0, 0, 0, 0, 0, 0.0067, 0.4808, 0.6113, 0.6747, 0.6942, 0.697, 0.6953, 0.6943, 0.6966, 0.6963, 0.6874, 0.6465, 0.5508, 0.3736, 0, 0, 0, 0])
#4-19 dia intermedio
Rad3=np.array([0, 0, 0, 0, 0, 0, 0, 0, 0.4654, 0.5771, 0.6083, 0.5921, 0.5739, 0.569, 0.5789, 0.5947, 0.5793, 0.4999, 0.2737, 0, 0, 0, 0, 0])
#9-4 dia intermedio
Rad4=np.array([0, 0, 0, 0, 0, 0, 0, 0, 0.4654, 0.5771, 0.6083, 0.5921, 0.5739, 0.569, 0.5789, 0.5947, 0.5793, 0.4999, 0.2737, 0, 0, 0, 0, 0]
)


YRad=[Rad0, Rad1, Rad2, Rad3, Rad4]

#Necesidad en kW del invernadero
# 17-6 Dia frio
EI0=np.array([6.4344,6.1505,5.9392,6.4899,5.992,5.429,5.1628,4.6688,3.0976,1.7929,0.45942,0,0,0,0,0,0,0,0,0.81437,1.6266,2.21,2.4891,2.0761
])
#13/4/24 Dia intermedio        
EI1=np.array([6.09,4.33,0.55,6.32,2.65,6.53,5.64,2.99,3.09,2.32,0.93,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
# 1-1 Dia calido
EI2=np.array([5.4807,0.22685,0,2.572,2.3762,3.5441,2.3793,1.237,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
#4-19 dia intermedio
EI3=np.array([6.1458, 4.7885, 4.5041, 4.0143, 3.4841, 3.8688, 3.6294, 3.5633, 3.0115, 1.0761, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.19518, 0.77247, 1.2698, 1.916])
#9-4 dia intermedio
EI4=np.array([6.4181, 6.7626, 5.9428, 5.2062, 5.2279, 5.589, 5.1406, 5.1926, 2.6034, 1.0767, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.52746, 1.4616, 2.3968, 2.6347, 2.4513]
)
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

# Exportar a Excel
df.to_excel(r"C:\Users\beatr\Desktop\resultados_montecarlo_1.35.xlsx", index=False)

#Resumen de resultados
fin=time.time()
print("STH:", STH)
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
plt.legend(*sc4.legend_elements(), title="Dia utilizado")
#plt.colorbar(sc_h, label="Día utilizado (Xei)")
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
plt.legend(*sc4.legend_elements(), title="Dia utilizado")
#plt.colorbar(sc_ah2, label="Día utilizado (Xei)")
plt.grid(True)
plt.tight_layout()


# Mostrar ambos gráficos
plt.show()

