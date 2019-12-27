#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('trawlnet.ice')
import TrawlNet 

class Client(Ice.Application):
    '''Clase cliente'''
    def run(self, argv):
        # proxy = self.communicator().stringToProxy(argv[1])
        # print(argv[1])
        # orchestrator = TrawlNet.OrchestratorPrx.uncheckedCast(proxy)

        # if not orchestrator:
        #     raise RuntimeError('Invalid proxy')

        if len(argv) > 2 and len(argv) < 4:
            if argv[1] == '--download':
                print('Descargando: %s'% str(argv[2]))
                file_info = orchestrator.downloadTask(argv[2])
                print(f'[Titulo: {str(file_info.name)} \nHash: {str(file_info.hash)}]')
                return 0
            elif argv[1] == '--transfer':
                pass
            else:
                print('****Opcion no reconocido.\nSaliendo...')
        elif len(argv) == 1:
            print('Peticion de lista de archivos mandada...')
            file = orchestrator.getFileList()
            print(file)
            return 0
        else:
            print('****ERROR EN LOS ARGUMENTOS.\nSaliendo...')
        

sys.exit(Client().main(sys.argv))
