#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, json

PATH_TO_JSON = './file_list.json'

def isInList(hash):
    json = jsonRead()
    for stored_songs in json['canciones']:
        if stored_songs['hash'] == hash:
            return True
        else:
            False
            
def addToList(name, hash):
    json = jsonRead()
    json['canciones'].append({'name' : name, 'hash' : hash})
    return json
    
def jsonRead():
    try:
        with open(PATH_TO_JSON) as json_file:
            data = json.load(json_file)
        return data
    except Exception:
        print('\nArchivo JSON no encontrado.')
        with open(PATH_TO_JSON, 'w') as file:
            file.write('{"canciones": []}')
        return []
            

def jsonWrite(json_data):
    with open(PATH_TO_JSON, 'w') as salida:
        salida.write(json.dumps(json_data, sort_keys=True,indent=4, separators=(',', ': ')))

