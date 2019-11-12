#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('Interface.ice')
import TrawlNet

class Client(Ice.Application):
    def run(self, argv):
        base = self.communicator().stringToProxy(argv[1])
        orchestrator = TrawlNet.downloadTask(url)

        if not servidor:
            raise RuntimeError('Invalid proxy')


if __name__ == "__main__":
    print('''
--------------------------------          
        Youtube to mp3
--------------------------------    
    ''')


