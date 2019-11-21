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
        orchestrator.downloadTask(argv[2])

        return 0


sys.exit(Client().main(sys.argv))
