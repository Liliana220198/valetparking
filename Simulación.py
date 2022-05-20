# Simular modelo de una linea de espera con un servidor

"""
El tiempo que transcurre entre la llegada de piezas a una estacion de inspeccion tiene una distribucion exponencial con media 5 minutos/pieza.

El proceso esta a cargo de un operario, y tarda en inspeccionar con una distribucion normal con media de 4 y desviacion estandar de 0.5 minutos/pieza.

Cual es el tiempo promedio de permanencia de la piezas en inspeccion
"""
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from numpy import log

from prng import linear_congruential

dfs = []

for index_replica in range(10):
    data_length = 10000

    random_numbers = linear_congruential(1103515245, 12345,
                                         2 ** 31, index_replica,
                                         data_length)

    data = np.array(random_numbers)

    llegada_de_piezas = -5 * log(1 - data)


    llegadas = []
    acum = 0
    for i in range(data_length):
        llegadas.append(acum + llegada_de_piezas[i])
        acum += llegada_de_piezas[i]


    inspeccion = []
    for ri in random_numbers:
        sum = 0
        for i in range(12):
            sum += ri
        inspeccion.append(((sum - 6) * 0.5) + 4)

    df = pd.DataFrame(
        data={'Tiempo entre llegadas': llegada_de_piezas, 'Llegadas': llegadas,
              'Tiempo en espera': 0, 'Inspeccion': inspeccion})

    for (index,row) in df.iterrows():
        if index == 0:
            tiempo_anterior = row['Inspeccion'] + row['Llegadas']
            continue
        if row['Llegadas'] > tiempo_anterior:
            df.loc[index,'Tiempo en espera'] = 0
        else:
            df.loc[index,'Tiempo en espera'] = tiempo_anterior - row['Llegadas']
        df.loc[index,'Operario en espera'] = abs(row['Llegadas'] + df.loc[index,
                                                                      'Tiempo en ' \
                                                                      'espera'] -\
                                             tiempo_anterior)
        tiempo_anterior = row['Inspeccion'] + df.loc[index,'Tiempo en espera'] + row[
            'Llegadas']

    df['Fin de inspeccion'] = df['Inspeccion'] + df['Tiempo en espera'] + df['Llegadas']

    df['Inicio de Inspeccion'] = df['Llegadas'] + df['Tiempo en espera']

    df['Tiempo en inspeccion'] = df['Fin de inspeccion'] - df['Llegadas']

    tiempo_promedio = []

    for i in range(1,data_length+1):
        temp_df = df.iloc[0:i]
        tiempo_promedio.append(temp_df['Tiempo en inspeccion'].mean())

    df['Tiempo Promedio'] = pd.Series(tiempo_promedio)
    fig, ax = plt.subplots()
    ax.plot([dframe.iloc[10000 - 1]['Tiempo Promedio'] for dframe in dfs])
    plt.show()
    dfs.append(df)

print([dframe.iloc[10000-1]['Tiempo Promedio'] for dframe in dfs])

fig, ax = plt.subplots()
ax.plot([dframe.iloc[10000-1]['Tiempo Promedio'] for dframe in dfs])
plt.show()