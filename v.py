import math
#import numpy as np
#import pandas as pd
#from matplotlib import pyplot as plt
#from numpy import log

num_personas = 4
tiempo_estancia_min = 15
tiempo_estancia_max = 30
t_llegadas = 20 #promedio de llegadas
total_espacios = 15 # el total de espacios para los clientes

tiemposClientes = total_espacios * [{'llegada' : 0,'servicio' : 0,'salida' : 0, 'espera' : 0}]

te = 0.0  # tiempo de espera total
dt = 0.0  # duracion de servicio total
fin = 0.0  # minuto en el que finaliza

nRandoms = []

def linear_Congruential_Method(Xo, a, c, m, noOfRandomNums):
    randomNums = [0] * (noOfRandomNums )
    randomNums[0] = Xo

    for i in range(1,noOfRandomNums):
        randomNums[i] = round(((randomNums[i-1] * a) + c) % m , 4)


    return randomNums



def estancia(cliente):
    global dt
    global nRandoms

    R = nRandoms[cliente] #random.random() # Obtiene un numero aleatorio y lo guarda en R
    tiempo = tiempo_estancia_max - tiempo_estancia_min 
    tiempo_estancia = tiempo_estancia_min + (tiempo*R) # formula para calcular el tiempo de estancia del cliente 
    tiemposClientes[cliente]['servicio'] = tiempo_estancia
    print("Cliente %s utilizo el servicio %.2f minutos" % (cliente, tiempo_estancia))
    dt += tiempo_estancia
    return tiempo_estancia

#funncion para determinar el minuto de llega y salida del cliente
def cliente(name):
    global te
    global fin
    global nRandoms

    llegada = tiemposClientes[name]['llegada'] 
    print("---> Cliente %s llega al estacionamiento en minuto %.2f" % (name, llegada))

    espera = 0
    if(name > 0):
        if(tiemposClientes[name -1]['salida'] > tiemposClientes[name]['llegada'] ):
            espera = tiemposClientes[name -1]['salida'] - tiemposClientes[name]['llegada']

    te += espera
    print("*** Cliente %s aparcan su auto habiendo esperado %.2f" % (name, espera))
    servicio = estancia(name)
    deja = servicio + llegada
    tiemposClientes[name]['salida'] = deja
    print("<--- Cliente %s deja el estacionamiento en minuto %.2f" % (name, deja))
    fin = deja

if __name__ == "__main__":

    print("....Bienvenido....")
    #random.seed(semilla) # inicializa el generador de números aleatorios

    llegada = 0
    i = 0

    # m,  el módulo
    # a,  el multiplicador
    # c,  el incremento
    # X0 Valor inicial de la secuencia conocido como semilla(seed).

    Xo = 0.7880
    m = 0.7
    a = 0.8
    c = 0.6

    nRandoms = linear_Congruential_Method(Xo, a, c, m, total_espacios)

    for i in range(total_espacios): #se crea una se secuencia de numeros de 0 hasta total_espacios
        R = nRandoms[i] #random.random()
        # math.log(R) -> calcular el logaritmo natural de R 
        llegada += -t_llegadas * math.log(R) # se calcula el tiempo de llegada  
        tiemposClientes[i]['llegada'] = llegada
        cliente(i)

        print("\n")

    #se calcula los promedios obtenidos del servicio total
    lpc = te / fin #tiempo de espera total / la ultima salida del del cliente -> Longitud promedio de la cola
    print("\nLongitud promedio de cola: %.2f" % lpc)
    tep = te / total_espacios #tiempo de espera total / total de espacios -> tiempo de espera promedio
    print("Tiempo de espera promedio = %.2f" % tep)
    upi = (dt / fin) / num_personas  #pocentaje que trabaja el valet parking
    print("Uso promedio del servicio 'Valet Parking' = %.2f" % upi)
    print("\n------------------------------------")
    