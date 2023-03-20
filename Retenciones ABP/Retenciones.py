import pandas as pd
import numpy as np
import os

def ProcesarRetenciones():

    #Crear un DataFrame vacío

    Conslidado = pd.DataFrame()

    # cargar todos los XLS de la carpeta 'RET' en el DataFrame

    for file in os.listdir('RET'):
        if file.endswith('.xls'):
            df = pd.read_excel('RET/' + file)
            # Crear columna 'CUIT' con el cuarto elemento entre '-' del nombre del archivo y sacarle los espacios en blanco
            df['CUIT'] = file.split('-')[3].strip()
            df['CUIT'] = df['CUIT'].astype('int64')
            #Crear columna de 'Cliente' con el quinto elemento entre '-' del nombre del archivo y sacarle los espacios en blanco y reemplazar los 'xls' por ''
            df['Cliente'] = file.split('-')[4].strip().replace('.xls', '')
            Conslidado = pd.concat([Conslidado, df], ignore_index=True)

    del df, file

    # Crear una tabla dinámica con el CUIT y el 'Importe Ret./Perc.'
    Consolidado_TD = pd.pivot_table(Conslidado, values='Importe Ret./Perc.', index=['CUIT' , 'Cliente'], aggfunc=np.sum)

    #reinicio el índice para que el 'CUIT' y 'Cliente' sea una columna
    Consolidado_TD = Consolidado_TD.reset_index()

    # Crear un archivo Excel con el resultado
    Consolidado_TD.to_excel("Resultado.xlsx" , index=False)

    return Consolidado_TD

if __name__ == '__main__':
    print(ProcesarRetenciones())

