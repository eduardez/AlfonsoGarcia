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
        orchestrator = TrawlNet.OrchestratorPrx.checkedCast(proxy)

        if not orchestrator:
            raise RuntimeError('Invalid proxy')

        print(str(argv[2]))
        file_info = orchestrator.downloadTask(argv[2])
        print(f'[Titulo: {str(file_info.name)} \nHash: {str(file_info.hash)}]')
        return 0


sys.exit(Client().main(sys.argv))
