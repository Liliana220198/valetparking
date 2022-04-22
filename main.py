# VALET PARKING...

import random
import math
import simpy

seed = 5
num_autos = 6
tiempo_estancia_min = 15
tiempo_estancia_max = 120
t_llegadas = 20
t_simulacion = 120
total_clientes_aceptan = 54
total_clientes_no_aceptan = 120

te = 0.0
dt = 0.0
fin = 0.0