import pandas as pd
import os


def suma_retenciones(nombre_archivo):
    #Leemos el archivo de retenciones
    df1= pd.read_excel(nombre_archivo)

    # Sumamos la columna Importe Ret./Perc.
    total_ret = df1['Importe Ret./Perc.'].sum()

    # Devolvemos el total de retenciones y percepciones del periodo.
    return total_ret


def retenciones_por_contrib(ruta_archivo_ret):
    archivos_ret = os.listdir(ruta_archivo_ret)
    resultados_ret = []

    for archivo_ret in archivos_ret:
            cuit = archivo_ret.split("-")[3].strip()
            contribuyente = contribuyente = archivo_ret.split("-")[4].strip().replace('.xlsx', '')

            suma_ret = suma_retenciones(os.path.join(ruta_archivo_ret, archivo_ret))

            resultados_ret.append((cuit, contribuyente, suma_ret))

    return resultados_ret

retenciones_por_contrib('./Retenciones')

SLD_anterior= pd.read_excel('Saldos a favor periodo anterior.xlsx')
