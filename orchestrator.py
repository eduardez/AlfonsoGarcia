#!/usr/bin/python3
# -*- coding: utf-8 -*-

#en el archivo config poner IceConfig.IPvVersion = 4 para librarnos de las ipv 6

import sys
from pathlib import Path as path
import Ice, IceStorm
Ice.loadSlice('TrawlNet.ice')
import TrawlNet 


class OrchestratorI(TrawlNet.Orchestrator):
    ''' Sirviente del Orchestrator '''
    downloader = None
    
    def downloadTask (self, url, current=None):
        print('Peticion de descarga, url: %s' % url)
        hash = ''
        from youtube_dl import YoutubeDL
        with YoutubeDL() as youtube:
            info = youtube.extract_info(url, download=False)
            hash = info.get("id", None)
        if self.isInList(hash=hash):
            print('ERROR*** Cancion ya descargada.')
        else:
            print('Descargando cancion.')
            if self.downloader is not None:
                file_info = self.downloader.addDownloadTask(url)
                self.addToList(file_info=file_info)
                return file_info

    def getFileList(self, current=None):
        print("Peticion de informacion de archivos disponibles")
        try:  
            list_file = []
            archivo = None
            with open('./file_list.txt', 'r') as f:
                archivo = f.readlines()
                
            for num_line in range(0, len(archivo)):
                file_info = TrawlNet.FileInfo()
                if (num_line % 2) == 0:
                    file_info.name = archivo[num_line]
                    file_info.hash = archivo[num_line + 1]
                    list_file.append(file_info)
            return list_file
        except FileExistsError:
            print('ERROR*** No existe la lista de archivos descargados.')
            return []
    
    def isInList(self, current = None, hash = None):
        archivo = './file_list.txt'
        objeto_archivo = path(archivo)
        if objeto_archivo.exists():
            with open(archivo, 'r') as f:
                if hash == f.readline()[:-1]:
                    #Acceder al orchestrator correcto y devolver el fichero
                    print("Ese fichero ya esta descargado")
                    return True
        else:
            return False
        
    def addToList(self, current = None, file_info = None):
        with open('./file_list.txt', 'a+') as f:
            f.write(file_info.name + '\n')
            f.write(file_info.hash + '\n')

    def announce(self, other_orchestrator):
        raise NotImplementedError
    
    
class OrchestratorEvent(TrawlNet.OrchestratorEvent):
    ''' '''
    orchestrator = None
    def hello(self, current = None, new_orchestrator = None):
        self.orchestrator.orchestrator_list.append(new_orchestrator.proxy)
 
 
class UpdateEvent(TrawlNet.UpdateEvent):
    def newFile(self, file_info):
        print(f'HA VENIDO {str(file_info)}')
 
    
class Orchestrator():
    ''' Implementacion del objeto orquestador '''
    def __init__(self):
        self.proxy = None
        self.orchestrator_list = []
        
        
class Server(Ice.Application):
    '''Código del servidor servidor'''
    def get_topic_manager(self):
        key = 'IceStorm.TopicManager.Proxy'
        proxy = self.communicator().propertyToProxy(key)
        if proxy is None:
            print("property {} not set".format(key))
            return None

        print("Using IceStorm in: '%s'" % key)
        return IceStorm.TopicManagerPrx.checkedCast(proxy)

    def run(self, args):
        # if len(args) < 2:
        #     print('ERROR: No se han introducido el numero de argumentos valido.')
        #     return 1
        
        # ---------------- Creacion del downloader --------------------
        downProxy = args[1]
        proxyDown = self.communicator().stringToProxy(downProxy)
        downloader = TrawlNet.DownloaderPrx.checkedCast(proxyDown)
        
        # ---------------- Creacion de objetos --------------------
        broker = self.communicator()
        orquestrator_object = Orchestrator() #Creamos el objeto para SOLO contener la informacion de los orqu
        servant = OrchestratorI() #Creamos el servant
        hello_servant = OrchestratorEvent() #Servant del canal OrquestratorSync
        servant.downloader=downloader
        hello_servant.orchestrator = orquestrator_object #Lo metemos para cuando llegue un hollo, actualizar el orq
        
        # ------------------- proxys -------------------
        adapter = broker.createObjectAdapter("OrchestratorAdapter")
        proxy = adapter.addWithUUID(servant)
        orquestrator_object.proxy = proxy
        
        # ------------------- Subscripciones -------------------
        topic_manager = self.get_topic_manager()
        if not topic_manager:
            print('Invalid proxy')
            return 2
        topic_name = 'OrchestratorSync'
        qos = {} # Que coño es esto
        try:
            topic = topic_manager.retrieve(topic_name)
        except IceStorm.NoSuchTopic:
            print("No se ha encontrado ese tonico")
            topic = topic_manager.create(topic_name)
        topic.subscribeAndGetPublisher(qos, proxy)
                
        # ---------------- Publicaciones ----------------------
        publisher = topic.getPublisher()
        hello_publish = None #hasta aqui hemos llegao
        
        # -----------------------------------------------
        print(proxy, flush=True)
        
        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        topic.unsubscribe(proxy)

        return 0


def readProxy():
    with open('./proxy.out', 'r') as f:
        return f.readline() 


if __name__ == "__main__":
    server = Server()
    sys.exit(server.main(sys.argv))


