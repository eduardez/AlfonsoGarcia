#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import Ice
import binascii
Ice.loadSlice('trawlnet.ice')
import TrawlNet


APP_DIRECTORY = './'
DOWNLOADS_DIRECTORY = os.path.join(APP_DIRECTORY, 'downloads')


class Client(Ice.Application):
    '''
    Clase cliente
    '''
    def run(self, argv):
        proxy = self.communicator().stringToProxy('orchestrator')
        orchestrator = TrawlNet.OrchestratorPrx.checkedCast(proxy)
        if not orchestrator:
            raise RuntimeError('Invalid proxy')
        print('Enviando peticion a \n' + str(orchestrator))

        if len(argv) > 2 and len(argv) < 4:
            if argv[1] == '--download':
                print('Descargando: %s' % str(argv[2]))
                file_info = orchestrator.downloadTask(argv[2])
                print(f'[Titulo: {str(file_info.name)} \nHash: {str(file_info.hash)}]')
                return 0

            elif argv[1] == '--transfer':
                print('Obteniendo: %s' % str(argv[2]))
                file_name = self.checkExtension(argv[2])
                self.transfer_request(file_name, orchestrator)

            else:
                print('****Opcion no reconocido.\nSaliendo...')
        elif len(argv) == 1:
            print('Peticion de lista de archivos mandada...')
            file = orchestrator.getFileList()
            print(file)
            return 0
        else:
            print('****ERROR EN LOS ARGUMENTOS.\nSaliendo...')

    def checkExtension(self, file_name):
        '''
        Comprueba si el nombre de la cancion introducido
        para la transferencia contiene la extension .mp3 .
        Si no la tiene, se la pone
        '''
        if file_name.endswith('.mp3'):
            return file_name
        else:
            return file_name + '.mp3'

    def createDownloadsDir(self):
        '''
        Comprueba que exista un directorio para almacenar
        las descargas del cliente.
        '''
        if not os.path.exists(DOWNLOADS_DIRECTORY):
            os.makedirs(DOWNLOADS_DIRECTORY)

    def transfer_request(self, file_name, orchestrator):
        remote_EOF = False
        BLOCK_SIZE = 1024
        transfer = None
        self.createDownloadsDir()

        try:
            transfer = orchestrator.getFile(file_name)
        except TrawlNet.TransferError as e:
            print(e.reason)
            return 1

        with open(os.path.join(DOWNLOADS_DIRECTORY, file_name), 'wb+') as file_:
            remote_EOF = False
            while not remote_EOF:
                data = transfer.recv(BLOCK_SIZE)
                if len(data) > 1:
                    data = data[1:]
                data = binascii.a2b_base64(data)
                remote_EOF = len(data) < BLOCK_SIZE
                if data:
                    file_.write(data)
            transfer.close()
        transfer.destroy()
        print('Transfer finished!')


sys.exit(Client().main(sys.argv))
