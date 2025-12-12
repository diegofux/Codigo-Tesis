import numpy as np
from pulp import *
from Function1 import Sinergias
#Generacion solar 1kW seguimiento en 2 ejes 1/1/24
Rad = [0,0,0,0,0,0,0.5664,0.6542,0.693,0.7073,0.7137,0.714,0.7127,0.705,0.7017,0.6866,0.658,0.5968,0.4617,0,0,0,0,0]

#Necesidad en kW del invernadero
EI=[10,5.1737,4.8947,4.5343,0.3615,6.0981,3.7066,3.8197,2.9831,2.152,0,0,10,0,0,0,0,0,0,0,0,0.46364,0.88176,1.5069]


SinergiaH, SinergiaC = Sinergias (EI,Rad)
print("SinergiaH:", SinergiaH+1)
print("SinergiaC:", SinergiaC)