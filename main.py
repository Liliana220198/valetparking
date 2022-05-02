# VALET PARKING...
# Liliana Flores Ortiz, Alan Alejandro Luna Gonzalez.

import math
import random
import simpy

semilla = 5
num_autos = 1
tiempo_estancia_min = 15
tiempo_estancia_max = 30
t_llegadas = 20
t_simulacion = 120
total_espacios = 20

te = 0.0  # tiempo de espera total
dt = 0.0  # duracion de servicio total
fin = 0.0  # minuto en el que finaliza


def estancia(usuario):
    global dt
    R = random.random()
    tiempo = tiempo_estancia_max - tiempo_estancia_min
    tiempo_estancia = tiempo_estancia_min + (tiempo * R)
    yield env.timeout(tiempo_estancia)
    print("\n Servicio utilizado %s en %.2f minutos" % (usuario, tiempo_estancia))
    dt = dt + tiempo_estancia


def cliente(env, name, personal):
    global te
    global fin
    llegada = env.now  # guarda el minuto de llegada del cliente
    print("---> %s llega al estacionamiento en minuto %.2f" % (name, llegada))
    with personal.request() as request:
        yield request
        acepta = env.now
        espera = acepta - llegada
        te = te + espera
        print("*** %s aparque su auto %.2f habiendo esperado %.2f" % (name, acepta, espera))
        yield env.process(estancia(name))
        deja = env.now
        print("<--- %s deja el estacionamiento en minuto %.2f" % (name, deja))
        fin = deja


def principal(env, personal):
    i = 0
    for i in range(total_espacios):
        R = random.random()
        llegada = -t_llegadas * math.log(R)
        yield env.timeout(llegada)
        i += 1
        env.process(cliente(env, 'Cliente %d' % i, personal))


if __name__ == "__main__":
    print("\n....Bienvenido....\n")
    random.seed(semilla)
    env = simpy.Environment()
    personal = simpy.Resource(env, num_autos)
    env.process(principal(env, personal))
    env.run()
    print("\n------------------------------------")
    print("\nIndicadores obtenidos: ")

    lp = te / fin
    print("\nLongitud promedio: %.2f" % lp)
    tep = te / total_espacios
    print("Tiempo de espera promedio = %.2f" % tep)
    ups = (dt / fin) / num_autos
    print("Uso promedio del servicio 'Valet Parking' = %.2f" % ups)
    print("\n------------------------------------")