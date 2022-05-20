# Modelo de un proceso de ensamble e inspección

'''

Dos barras metálicas de diferente longitud son unidas mediante
un proceso de soldadura para formar una barra de mayor longitud.

La longitud del primer tipo de barra sigue
una distribución uniforme entre 45 y 55 cm.

La longitud del segundo tipo de barra sigue
una distribución 4-Erlang con media de 30 cm.

Las especificaciones del producto final son de 80 ± 10 cm.

Determine el porcentaje de barras fuera de especificación.
'''
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from prng import linear_congruential

data_length = 10000

random_numbers_1er_barra = linear_congruential(1103515245, 12345,
                                                      2 ** 31, 1,
                                                      data_length)
random_numbers_2da_barra = linear_congruential(
    1103515245,
    12345,
    2 ** 31, 3,
    data_length)

longitud_barra_1 = 45 + ((55 - 45) * np.array(random_numbers_1er_barra))

longitud_barra_2 = []

for ri in random_numbers_2da_barra:
    mult = 1
    for _ in range(4):
        mult *= ri
    longitud_barra_2.append(-1*((30 / 4) * np.log(mult)))

df = pd.DataFrame(data={
    'Longitud barra 1': longitud_barra_1,
    'Longitud barra 2': np.array(longitud_barra_2),
})

df['Longitud barra soldada'] = df['Longitud barra 1'] + df['Longitud barra 2']

df['Estado de barra soldada'] = 1
df.loc[(df['Longitud barra soldada'] >= 70) & (df['Longitud barra ' \
                                                  'soldada'] < 90), 'Estado de ' \
                                                                    'barra ' \
                                                                    'soldada'] = 0

probabilidad = []

for i in range(1, len(random_numbers_2da_barra) + 1):
    temp_df = df.iloc[0:i]
    probabilidad.append(temp_df['Estado de barra soldada'].mean())

df['Probabilidad barra fuera specs'] = probabilidad

pd.set_option('display.max_rows', None, 'display.max_columns', None)
print(df.head())

fig, ax = plt.subplots()
ax.plot(df['Probabilidad barra fuera specs'])
plt.show()
