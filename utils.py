#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json

PATH_TO_JSON = './file_list.json'


def appendProxyToFile(proxy):
    tmp_proxy_file = open("/tmp/trawlnet_proxylist", "a+")
    tmp_proxy_file.write(proxy + '\n')


def readProxyfile():
    proxy_array = []
    with open('/tmp/trawlnet_proxylist') as proxy_list_file:
        for line in proxy_list_file:
            proxy_array.append(line.rstrip('\n'))
    return proxy_array


def isInList(hash):
    json = jsonRead()
    for stored_songs in json['canciones']:
        if stored_songs['hash'] == hash:
            return True
        else:
            False


def addToList(name, hash):
    json = jsonRead()
    json['canciones'].append({'name': name, 'hash': hash})
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

