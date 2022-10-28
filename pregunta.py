"""
Ingestión de datos - Reporte de clusteres
-----------------------------------------------------------------------------------------

Construya un dataframe de Pandas a partir del archivo 'clusters_report.txt', teniendo en
cuenta que los nombres de las columnas deben ser en minusculas, reemplazando los espacios
por guiones bajos; y que las palabras clave deben estar separadas por coma y con un solo 
espacio entre palabra y palabra.


"""
import pandas as pd

import re

def limpieza(posicion,linea):
    #limpiar el encabezado de las columnas
    if posicion==0:
        linea = [re.split(r'[ ]{2,}', element.strip())
                for element in linea.split('\n')]
        linea[1].insert(0,'')
        linea[1].append('')
        linea = [(a+' '+b).strip().lower() for a,b in zip(linea[0],linea[1])]
        linea = [element.replace(' ', '_') for element in linea]

    else:
        #limpiar las filas (clusters)
        linea = re.sub('[-]+\n', '', linea)
        linea = re.split(r'[ ]{4,}', linea)
        linea[3] = ' '.join(linea[3:])
        linea[3] = linea[3].replace('\n', ' ')
        linea[3] = re.sub('\s+',' ',linea[3]).replace('.', '')
        linea = linea[0:4]
        linea[2] =linea[2].split(' ')[0]
        linea = [l.strip() for l in linea]

    return linea


def ingest_data():

    #
    # Inserte su código aquí
    #
    with open("clusters_report.txt") as file:
        # Load data
        df = file.read()
        df = re.sub('\n\s+\n', '\n\n', df) # Check problem with line-cluster 9
        df = df.split('\n\n')[:-1]

        # Cleaning data
        df = [limpieza(posicion, linea) for posicion, linea in enumerate(df)]
        df = pd.DataFrame(df, columns=df[0]).drop(0)
        df.iloc[:,2] = df.iloc[:,2].str.replace(',','.')
        types = {
            'cluster':int,
            'cantidad_de_palabras_clave': int,
            'porcentaje_de_palabras_clave': float,
            'principales_palabras_clave':str
        }
        df = df.astype(types)
    return df
