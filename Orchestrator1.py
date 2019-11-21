#!/usr/bin/python3
# -*- coding: utf-8 -*-

#en el archivo config poner IceConfig.IPvVersion = 4 para librarnos de las ipv 6

import sys
import Ice
Ice.loadSlice('TrawlNet.ice')
import TrawlNet 


class OrchestratorI(TrawlNet.Orchestrator):
    ''' Sirviente del Orchestrator '''
    downloader = None
    
    def downloadTask (self, url, current=None):
        print('Peticion de descarga, url: %s' % url)
        if self.downloader is not None:
            return self.downloader.addDownloadTask(url)


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
        servant.downloader=downloader
        
        adapter = broker.createObjectAdapter("OrchestratorAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("orchestrator"))
        print(proxy, flush=True)
        
        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

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


