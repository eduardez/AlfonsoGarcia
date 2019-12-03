#!/usr/bin/python3
# -*- coding: utf-8 -*-

#en el archivo config poner IceConfig.IPvVersion = 4 para librarnos de las ipv 6

import sys
import Ice, IceStorm
Ice.loadSlice('TrawlNet.ice')
import TrawlNet 
import HieloStorm


class OrchestratorI(TrawlNet.Orchestrator):
    ''' Sirviente del Orchestrator '''
    downloader = None
    
    def downloadTask (self, url, current=None):
        print('Peticion de descarga, url: %s' % url)
        hash = ''
        file_list=self.getFileList()
        from youtube_dl import YoutubeDL
        with YoutubeDL() as youtube:
            info = youtube.extract_info(url, download=False)
            hash = info.get("id", None)
        if hash in file_list:
            #Acceder al orchestrator correcto y devolver el fichero
            print("Ese fichero ya esta descargado")
            pass
        else:
            if self.downloader is not None:
                file_info = self.downloader.addDownloadTask(url)
                with open('./file_list.txt', 'a+') as f:
                    #En el write tambien hay que añadir el orchestator para saber quien tiene el archivo
                    f.write(file_info.hash + '\n')
                return file_info
            
    
    def getFileList(self, current=None):
        list_file = []
        archivo = None
        with open('./file_list.txt', 'r') as f:
            archivo = f.readlines()
        for x in range(0, len(archivo), 2):
            file_info = TrawlNet.FileInfo()
            file_info.hash = archivo[x]
            file_info.name = archivo[x+1]
            list_file.append(file_info)

        print("Peticion de informacion de archivos disponibles")
        return list_file
    
    def announce(self, other_orchestrator):
        raise NotImplementedError
    
    
class OrchestratorEvent(TrawlNet.OrchestratorEvent):
    ''' '''
    def hello(self):
        raise NotImplementedError
 
 
class UpdateEvent(TrawlNet.UpdateEvent):
    def newFile(self, file_info):
        print(f'HA VENIDO {str(file_info)}')
 
    
class Orchestrator():
    ''' Implementacion del orquestador PRINCIPAL 
    (el que va a tener la lista de todos los orquestadores) 
    El orchestrator es subscriptor'''
    def __init__(self):
        self.broker = None
        self.servant = None
        self.orchestrator_list = []
        self.downloader = None
        


class Server(Ice.Application):
    '''Código del servidor servidor'''

    def run(self, args):
        # if len(args) < 2:
        #     print('ERROR: No se han introducido el numero de argumentos valido.')
        #     return 1
        
        # Crear downloader -----
        downProxy = readProxy()
        proxyDown = self.communicator().stringToProxy(downProxy)
        downloader = TrawlNet.DownloaderPrx.checkedCast(proxyDown)
        
        # -----------------------------------------------
        broker = self.communicator()
        servant = OrchestratorI()
        servant2 = UpdateEvent()
        servant.downloader=downloader
        
        adapter = broker.createObjectAdapter("OrchestratorAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("orchestrator"))
        # subscriber2 = adapter.addWithUUID(servant2)
        # topic_manager = HieloStorm.getTopicManager(self)
        # topic = HieloStorm.getTopic('UpdateEvents', topic_manager)
        # topic.subscribeAndGetPublisher({}, subscriber)

        print(proxy, flush=True)
        
        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        # topic.unsubscribe(subscriber)

        return 0


def readProxy():
    with open('./proxy.out', 'r') as f:
        return f.readline() 


if __name__ == "__main__":
    print('''
--------------------------------          
        Orquestador
--------------------------------    
    ''' )
    server = Server()
    sys.exit(server.main(sys.argv))


