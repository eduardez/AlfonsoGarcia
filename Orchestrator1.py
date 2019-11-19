#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('TrawlNet.ice')
import TrawlNet 


class OrchestratorI(TrawlNet.Orchestrator):
    ''' Sirviente del Orchestrator '''
    downloader = None
    def downloaderTask (self, url, current=None):
        print('Forward request to download %s' % url)
        if self.downloader is not None:
            return self.downloader.addDownloadTask(url)


class Server(Ice.Application):
    '''Código del servidor servidor'''
    def run(self, args):
        if len(args) < 2:
            print('ERROR: No se han introducido el numero de argumentos valido.')
            return 1
        broker = self.communicator()

        #Connect with downloader
        downloader_proxy = broker.stringToProxy(args[1])
        downloader = TrawlNet.DownloaderPrx.checkedCast(downloader_proxy)
        if not downloader:
            raise ValueError('Invalid proxy: %s' % repr(args[1]))

        adapter = broker.createObjectAdapter('OrchestratorAdapter')
        servant = OrchestratorI()
        servant.downloader = downloader
        proxy = adapter.addWithUUID(servant)
        print(proxy, flush=True)

        adapter.activate()

        #Wait until close
        self.shutdownOnInterrupt()
        server=Server()
        sys.exit(server.main(sys.argv))


if __name__ == "__main__":
    print('''
--------------------------------          
        Youtube to mp3
--------------------------------    
    ''' )
    argumentos = ['ProgramName', 'orchestrator -t -e 1.1:tcp -h localhost -p 9094 -t 60000']
    Server().main(argumentos)

