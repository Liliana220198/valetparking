# variables

# demanda  # distribucion exponencial *
# dia = 0 *
# dia_pedido = dia % 7 == 0 *
# capacidad = 700 *
# cantidad_pedido = capacidad - invetario_final[i-1] *
# inventario_inicial = cantidad_pedido + inventario_final[i-1] *
# venta = perdida > 0 ? inventario_inicial : demanda *
# inventario_final = max(0,inventario_inicial - demanda) *
# perdida = demanda - inventario_inicial *
# costo_por_ordenar = dia % 7 == 0 ? 1000 : 0 *
# costo_por_faltante = 6*perdida *
# costo_por_inventario = 1*(inicial_inventario+final_inventario)/2 *
# costo_total = costo_por_ordenar + costo_por_faltante + costo_por_inventario *
# costo_por_kilo = 22
# ganancia = venta * costo_por_kilo
# utilidad = ganacia - costo_total
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from numpy import log

from prng import linear_congruential

dias = 60
capacidad = 700
costo_por_kilo = 22

random_numbers = \
    np.array(linear_congruential(1103515245, 12345, 2 ** 31, 1, dias))
demanda = -100 * log(1 - random_numbers)


dataframe = pd.DataFrame(data={
    'Demanda': demanda,
})

dias_pedido = dataframe.index % 7 == 0

dataframe['Pedido'] = 0
dataframe.loc[0, 'Pedido'] = capacidad
dataframe.loc[0, 'Inventario inicial'] = dataframe.loc[0, 'Pedido']
dataframe.loc[0, 'Inventario final'] = \
    dataframe.loc[0, 'Inventario inicial'] - dataframe.loc[0, 'Demanda']

for (index, row) in dataframe.iterrows():
    if index == 0:
        continue
    if index % 7 == 0:
        dataframe.loc[index, 'Pedido'] = \
            capacidad - dataframe.loc[index - 1, 'Inventario final']
    dataframe.loc[index, 'Inventario inicial'] = \
        dataframe.loc[index, 'Pedido'] \
        + dataframe.loc[index - 1, 'Inventario final']
    dataframe.loc[index, 'Inventario final'] = \
        max(0, dataframe.loc[index, 'Inventario inicial'] -
            dataframe.loc[index, 'Demanda'])

perdida = dataframe['Demanda'] - dataframe['Inventario inicial']
dataframe['Perdida'] = 0
dataframe.loc[perdida > 0, 'Perdida'] = perdida

dataframe.loc[dataframe['Perdida'] > 0, 'Venta real'] \
    = dataframe['Inventario inicial']
dataframe.loc[dataframe['Perdida'] == 0, 'Venta real'] = dataframe['Demanda']

dataframe['Ganancia'] = 0
dataframe.loc[dataframe['Perdida'] == 0,'Ganancia'] = \
    dataframe['Venta real'] * costo_por_kilo

dataframe['Costo por orden'] = 0

dataframe.loc[dias_pedido, 'Costo por orden'] = 1000

dataframe['Costo por perdida'] = 6 * dataframe['Perdida']

dataframe['Costo por inventario'] = (dataframe['Inventario inicial'] +
                                     dataframe['Inventario final']) / 2

dataframe['Costo total'] = dataframe['Costo por orden'] + \
                           dataframe['Costo por perdida'] + \
                           dataframe['Costo por inventario']

dataframe['Utilidad'] = dataframe['Ganancia'] - dataframe['Costo total']
costo_promedio = []
utilidad_promedio = []
for i in range(1, dias + 1):
    temp_df = dataframe.iloc[0:i]
    utilidad_promedio.append(temp_df['Utilidad'].mean())
    costo_promedio.append(temp_df['Costo total'].mean())

dataframe['Costo promedio'] = costo_promedio
dataframe['Utilidad promedio'] = utilidad_promedio

pd.set_option('display.max_rows', None, 'display.max_columns', None)
print(dataframe[['Pedido', 'Inventario inicial',
                 'Demanda', 'Venta real',
                 'Inventario final', 'Ganancia', 'Perdida',
                 'Costo por orden', 'Costo por perdida',
                 'Costo por inventario', 'Costo total','Utilidad',
                 'Costo promedio', 'Utilidad promedio']].head(60))

fig, ax = plt.subplots()
ax.plot(dataframe['Utilidad promedio'])
plt.show()
