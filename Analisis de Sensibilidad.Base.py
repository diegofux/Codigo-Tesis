import numpy as np
from pulp import *



Hora = range(8)# Horas va desde 0 a x-1. 
Baterias = range(1)

#Generacion eolica de 1k instalados segun  el explorador eolico. Escalado de la generacion de 10k de Bergey-ExcelS
#Dia representativo de ENERO
Rad = [0,0,1,1,1,1,0,0]
#Necesidad en kW del invernadero
#EI=[1,0.472,0.581,0.579,0.548,0.553,0.348,0,0,0,0.0,0,0,0,0,0,0,0,0,0,0,0,0,0] #esta es la de de 4m^2
EI=[1,1,0,0,0,0,1,1]
eta_E = 0.5 #si la eficiencia del electrolizador es 1. no sep uede derivar calor de él
eta_R = 0
eta_C = 1
eta_D = 1

fracc_M=1#se desactiva en 1
fracc_m=0 #se desactiva en 0


#Costos por kW instalado. 
CE = 10 #Costo por kW de EL 4.1 #Es de notar que puede ser problematico si la produccion es de menos de 2.4kW por hora.
CEO = 1
Ccal = 0.5
CB = [3] ### costo asosiado a cada bateria.

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

Eh= LpVariable("Eh", 4, None) #en el caso conjunto el minimo es 0, tiene que estar en kW.

prob = LpProblem("myProblem", LpMinimize)

#Viento es la generacion eolica de 1kW de potencia instalada equivalente para cada hora. ESto es escalado linealmente
# Restricción Operacion EO
for j in Hora:
    prob += EEO[j] <= PEO * Rad[j]
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
            #prob +=  EBD[i][j]==0
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
B_Final = B[0][7] + EBC[0][7]*eta_C - EBD[0][7]*(1/eta_D)
status = prob.solve()

Sobra= {}
for j in Hora:
    Sobra[j] =Ecal [j] + EE[j] * (1-eta_E) * eta_R - EI[j]

print(LpStatus[status])

#print("EI:", [value(EI[j]) for j in Hora])

print("EE:", [value(EE[j]) for j in Hora])
print("PE:", value(PE))
print("EEO:", [value(EEO[j]) for j in Hora])
#print("Viento:", [value(Viento[j]) for j in Hora])
print("PEO:", value(PEO))
#print("Ecal:", [value(Ecal[j]) for j in Hora])
#print("Pcal:", value(Pcal))
print("EBC0:", [value(EBC[0][j]) for j in Hora]) #Hay uno para cada bateria.
print("EBD0:", [value(EBD[0][j]) for j in Hora])
print("B_init", [value(B_init[i]) for i in Baterias])
print("B_Max", [value(B_Max[i]) for i in Baterias])
#print("B1", [value(B[1][j]) for j in Hora])
#print("B2", [value(B[2][j]) for j in Hora])
#print("B3", [value(B[3][j]) for j in Hora])
print("B0", [value(B[0][j]) for j in Hora])
print("PB", [value(PB[i]) for i in Baterias])
#print("CB", [value(CB[i]) for i in Baterias])
#print(Hora[0])
print("Z:", value(Z))
print("Eh:", value(sum([EE[j] for j in Hora]) * eta_E))
#print("Sobra", [value(Sobra[j]) for j in Hora])
print("B_Final", value(B_Final))