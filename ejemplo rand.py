import numpy as np

# Número aleatorio entre 0 y 1 (distribución uniforme)
np.random.rand()
# → 0.5488135 (por ejemplo)

# Arreglo 1D con 5 números aleatorios entre 0 y 1
np.random.rand(5)

# Entero aleatorio entre 0 y 9
np.random.randint(0, 10)

# 3 números aleatorios con distribución normal (media=0, std=1)
np.random.randn(3)

# Permutación aleatoria de una lista
np.random.permutation([1, 2, 3, 4, 5])

# Elegir 3 elementos aleatoriamente de una lista
np.random.choice([10, 20, 30, 40], size=3)

import numpy as np

min_val = 10
max_val = 20
cantidad = 5

valores = np.random.uniform(min_val, max_val, cantidad)
valores_redondeados = np.round(valores, 2)  # redondea a 2 decimales
print(valores_redondeados.tolist())
#print(valores.tolist())  # convierte el resultado a lista de Python
