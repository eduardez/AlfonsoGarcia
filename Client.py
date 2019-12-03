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

       
        if len(argv) == 3:
            print(str(argv[2]))
            file_info = orchestrator.downloadTask(argv[2])
            print(f'[Titulo: {str(file_info.name)} \nHash: {str(file_info.hash)}]')
            return 0
        elif len(argv) == 2:
            file = orchestrator.getFileList()
            print(file)
            return 0
            


sys.exit(Client().main(sys.argv))
