#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json

PATH_TO_JSON = './file_list.json'


def isInList(hash):
    '''
    Comprueba si una cancion esta en la lista de canciones
    descargadas comparando su hash.
    '''
    for k in jsonRead():
        if k == hash:
            return True
        else:
            False


def addToList(name, hash):
    '''
    Actualiza la lista de canciones descargadas con el
    nombre y hash de la nueva cancion.
    '''
    json = jsonRead()
    json.update({hash: name})
    return json


def jsonRead():
    '''
    Lee un archivo JSON el cual contiene la lista de
    canciones descargadas y lo devuelve como un objeto
    JSON.
    Si no se encuentra el archivo, el metodo creara uno
    nuevo y se llamara a si mismo para leerlo y devolverlo
    una vez creado.
    '''
    data = None
    try:
        with open(PATH_TO_JSON) as json_file:
            data = json.load(json_file)
        return data
    except Exception:
        print('\nArchivo JSON no encontrado.')
        with open(PATH_TO_JSON, 'w') as file:
            file.write('{}')
        return jsonRead()


def jsonWrite(json_data):
    '''
    Escribe en el archivo JSON los cambios efectuados
    por los orchestrators con respecto a la lista de
    canciones descargadas.
    '''
    with open(PATH_TO_JSON, 'w') as salida:
        salida.write(json.dumps(json_data, sort_keys=True, indent=4, separators=(',', ': ')))
