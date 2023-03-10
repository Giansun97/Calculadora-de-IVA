import pandas as pd
import os


def calcular_iva_a_pagar(nombre_archivo1, nombre_archivo2):
    # Leemos ambos archivos
    df1 = pd.read_excel(nombre_archivo1,
                        header=1)
    df2 = pd.read_excel(nombre_archivo2,
                        header=1)

    # Sumamos las columnas de iva crédito y débito
    iva_debito = df1['IVA'].sum()
    iva_credito = df2['IVA'].sum()

    # Calculamos el IVA a pagar
    iva_pagar = iva_debito - iva_credito

    # Devolvemos el resultado
    return iva_pagar


#ruta_archivo = input('Ingrese la ruta donde se encuentran guardados los archivos')


def calcular_iva_archivos(ruta_archivo):
    archivos = os.listdir(ruta_archivo)

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
                iva_pagar = calcular_iva_a_pagar(os.path.join(ruta_archivo, archivo_venta),
                                                 os.path.join(ruta_archivo, archivo_compra))
                resultados.append((contribuyente, cuit_venta, round(iva_pagar, 2)))
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

