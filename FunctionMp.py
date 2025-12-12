import numpy as np
from pulp import *

#Generacion solar 1kW seguimiento en 1 eje HSAT 19/4/16
#Rad = [0,0,0,0,0,0,0.5664,0.6542,0.693,0.7073,0.7137,0.714,0.7127,0.705,0.7017,0.6866,0.658,0.5968,0.4617,0,0,0,0,0]
Rad=[0,0,0,0,0,0,0,0,0.39,0.5252,0.5649,0.5524,0.5291,0.5236,0.5359,0.5548,0.538,0.4497,0.1465,0,0,0,0,0]

#Necesidad en kW del invernadero
#EI=[10,5.1737,4.8947,4.5343,0.3615,6.0981,3.7066,3.8197,2.9831,2.152,0,0,0,0,0,0,0,0,0,0,0,0.46364,0.88176,1.5069]
EI=[6.09,4.33,0.55,6.32,2.65,6.53,5.64,2.99,3.09,2.32,0.93,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


#Seed
#np.random.seed(32)

def Sinergias (EI,Rad):

    #necesito que calcule la meta de hidrogeno en base al EI
    EH_min=sum(EI)/0.8 #kWh/dia
    #maximo de calor aprovechable del electrolizador
    Cal=[None, 0, None]
    resultados = []
    #valores de eficiencia del recuperador de calor
    indice=[0,1,2]
    XRec=[0.7,0.8,0.9]
    Xr=np.random.choice(indice) #recuperador de calor
    Rec=[0, XRec[Xr], XRec[Xr]] 

    #Posibles eta_E
    Xeta_E=[0.3,0.5,0.7]
    Xe=np.random.choice(indice)

    #Posible eta_C, eficiencia de carga
    Xeta_C=[0.92,0.95,0.97]
    Xc=np.random.choice(indice)

    #Posible fracc_M
    Xfracc_M=[0.85,0.9,0.95]
    Xf=np.random.choice(indice)

    #Posible fracc_m
    Xfracc_m=[0.05,0.1,0.15]
    Xfm=np.random.choice(indice)

    #posible CE
    XCE=[3500000, 3865987.5, 4000000]
    Xce=np.random.choice(indice)

    #posible CPV
    XCPV=[200000, 245455, 300000]
    Xcpv=np.random.choice(indice)

    #posible Ccal
    XCAL=[75000, 100000, 150000]
    Xcal=np.random.choice(indice)

    #Posibles costos de baterias
    XCB0=[986699.7, 590850.0, 392924.7, 293962.5, 244481.4]
    XCB1=[1096333, 656500, 436583, 326625,271646]
    XCB2=[1205966.3, 722150.0, 480241.3, 359287.5, 298810.6]

    XCBM=[XCB0, XCB1, XCB2]
    Xcb=np.random.choice(indice)

    for a in range(len(Cal)):
        Hora = range(24)# Horas va desde 0 a x-1. 
        Baterias = range(5)

        eta_E = Xeta_E[Xe] #Eficiencia de electrolisis
        eta_R = Rec[a]
        eta_C = Xeta_C[Xc]
        eta_D = 1

        fracc_M=Xfracc_M[Xf] #se desactiva en 1
        fracc_m=Xfracc_m[Xfm] #se desactiva en 0

        #Costos por kW instalado. 
        CE = XCE[Xce] #Costo por kW de EL 4.1 #Es de notar que puede ser problematico si la produccion es de menos de 2.4kW por hora.
        CPV = XCPV[Xcpv]
        Ccal = XCAL[Xcal]
        CB = XCBM[Xcb]### costo asosiado a cada bateria.

        Duración = [4, 2, 1, 0.5, 0.25]

        EE = LpVariable.dicts("EE", (Hora), 0, None)
        PE = LpVariable("PE", 0, None)

        EPV = LpVariable.dicts("EPV", (Hora), 0, None)
        PPV = LpVariable("PPV", 0, None)

        Ecal = LpVariable.dicts("Ecal", (Hora), 0, Cal[a]) #En el caso conjunto su maximo es 0.
        Pcal = LpVariable("Pcal", 0, None)

        EBC = LpVariable.dicts("EBC", (Baterias, Hora), 0, None)
        EBD = LpVariable.dicts("EBD", (Baterias, Hora), 0, None)
        PB = LpVariable.dicts("PB", (Baterias), 0, None)

        B = LpVariable.dicts("B", (Baterias, Hora), 0, None)
        B_Max = LpVariable.dicts("B_Max", (Baterias), 0, None)
        B_init = LpVariable.dicts("B_init", (Baterias), 0, None)

        Eh= LpVariable("Eh", EH_min, None) #en el caso conjunto el minimo es 0, tiene que estar en kW.


        prob = LpProblem("myProblem", LpMinimize)

        #Estoy usando radiacion por eficiencia del panel para definir el maximo posible por kW instalado.
        # Restricción Naturaleza PV
        for j in Hora:
            prob += EPV[j] <= PPV * Rad[j]
            prob += 0 <= EPV[j]                    

        # Restricción Necesidad de invernadero
        for j in Hora:
            prob += Ecal[j] + EE[j] * (1-eta_E) * eta_R >= EI[j]

        # Restricción Equilibrio de potencias
        for j in Hora:
            prob += EPV[j] + sum([EBD[i][j] for i in Baterias]) == Ecal[j] + EE[j] + sum([EBC[i][j] for i in Baterias])

        # Restricción Hidrógeno.
        prob += sum([EE[j] for j in Hora]) * eta_E == Eh

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
                prob += B_Max[i]==PB[i]*Duración[i]

        # Restricción Estado de carga
        for i in Baterias:
            for j in Hora:    
                if j==len(Hora)-1:        #Esta restriccion hace que la hora final sea igual a la hora inicial
                    #break                                                                           
                    prob += B_init[i] == B[i][j] + EBC[i][j]*eta_C - EBD[i][j]*(1/eta_D) #Aqui para mis fines es mejor que la carga final sea mayor o igual a la inicial.
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
        prob += PE*CE + sum([PB[i]*CB[i] for i in Baterias]) + PPV*CPV + Pcal*Ccal

        status = prob.solve()

        Sobra= {}
        for j in Hora:
            Sobra[j] =Ecal [j] + EE[j] * (1-eta_E) * eta_R - EI[j]


        #print(LpStatus[status])

        #print("EI:", [value(EI[j]) for j in Hora])

        #print("EE:", [value(EE[j]) for j in Hora])
        #print("PE:", value(PE))
        #print("EPV:", [value(EPV[j]) for j in Hora])
        #print("Rad:", [value(Rad[j]) for j in Hora])
        #print("PPV:", value(PPV))
        #print("Ecal:", [value(Ecal[j]) for j in Hora])
        #print("Pcal:", value(Pcal))
        #print("EBC0:", [value(EBC[0][j]) for j in Hora]) #Hay uno para cada bateria.
        #print("EBD0:", [value(EBD[0][j]) for j in Hora])
        #print("B_init", [value(B_init[i]) for i in Baterias])
        #print("B1", [value(B[1][j]) for j in Hora])
        #print("B2", [value(B[2][j]) for j in Hora])
        #print("B3", [value(B[3][j]) for j in Hora])
        #print("B0", [value(B[0][j]) for j in Hora])
        #print("PB", [value(PB[i]) for i in Baterias])
        #print("CB", [value(CB[i]) for i in Baterias])
        Z=PE*CE + sum([PB[i]*CB[i] for i in Baterias]) + PPV*CPV + Pcal*Ccal

        #Y= value(Z)

        #resultadito = np.round(Y, 2)

        #print(Hora[0])
        resultados.append(value(Z))
        #print("Eh:", value(Eh))
        #print("EH_min:", EH_min)
        #print("Sobra", [value(Sobra[j]) for j in Hora])
    #print("Z:", resultados)
    Base=resultados[0]
    Conjunto=resultados[1]
    Hibrido=resultados[2]
    SinergiaC=(Base-Conjunto)*100/Base
    SinergiaH=(Base-Hibrido)*100/Base
    #registro de los inputs.
    CB_list = XCBM[Xcb]
    inputs = [
        Xeta_E[Xe], Xeta_C[Xc], XRec[Xr], Xfracc_M[Xf], Xfracc_m[Xfm],
        XCE[Xce], XCPV[Xcpv], XCAL[Xcal],
        *CB_list
    ]
    return SinergiaH, SinergiaC, Base, inputs, Conjunto, Hibrido

Sinergias (EI,Rad)