#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json

PATH_TO_JSON = './file_list.json'


def isInList(hash):
    for k in jsonRead():
        if k == hash:
            return True
        else:
            False


def addToList(name, hash):
    json = jsonRead()
    json.update({hash : name})
    return json


def jsonRead():
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
    with open(PATH_TO_JSON, 'w') as salida:
        salida.write(json.dumps(json_data, sort_keys=True, indent=4, separators=(',', ': ')))

