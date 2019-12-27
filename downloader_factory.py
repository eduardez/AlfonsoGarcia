#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice, IceStorm
import os
Ice.loadSlice('trawlnet.ice')
import TrawlNet

APP_DIRECTORY = './'
DOWNLOADS_DIRECTORY = os.path.join(APP_DIRECTORY, 'downloads')

# --------------- REGION DE ESCUCHA DE DOWNLOADER  (ZeroC) ---------------


class DownloaderI(TrawlNet.Downloader):
    ''' Sirviente del Downloader '''
    iceApplication = None
    publisher_update_proxy = None
    
    def addDownloadTask(self, url, current):
        download_mp3(url)
        file_info = self.createFileInfo(url)
        self.updateEvent(file_info)
        return file_info
    
    def createFileInfo(self, url):
        file_info = TrawlNet.FileInfo()
        file_info.name = ''
        file_info.hash = ''
        try:
            from youtube_dl import YoutubeDL
            with YoutubeDL() as youtube:
                info = youtube.extract_info(url, download=False)
                file_info.hash = info.get("id", None)
                file_info.name = info.get('title', None)
            return file_info
        except Exception:
            print('ERROR: Hubo un error creando el objeto FileInfo.')
            sys.exit(1) 
    
    def updateEvent(self, file_info):
        self.publisher_update_proxy.newFile(file_info)
    
    def destroy(self, current):
        try:
            current.adapter.remove(current.id)
            print('DOWNLOADER DESTROYED', flush=True)
        except Exception as e:
            print(e, flush=True)

        
class DownloaderFactoryI(TrawlNet.DownloaderFactory):
    publisher_update_proxy = None
    
    def create(self, current):
        servant = DownloaderI()
        servant.publisher_update_proxy = self.publisher_update_proxy
        proxy = current.adapter.addWithUUID(servant)
        print('# New downloader created.', flush=True)

        return TrawlNet.DownloaderPrx.checkedCast(proxy)


class Server(Ice.Application):
    '''Código del servidor de descargas
    El downloader es publicador'''
    def get_topic_manager(self):
        key = 'IceStorm.TopicManager.Proxy'
        proxy = self.communicator().propertyToProxy(key)
        if proxy is None:
            return None
        return IceStorm.TopicManagerPrx.checkedCast(proxy)
    
    def get_topic(self, topic_name):
        topic_manager = self.get_topic_manager()
        topic = None
        if not topic_manager:
            return 2
        try:
            topic = topic_manager.retrieve(topic_name)
        except IceStorm.NoSuchTopic:
            topic = topic_manager.create(topic_name)
        return topic
    
    def run(self, args):
        # if len(args) < 2:
        #     print('ERROR: No se han introducido el numero de argumentos valido.')
        #     return 1
        broker = self.communicator()
        servant_downloader_factory = DownloaderFactoryI()
        servant_downloader_factory.iceApplication = self
        adapter = broker.createObjectAdapter("DownloaderAdapter")
        proxy = adapter.addWithUUID(servant_downloader_factory)

        topic_update = self.get_topic('UpdateEvents')
        publisher_update = topic_update.getPublisher()
        publisher_update_proxy = TrawlNet.UpdateEventPrx.uncheckedCast(publisher_update)
        servant_downloader_factory.publisher_update_proxy = publisher_update_proxy

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
    server = Server()
    sys.exit(server.main(sys.argv))
