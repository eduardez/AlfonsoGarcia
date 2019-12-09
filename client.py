#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('TrawlNet.ice')
import TrawlNet 

class Client(Ice.Application):
    '''Clase cliente'''
    def run(self, argv):
        proxy = self.communicator().stringToProxy(argv[1])
        print(argv[1])
        orchestrator = TrawlNet.OrchestratorPrx.uncheckedCast(proxy)

        if not orchestrator:
            raise RuntimeError('Invalid proxy')
    
        url = argv[2]
        if not url == '':
            print(str(argv[2]))
            file_info = orchestrator.downloadTask(url)
            print(f'[Titulo: {str(file_info.name)} \nHash: {str(file_info.hash)}]')
            return 0
        else:
            file = orchestrator.getFileList()
            print(file)
            return 0


sys.exit(Client().main(sys.argv))