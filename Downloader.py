#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
import os
Ice.loadSlice('TrawlNet.ice')
import TrawlNet 


# --------------- REGION DE ESCUCHA DE DOWNLOADER  (ZeroC) ---------------


class DownloaderI(TrawlNet.Downloader):
    ''' Sirviente del Downloader '''
    def addDownloadTask (self, url, current=None):
        download_mp3(url)


class Server(Ice.Application):
    '''Código del servidor de descargas'''
    def run(self, args):
        # if len(args) < 2:
        #     print('ERROR: No se han introducido el numero de argumentos valido.')
        #     return 1
        broker = self.communicator()
        servant = DownloaderI()

        adapter = broker.createObjectAdapter("DownloaderAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("downloader"))

        print(proxy, flush=True)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        
        return 0
    


# --------------- REGION DE DESCARGAS DE YOUTUBE ---------------
try:
    import youtube_dl
except ImportError:
    print('ERROR: do you have installed youtube-dl library?')
    sys.exit(1)


class NullLogger:
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass

_YOUTUBEDL_OPTS_ = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': NullLogger()
}

def download_mp3(url, destination='./'):
    '''
    Synchronous download from YouTube
    '''
    options = {}
    task_status = {}
    def progress_hook(status):
        task_status.update(status)
    options.update(_YOUTUBEDL_OPTS_)
    options['progress_hooks'] = [progress_hook]
    options['outtmpl'] = os.path.join(destination, '%(title)s.%(ext)s')
    with youtube_dl.YoutubeDL(options) as youtube:
        youtube.download([url])
    filename = task_status['filename']
    # BUG: filename extension is wrong, it must be mp3
    filename = filename[:filename.rindex('.') + 1]
    return filename + options['postprocessors'][0]['preferredcodec']


if __name__ == "__main__":
#     print('''
# --------------------------------          
#         Downloader
# --------------------------------    
#     ''' )
    server = Server()
    sys.exit(server.main(sys.argv))
