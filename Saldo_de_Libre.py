import pandas as pd
import os
import numpy as np


def suma_retenciones(nombre_archivo):
    # Leemos el archivo de retenciones
    df1= pd.read_excel(nombre_archivo, 
                       usecols=["Importe Ret./Perc."])

    # Sumamos la columna Importe Ret./Perc.
    total_ret = df1['Importe Ret./Perc.'].sum()

    # Devolvemos el total de retenciones y percepciones del periodo.
    return total_ret


def retenciones_por_contrib(ruta_archivo_ret, cuit):
    # Leemos los archivos que se encuentran en la direccion
    archivos_ret = os.listdir(ruta_archivo_ret)

    # Creamos una lista vacia para almacenar los resultados luego.
    resultados_ret = []

    for archivo_ret in archivos_ret:
            # Extraigo el cuit del contribuyente del nombre del archivo.
            cuit_ret = archivo_ret.split("-")[3].strip()

            if cuit_ret == cuit:
                # Extraigo el nombre del contribuyente del nombre del archivo.
                contribuyente = archivo_ret.split("-")[4].strip().replace('.xls', '')

                # Aplico la funcion de sumar retenciones al archivo
                suma_ret = suma_retenciones(os.path.join(ruta_archivo_ret, archivo_ret))

                # Concateno los resultados en una lista
                resultados_ret.append((contribuyente, cuit_ret, round(suma_ret, 2)))

    # Devolvemos los resultados.
    return print(resultados_ret)

# retenciones_por_contrib('./Retenciones')

df_saldo_anterior = pd.read_excel('Saldos a favor periodo anterior.xlsx')
#print(df_saldo_anterior)

df_saldo_anterior['Cuit'] = df_saldo_anterior['Cuit'].astype(np.int64)

