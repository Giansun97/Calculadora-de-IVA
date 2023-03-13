import pandas as pd
import os
import numpy as np

def calcular_iva_a_pagar(nombre_archivo1, nombre_archivo2):
    # Leemos ambos archivos
    df1 = pd.read_excel(nombre_archivo1,
                        header=1)
    df2 = pd.read_excel(nombre_archivo2,
                        header=1)

    # Multiplicar por tipo de cambio
    df1['IVA'] *= df1['Tipo Cambio']
    df2['IVA'] *= df2['Tipo Cambio']

    # Si él data frame esta vació cambio los NaN por espacios en blanco.
    df1['Tipo'].fillna("", inplace=True)  
    df2['Tipo'].fillna("", inplace=True)  

    # Cambiar de signo si es una Nota de Crédito
    df1.loc[df1["Tipo"].str.contains("Nota de Crédito"), ['IVA']] *= -1
    df2.loc[df2["Tipo"].str.contains("Nota de Crédito"), ['IVA']] *= -1

    # Sumamos las columnas de iva crédito y débito
    iva_debito = df1['IVA'].sum()
    iva_credito = df2['IVA'].sum()

    # Calculamos el IVA a pagar
    iva_pagar = iva_debito - iva_credito

    # Devolvemos el resultado
    return iva_pagar




def calcular_iva_archivos(ruta_archivo, ruta_retenciones, archivo_saldos):
    archivos = os.listdir(ruta_archivo)
    archivos_retenciones = os.listdir(ruta_retenciones)

    # Creamos listas vacías de archivos_ventas y archivos_compras
    archivos_ventas = []
    archivos_compras = []
    resultados = []

    # Leer el archivo de saldos a favor
    saldos_anteriores = pd.read_excel(archivo_saldos)

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
                iva_pagar = calcular_iva_a_pagar(os.path.join(ruta_archivo, archivo_venta),
                                                 os.path.join(ruta_archivo, archivo_compra))
                
                # Buscamos el archivo de retenciones correspondiente al cuit
                for archivo_retencion in archivos_retenciones:
                    cuit_retencion = archivo_retencion.split("-")[3].strip()
                    
                    # Si el cuit coincide, sumamos el importe de la columna "Importe Ret./Perc."
                    if cuit_venta == cuit_retencion:
                        ruta_archivo_retencion = os.path.join(ruta_retenciones, archivo_retencion)
                        df_retencion = pd.read_excel(ruta_archivo_retencion)
                        importe_retencion = df_retencion['Importe Ret./Perc.'].sum()

                print(saldos_anteriores['Cuit'])
                print(cuit_venta)
                saldo_tecnico = saldos_anteriores.loc[saldos_anteriores['Cuit'] == cuit_venta]['Saldo 1er P'].values
                 

                #Devolvemos los resultados
                resultados.append((contribuyente, cuit_venta, round(iva_pagar, 2), importe_retencion, saldo_tecnico))

    return resultados

# resultados = calcular_iva_archivos(ruta_archivo)
# for resultado in resultados:
#     contribuyente, cuit_venta, iva_pagar = resultado
#     if iva_pagar > 0:
#         print(f'El contribuyente {contribuyente} con cuit {cuit_venta} debe pagar ${round(abs(iva_pagar), 2)} de '
#               f'IVA.')
#     else:
#         print(f'El contribuyente {contribuyente} con cuit {cuit_venta} tiene ${round(abs(iva_pagar), 2)} de '
#               f'saldo a favor de IVA.')
