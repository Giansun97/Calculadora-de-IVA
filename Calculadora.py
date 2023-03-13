import pandas as pd
import numpy as np
import os
from tkinter.filedialog import askdirectory

def calcular_iva_a_pagar(nombre_archivo1, nombre_archivo2):
    # Leemos ambos archivos
    df1 = pd.read_excel(nombre_archivo1,
                        header=1)
    df2 = pd.read_excel(nombre_archivo2,
                        header=1)

    #Multiplicar por tipo de cambio
    df1['IVA'] *= df1['Tipo Cambio']
    df2['IVA'] *= df2['Tipo Cambio']

    #Cambiar de signo si es una Nota de Crédito
    df1.loc[df1["Tipo"].str.contains("Nota de Crédito"), ['IVA']] *= -1
    df2.loc[df2["Tipo"].str.contains("Nota de Crédito"), ['IVA']] *= -1
    
    # Sumamos las columnas de iva crédito y débito
    iva_debito = df1['IVA'].sum()
    iva_credito = df2['IVA'].sum()

    # Calculamos el IVA a pagar
    iva_pagar = iva_debito - iva_credito

    # Devolvemos el resultado
    return iva_pagar


def calcular_iva_archivos():

    # Pedimos la ruta de la carpeta donde están los archivos
    Dirección = askdirectory()
    Ruta = os.path.join(Dirección)
    archivos = os.listdir(Dirección)

    # Filtramos los archivos que sean los de Saldos Iniciales y Retenciones
    archivo_saldos = [archivo for archivo in archivos if 'Saldos' in archivo]
    archivo_retenciones = [archivo for archivo in archivos if 'Retenciones' in archivo]

    #Filtramos los archivos que no sean .xlsx y los que contengas en el nombre Resultados o Saldos o Retenciones
    archivos = [archivo for archivo in archivos if archivo.endswith('.xlsx') and 'Resultados' not in archivo and 'Saldos' not in archivo and 'Retenciones' not in archivo]

    # Creamos listas vacías de archivos_ventas y archivos_compras
    archivos_ventas = []
    archivos_compras = []
    resultados = []

    for archivo in archivos:
        if 'MCE' in archivo:
            archivos_ventas.append(archivo)
        else:
            archivos_compras.append(archivo)

    # Recorremos la lista de archivos de venta y buscamos su cuit
    for archivo_venta in archivos_ventas:
        cuit_venta = archivo_venta.split("-")[3].strip()

        # Recorremos la lista de archivos de compra y buscamos su cuit
        for archivo_compra in archivos_compras:
            cuit_compra = archivo_compra.split("-")[3].strip()
            contribuyente = archivo_compra.split("-")[4].strip().replace('.xlsx', '')

            # Si los cuits coinciden, aplicamos la función calcular_iva_a_pagar
            if cuit_venta == cuit_compra:
                iva_pagar = calcular_iva_a_pagar(os.path.join(Ruta, archivo_venta),
                                                 os.path.join(Ruta, archivo_compra))
                resultados.append((contribuyente, cuit_venta, round(iva_pagar, 2)))

    #Leemos el archivo de Saldos Iniciales
    df_saldos = pd.read_excel(os.path.join(Ruta, archivo_saldos[0]))
    df_saldos['CUIT'] = df_saldos['CUIT'].astype(np.int64)
    
    # Leemos el archivo de Retenciones
    df_retenciones = pd.read_excel(os.path.join(Ruta, archivo_retenciones[0]))
    df_retenciones['CUIT'] = df_retenciones['CUIT'].astype(np.int64)

    # Sumar las columnas de 'RET IVA1' y 'RET IVA2' en la columan 'RET IVA'
    df_retenciones['RET IVA'] = df_retenciones['RET IVA1'] + df_retenciones['RET IVA2']

    #Exportamos los resultados a un archivo excel en la misma carpeta que los archivos
    resultados_df = pd.DataFrame(resultados, columns=['Contribuyente', 'CUIT', 'IVA a pagar'])
    resultados_df['CUIT'] = resultados_df['CUIT'].astype(np.int64)

    #Agregamos las columnas de Saldos Iniciales y Retenciones a los resultados con merge en base al CUIT
    resultados_df = pd.merge(resultados_df, 
                             df_saldos[['CUIT' , 'Saldo Primer Párrafo' , 'Saldo Segundo Párrafo']], 
                             on='CUIT', 
                             how='left')

    resultados_df = pd.merge(resultados_df,
                             df_retenciones[['CUIT', 'RET IVA']],
                             on='CUIT',
                             how='left')
    
    resultados_df = resultados_df.fillna(0)

    # Calculos en Resultados

    # Sumar las columnas de 'Saldo Segundo Párrafo' y 'RET IVA' en la columan 'Saldo Segundo Párrafo'
    resultados_df['Saldo Segundo Párrafo'] = resultados_df['Saldo Segundo Párrafo'] + resultados_df['RET IVA']
    del resultados_df['RET IVA']


    ## Si el 'IVA a pagar' < 'Saldo Primer Párrafo', se paga la totalidad del 'IVA a pagar' con el 'Saldo Primer Párrafo'
    # Crear columna temporal 'Temp Pagar < 1P'
    resultados_df['Temp Pagar < 1P'] = False

    # Si el 'IVA a pagar' < 'Saldo Primer Párrafo', 'Temp Pagar < 1P' es igual a Verdadero
    resultados_df.loc[resultados_df['IVA a pagar'] < resultados_df['Saldo Primer Párrafo'], 'Temp Pagar < 1P'] = True

    # Si 'Temp Pagar < 1P' es Verdadero, el 'Saldo Primer Párrafo' = 'Saldo Primer Párrafo' - 'IVA a pagar'
    resultados_df.loc[resultados_df['Temp Pagar < 1P'] == True, 'Saldo Primer Párrafo'] = (resultados_df.loc[resultados_df['Temp Pagar < 1P'] == True, 'Saldo Primer Párrafo'] - 
                                                                                          resultados_df.loc[resultados_df['Temp Pagar < 1P'] == True, 'IVA a pagar'])
    
    # Si 'Temp Pagar < 1P' es Verdadero, el 'IVA a pagar' = 0
    resultados_df.loc[resultados_df['Temp Pagar < 1P'] == True, 'IVA a pagar'] = 0

    # Si 'Temp Pagar < 1P' es Falso, el 'IVA a pagar' = 'IVA a pagar' - 'Saldo Primer Párrafo'
    resultados_df.loc[resultados_df['Temp Pagar < 1P'] == False, 'IVA a pagar'] = (resultados_df.loc[resultados_df['Temp Pagar < 1P'] == False, 'IVA a pagar'] -
                                                                                      resultados_df.loc[resultados_df['Temp Pagar < 1P'] == False, 'Saldo Primer Párrafo'])
    
    # Si 'Temp Pagar < 1P' es Falso, el 'Saldo Primer Párrafo' = 0
    resultados_df.loc[resultados_df['Temp Pagar < 1P'] == False, 'Saldo Primer Párrafo'] = 0

    # Eliminar columna temporal 'Temp Pagar < 1P'
    del resultados_df['Temp Pagar < 1P']



    ## Si el 'IVA a pagar' < 'Saldo Segundo Párrafo', se paga la totalidad del 'IVA a pagar' con el 'Saldo Segundo Párrafo'
    # Crear columna 'Temp Pagar < 2P'
    resultados_df['Temp Pagar < 2P'] = False

    #Si el 'IVA a apgar' < 'Saldo Segundo Párrafo', 'Temp Pagar < 2P' es Verdadero
    resultados_df.loc[resultados_df['IVA a pagar'] < resultados_df['Saldo Segundo Párrafo'], 'Temp Pagar < 2P'] = True

    #si 'Temp Pagar < 2P' es Verdadero, el 'Saldo Segundo Párrafo' = 'Saldo Segundo Párrafo' - 'IVA a pagar'
    resultados_df.loc[resultados_df['Temp Pagar < 2P'] == True, 'Saldo Segundo Párrafo'] = (resultados_df.loc[resultados_df['Temp Pagar < 2P'] == True, 'Saldo Segundo Párrafo'] - 
                                                                                          resultados_df.loc[resultados_df['Temp Pagar < 2P'] == True, 'IVA a pagar'])
    
    #si 'Temp Pagar < 2P' es Verdadero, el 'IVA a pagar' = 0
    resultados_df.loc[resultados_df['Temp Pagar < 2P'] == True, 'IVA a pagar'] = 0

    #si 'Temp Pagar < 2P' es Falso, el 'IVA a pagar' = 'IVA a pagar' - 'Saldo Segundo Párrafo'
    resultados_df.loc[resultados_df['Temp Pagar < 2P'] == False, 'IVA a pagar'] = (resultados_df.loc[resultados_df['Temp Pagar < 2P'] == False, 'IVA a pagar'] -
                                                                                        resultados_df.loc[resultados_df['Temp Pagar < 2P'] == False, 'Saldo Segundo Párrafo'])
    
    #si 'Temp Pagar < 2P' es Falso, el 'Saldo Segundo Párrafo' = 0
    resultados_df.loc[resultados_df['Temp Pagar < 2P'] == False, 'Saldo Segundo Párrafo'] = 0

    # Eliminar columna temporal 'Temp Pagar < 2P'
    del resultados_df['Temp Pagar < 2P']


    # Exportar resultados a Excel
    resultados_df.to_excel(os.path.join(Ruta, 'Resultados.xlsx'), index=False)
            
    return resultados_df

if __name__ == '__main__':
    calcular_iva_archivos()

    