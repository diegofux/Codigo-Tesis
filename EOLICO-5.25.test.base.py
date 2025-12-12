import numpy as np
from pulp import *



Hora = range(24)# Horas va desde 0 a x-1. 
Baterias = range(5)

#Generacion eolica de 1k instalados segun  el explorador eolico. Escalado de la generacion de 10k de Bergey-ExcelS
Viento = [0.33,0.16,0.35,0.50,0.45,0.24,0.18,0.34,0.52,0.50,0.35,0.54,0.25,0.93,0.76,1.06,0.37,0.23,0.09,0.42,0.45,0.55,0.56,0.79,0.33]
#Necesidad en kW del invernadero
#EI=[10,5.1737,4.8947,4.5343,0.3615,6.0981,3.7066,3.8197,2.9831,2.152,0,0,0,0,0,0,0,0,0,0,0,0.46364,0.88176,1.5069,10] # esta es la de 40m^2
EI=[12.10, 11.22, 11.95, 9.39, 9.34, 8.06, 9.66, 8.96, 9.90, 9.12, 7.31, 9.41, 10.56, 10.86, 10.85, 10.56, 10.52, 10.14, 7.81, 9.43, 10.50, 10.25, 9.83, 9.96, 9.51]

eta_E = 0.5
eta_R = 0
eta_C = 0.95
eta_D = 1

fracc_M=0.9#se desactiva en 1
fracc_m=0.1 #se desactiva en 0


#Costos por kW instalado. 
CE = 3865987.5 #Costo por kW de EL 4.1 #Es de notar que puede ser problematico si la produccion es de menos de 2.4kW por hora.
CEO = 6345109
Ccal = 100000
CB = [1096333, 656500, 436583, 326625,271646] ### costo asosiado a cada bateria.

Duración = [4, 2, 1, 0.5, 0.25]


EE = LpVariable.dicts("EE", (Hora), 0, None)
PE = LpVariable("PE", 0, None)

EEO = LpVariable.dicts("EEO", (Hora), 0, None)
PEO = LpVariable("PEO", 0, None)

Ecal = LpVariable.dicts("Ecal", (Hora), 0, None) #En el caso conjunto su maximo es 0.
Pcal = LpVariable("Pcal", 0, None)

EBC = LpVariable.dicts("EBC", (Baterias, Hora), 0, None)
EBD = LpVariable.dicts("EBD", (Baterias, Hora), 0, None)
PB = LpVariable.dicts("PB", (Baterias), 0, None)

B = LpVariable.dicts("B", (Baterias, Hora), 0, None)
B_Max = LpVariable.dicts("B_Max", (Baterias), 0, None)
B_init = LpVariable.dicts("B_init", (Baterias), 0, None)

Eh= LpVariable("Eh", 322.58738, None) #en el caso conjunto el minimo es 0, tiene que estar en kW.

prob = LpProblem("myProblem", LpMinimize)

#Viento es la generacion eolica de 1kW de potencia instalada equivalente para cada hora. ESto es escalado linealmente
# Restricción Operacion EO
for j in Hora:
    prob += EEO[j] <= PEO * Viento[j]
    prob += 0 <= EEO[j]                    

# Restricción Necesidad de invernadero
for j in Hora:
    prob += Ecal[j] + EE[j] * (1-eta_E) * eta_R >= EI[j]

# Restricción Equilibrio de potencias
for j in Hora:
    prob += EEO[j] + sum([EBD[i][j] for i in Baterias]) == Ecal[j] + EE[j] + sum([EBC[i][j] for i in Baterias])

# Restricción Hidrógeno.
prob += sum([EE[j] for j in Hora]) * eta_E >= Eh

# Restricción Baterias
for i in Baterias:
    for j in Hora:
        prob += EBC[i][j] <= PB[i]
        prob += EBD[i][j] <= PB[i]

#Restricción de cuanto del maximo de bateria quiero ocupar.
for i in Baterias:
    for j in Hora:
        prob += B[i][j] <= B_Max[i]*fracc_M #Desactivada.
        prob += B_Max[i]*fracc_m <= B[i][j]

#Restricción de maximo de batería
for i in Baterias:
    for j in Hora:
        prob += 0<=B_Max[i]==PB[i]*Duración[i] # ME queda la duda de si aqui deberia ser B_Max o  B[i][j]

# Restricción Estado de carga
for i in Baterias:
    for j in Hora:    
        if j==len(Hora)-1:        #Esta restriccion hace que la hora final sea igual a la hora inicial
            #break                                                                           
            prob += B_init[i] == B[i][j] + EBC[i][j]*eta_C - EBD[i][j]*(1/eta_D) 
        elif j==0:
            prob += B[i][j+1] == B_init[i] + EBC[i][j]*eta_C - EBD[i][j]*(1/eta_D)
            prob += B[i][j] == B_init[i] #ME habia faltado resolver para B[i][0] no habia explicitado que tenia que ser B_init
        else:
            prob += B[i][j+1] == B[i][j] + EBC[i][j]*eta_C - EBD[i][j]*(1/eta_D)

# Restricción Naturaleza
for j in Hora:
    prob += 0 <= EE[j] <= PE
    prob += 0 <= Ecal[j] <= Pcal
    for i in Baterias:
        prob += 0<=EBC[i][j] <= PB[i]
        prob += 0<=EBD[i][j] <= PB[i]


#Problema de optimizacion
prob += PE*CE + sum([PB[i]*CB[i] for i in Baterias]) + PEO*CEO + Pcal*Ccal
Z=PE*CE + sum([PB[i]*CB[i] for i in Baterias]) + PEO*CEO + Pcal*Ccal

status = prob.solve()

Sobra= {}
for j in Hora:
    Sobra[j] =Ecal [j] + EE[j] * (1-eta_E) * eta_R - EI[j]

print(LpStatus[status])

#print("EI:", [value(EI[j]) for j in Hora])

print("EE:", [value(EE[j]) for j in Hora])
#print("PE:", value(PE))
print("EEO:", [value(EEO[j]) for j in Hora])
#print("Viento:", [value(Viento[j]) for j in Hora])
#print("PEO:", value(PEO))
print("Ecal:", [value(Ecal[j]) for j in Hora])
#print("Pcal:", value(Pcal))
#print("EBC0:", [value(EBC[0][j]) for j in Hora]) #Hay uno para cada bateria.
#print("EBD0:", [value(EBD[0][j]) for j in Hora])
#print("B_init", [value(B_init[i]) for i in Baterias])
#print("B_Max", [value(B_Max[i]) for i in Baterias])
print("B0", [value(B[0][j]) for j in Hora])
print("B1", [value(B[1][j]) for j in Hora])
#print("B2", [value(B[2][j]) for j in Hora])
#print("B3", [value(B[3][j]) for j in Hora])
#print("PB", [value(PB[i]) for i in Baterias])
#print("CB", [value(CB[i]) for i in Baterias])
#print(Hora[0])
#print("Z:", value(Z))
#print("Eh:", value(Eh))
#print("Sobra", [value(Sobra[j]) for j in Hora])