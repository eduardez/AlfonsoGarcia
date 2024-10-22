#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import utils as utiles
import Ice
import IceStorm
Ice.loadSlice('trawlnet.ice')
import TrawlNet


class OrchestratorI(TrawlNet.Orchestrator):
    ''' Sirviente del Orchestrator '''
    orchestrator_list = {}
    publisher_update_proxy = None
    downloader_factory = None
    transfer_factory = None
    proxy = None
    name = None

    def downloadTask(self, url, current):
        print('\n[Orchestrator]Peticion de descarga, url: %s' % url)
        hash = ''
        name = ''
        from youtube_dl import YoutubeDL
        with YoutubeDL({'quiet': True}) as youtube:
            info = youtube.extract_info(url, download=False)
            hash = info.get("id", None)
            name = info.get("title", None)
        if utiles.isInList(hash):
            file_info = TrawlNet.FileInfo()
            file_info.name = name
            file_info.hash = hash
            print('\n[Orchestrator] ERROR*** Cancion ya descargada.')
            return file_info
        else:
            downloader = self.downloader_factory.create()  # Crear el downloader
            if downloader is not None:
                print(f'\nDescargando cancion.\nDownloader: {downloader}')
                file_info = downloader.addDownloadTask(url)
                self.addToList(file_info=file_info)
                downloader.destroy()
                return file_info
            else:
                print('***ERROR. No se ha encontrado ningun downloader')

    def getFileList(self, current=None):
        print("\n[Orchestrator]Peticion de informacion de archivos disponibles")
        list_file = []
        archivo = utiles.jsonRead()
        if not archivo:
            return archivo
        for k, v in archivo.items():
            file_info = TrawlNet.FileInfo()
            file_info.name = v
            file_info.hash = k
            list_file.append(file_info)
        return list_file

    def getFile(self, file_name, current=None):
        print(f'\n[Orchestrator]Peticion de transferencia. Archivo: {file_name}')
        transfer = None
        try:
            transfer = self.transfer_factory.create(file_name)
        except Ice.UnknownException:
            print('\n[Orchestrator]Este orchestrator no tiene ese archivo. Probando con otro...\n')
        finally:
            return transfer

    def addToList(self, file_info, current=None):
        json = utiles.addToList(file_info.name, file_info.hash)
        utiles.jsonWrite(json)

    def announce(self, other_orchestrator, current=None):
        print('\n[Orchestrator]Anuncio de ' + str(other_orchestrator))
        self.orchestrator_list[other_orchestrator.ice_toString()] = other_orchestrator
        print(f'\n[Orchestrator] Lista de orchestrators actualizada: \n{str(self.orchestrator_list.keys())}')

    def updateFiles(self, current=None):
        for file in self.getFileList():
            self.publisher_update_proxy.newFile(file)


class OrchestratorEvent(TrawlNet.OrchestratorEvent):
    '''
    Servant del OrchestratorEvent.
    Comunica que un nuevo Orchestrator ha sido creado.
    '''
    orchestrator = None

    def hello(self, new_orchestrator, current=None):
        print('\n[OrchestratorEvent]--> Hello from ' + str(new_orchestrator))
        self.orchestrator.orchestrator_list[new_orchestrator.ice_toString()] = new_orchestrator
        new_orchestrator.announce(TrawlNet.OrchestratorPrx.checkedCast(self.orchestrator.proxy))
        self.orchestrator.updateFiles()


class UpdateEvent(TrawlNet.UpdateEvent):
    '''
    Servant del UpdateEvent.
    Comunica que un nuevo archivo ha sido descargado.
    '''
    orchestrator = None

    def newFile(self, file_info, current=None):
        if not utiles.isInList(file_info.hash):
            print(f'NO ESTA {str(file_info.name)}')
            self.orchestrator.addToList(file_info)
        else:
            print(f'Ya en lista {str(file_info.name)}')


class Server(Ice.Application):
    '''
    Clase para mantener un servidor para el orchestrator
    '''

    def get_topic_manager(self):
        key = 'YoutubeDownloaderApp.IceStorm/TopicManager'
        proxy = self.communicator().stringToProxy(key)
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
        # ---------------- Creacion del downloader factory -------------------
        down_factory_proxy = 'DownloaderFactory'
        proxy_downloader_factory = self.communicator().stringToProxy(down_factory_proxy)
        downloader_factory = TrawlNet.DownloaderFactoryPrx.checkedCast(proxy_downloader_factory)

        # ---------------- Creacion del transfer factory --------------------
        transfer_factory_proxy = 'TransferFactory'
        proxy_transfer_factory = self.communicator().stringToProxy(transfer_factory_proxy)
        transfer_factory = TrawlNet.TransferFactoryPrx.checkedCast(proxy_transfer_factory)

        # ---------------- Creacion de objetos --------------------
        broker = self.communicator()
        properties = broker.getProperties()
        orchestrator_servant = OrchestratorI()
        hello_servant = OrchestratorEvent()
        update_servant = UpdateEvent()

        orchestrator_servant.downloader_factory = downloader_factory
        orchestrator_servant.transfer_factory = transfer_factory
        hello_servant.orchestrator = orchestrator_servant
        update_servant.orchestrator = orchestrator_servant

        # ---------------------- proxys ----------------------
        adapter = broker.createObjectAdapter("OrchestratorAdapter")
        id_orch = properties.getProperty('Identity')
        proxy = adapter.add(orchestrator_servant, broker.stringToIdentity(id_orch))
        proxy_hello = adapter.addWithUUID(hello_servant)
        proxy_update = adapter.addWithUUID(update_servant)
        orchestrator_servant.proxy = proxy

        # ------------------- Subscripciones ------------------
        topic_hello = self.get_topic('OrchestratorSync')
        topic_hello.subscribeAndGetPublisher({}, proxy_hello)

        topic_update = self.get_topic('UpdateEvents')
        topic_update.subscribeAndGetPublisher({}, proxy_update)

        # ------------------- Publicaciones --------------------
        # Mensajes hello
        publisher_hello = topic_hello.getPublisher()
        publisher_hello_proxy = TrawlNet.OrchestratorEventPrx.uncheckedCast(publisher_hello)

        # Mensajes update
        publisher_update = topic_update.getPublisher()
        publisher_update_proxy = TrawlNet.UpdateEventPrx.uncheckedCast(publisher_update)
        orchestrator_servant.publisher_update_proxy = publisher_update_proxy

        # -------------- Acciones sobre los proxys --------------
        publisher_hello_proxy.hello(TrawlNet.OrchestratorPrx.checkedCast(proxy))
        for file in orchestrator_servant.getFileList():
            publisher_update_proxy.newFile(file)

        # -----------------------------------------------
        print(proxy, flush=True)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        topic_hello.unsubscribe(proxy_hello)
        topic_update.unsubscribe(proxy_update)

        return 0


if __name__ == "__main__":
    server = Server()
    sys.exit(server.main(sys.argv))
