#!/usr/bin/python3
# -*- coding: utf-8 -*-

#en el archivo config poner IceConfig.IPvVersion = 4 para librarnos de las ipv 6

import sys, utiles
from pathlib import Path as path
import Ice, IceStorm
Ice.loadSlice('TrawlNet.ice')
import TrawlNet 


class OrchestratorI(TrawlNet.Orchestrator):
    ''' Sirviente del Orchestrator '''
    downloader = None
    orchestrator_list = {}
    publisher_update_proxy = None
    
    def downloadTask (self, url, current=None):
        print('Peticion de descarga, url: %s' % url)
        hash = ''
        name = ''
        from youtube_dl import YoutubeDL
        with YoutubeDL() as youtube:
            info = youtube.extract_info(url, download=False)
            hash = info.get("id", None)
            name = info.get("title", None)
        if utiles.isInList(hash):
            file_info = TrawlNet.FileInfo()
            file_info.name = name
            file_info.hash = hash
            print('ERROR*** Cancion ya descargada.')
            return file_info
        else:
            print('Descargando cancion.')
            if self.downloader is not None:
                file_info = self.downloader.addDownloadTask(url)
                self.addToList(file_info=file_info)
                return file_info

    def getFileList(self, current=None):
        print("Peticion de informacion de archivos disponibles")
        list_file = []
        archivo = utiles.jsonRead()
        if not archivo:
            return archivo
        for cancion in archivo['canciones']:
            file_info = TrawlNet.FileInfo()
            file_info.name = cancion['name']
            file_info.hash = cancion['hash']
            list_file.append(file_info)
        return list_file
        
    def addToList(self, file_info, current = None):
        json = utiles.addToList(file_info.name, file_info.hash)
        utiles.jsonWrite(json)

    def announce(self, other_orchestrator, current = None ):
        print('\n[Orchestrator]--> Anuncio de ' + str(other_orchestrator))
        self.orchestrator_list[other_orchestrator.ice_toString()] = other_orchestrator
        print(f'Lista de orchestrators actualizada: {len(self.orchestrator_list)} orchestrators \n{str(self.orchestrator_list.keys())}')

    def updateFiles(self, current = None):
        for file in self.getFileList():
            self.publisher_update_proxy.newFile(file)


class OrchestratorEvent(TrawlNet.OrchestratorEvent):
    ''' '''
    orchestrator = None
    def hello(self, new_orchestrator, current = None):
        print('\n[OrchestratorEvent]--> Hello from ' + str(new_orchestrator))
        self.orchestrator.orchestrator_list[new_orchestrator.ice_toString()] = new_orchestrator#ice_toString() para devolver el proxy en str
        new_orchestrator.announce(TrawlNet.OrchestratorPrx.checkedCast(self.orchestrator.proxy))#llamo al announce del nuevo orchestrator para anunciarme
        self.orchestrator.updateFiles()


class UpdateEvent(TrawlNet.UpdateEvent):
    orchestrator = None
    def newFile(self, file_info, current = None):
        if not utiles.isInList(file_info.hash):
            print(f'NO ESTA {str(file_info.name)}')
            self.orchestrator.addToList(file_info)
        else:
            print(f'Ya en lista {str(file_info.name)}')

 
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

    def get_topic(self, topic_name):
        topic_manager = self.get_topic_manager()
        topic = None
        if not topic_manager:
            print('Invalid proxy')
            return 2
        try:
            topic = topic_manager.retrieve(topic_name)
        except IceStorm.NoSuchTopic:
            print("No se ha encontrado ese tonico")
            topic = topic_manager.create(topic_name)
        return topic
    
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
        ochestrator_servant = OrchestratorI() #Creamos el servant
        hello_servant = OrchestratorEvent() #Servant del canal OrquestratorSync
        update_servant = UpdateEvent()
        
        ochestrator_servant.downloader=downloader
        hello_servant.orchestrator = ochestrator_servant #Lo metemos para cuando llegue un hollo, actualizar el orq
        update_servant.orchestrator = ochestrator_servant
        
        # ------------------- proxys -------------------
        adapter = broker.createObjectAdapter("OrchestratorAdapter")
        proxy = adapter.addWithUUID(ochestrator_servant)
        proxyHello = adapter.addWithUUID(hello_servant)
        proxyUpdate = adapter.addWithUUID(update_servant)
        ochestrator_servant.proxy = proxy
        
        # ------------------- Subscripciones -------------------
        topic_hello = self.get_topic('OrchestratorSync')
        topic_hello.subscribeAndGetPublisher({}, proxyHello)
        
        topic_update = self.get_topic('UpdateEvents')
        topic_update.subscribeAndGetPublisher({}, proxyUpdate)
                
        # ---------------- Publicaciones ----------------------
        # Mensajes hello
        publisher_hello = topic_hello.getPublisher()
        publisher_hello_proxy = TrawlNet.OrchestratorEventPrx.uncheckedCast(publisher_hello)
        
        # Mensajes update
        publisher_update = topic_update.getPublisher()
        publisher_update_proxy = TrawlNet.UpdateEventPrx.uncheckedCast(publisher_update)
        ochestrator_servant.publisher_update_proxy = publisher_update_proxy

                    
        # --------------- Acciones sobre los proxys ---------------------
        publisher_hello_proxy.hello(TrawlNet.OrchestratorPrx.checkedCast(proxy))
        for file in ochestrator_servant.getFileList():
            publisher_update_proxy.newFile(file)

        # -----------------------------------------------
        print(proxy, flush=True)
        
        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        topic_hello.unsubscribe(proxyHello)
        topic_update.unsubscribe(proxyUpdate)

        return 0


def readProxy():
    with open('./proxy.out', 'r') as f:
        return f.readline() 


if __name__ == "__main__":
    server = Server()
    sys.exit(server.main(sys.argv))


