#!/usr/bin/env python3
#encoding: utf-8

import os
#import settings
from StringMerge import StringMerge
#from time import sleep
from Listen import Listener
from FTP import FTPFactory
from Getor import Getor


class CK_BaS:
    def __init__(self, animeName, num=0, TV='', match=''):
        self._match = match
        self.animeInfo = {
                'name': animeName,
                'num': int(num),
                'TV': TV
            }

    @property
    def Match(self):
        return self._match

    def Binding(self, listenerList, getor):
        for listener in listenerList:
            listener.Selector = self._match
            listener.Attach(getor)
            listener.start()

    def DeBinding(self, listener, getor):
        listener.Detach(getor)

    def _Filter(self, tsList):
# 过滤器
        if tsList and self.animeInfo['TV']:
            tsList = list(filter(lambda t: t[2].upper() == self.animeInfo['TV'], tsList))

        if tsList and self.animeInfo['num']:
            tsList = list(filter(lambda t: int(t[1]) >= self.animeInfo['num'], tsList))

        if tsList:
            size, num, TV = sorted(tsList, key=lambda t: t[1])[-1]

            filename =  StringMerge( \
                    head=self.animeInfo['name'], \
                    foot='.ts', \
                    middleWare='_', \
                    stringList=[num, TV]\
                ).Return()

            print(r"{} size: {}".format(filename, size))

            return filename, size
        else:
            return False

    def Start(self, listenerList, getor):
        for aThread in listenerList:
            aThread.join()
            self.DeBinding(aThread, getor)

def Clear(*args):
    # 清理文件
    for aFile in args:
        try:
            os.remove(aFile)
        except FileNotFoundError:
            print("No such file {}".format(aFile))
        except NotImplementedError:
            print("Your platform not support remove.")
            return -1

def main(animeName, num=0, TV=''):
    ck = CK_BaS(animeName, num, TV, match='group *?(\d.*) \w+\w+\w+.*? {}_?(\d*)_?(.*?)\.ts'.format(animeName))

    ftp = FTPFactory().GetFTP()
    getor = Getor(ftp, ck._Filter)
    listener = Listener(ftp, ck.Match)

    ck.Binding([listener], getor)
    ck.Start([listener], getor)
