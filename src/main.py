#!/usr/bin/env python3
#encoding: utf-8

import os
import settings
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

def Clear(*args):
    # 清理文件
    for aFile in args:
        try:
            os.remove(aFile)
        except IOError:
            print("No such file {}".format(aFile))
        except NotImplementedError:
            print("Your platform not support remove.")
            return -1

def main(animeName, num=0, TV=''):
    ck = CK_BaS(animeName, num, TV, match=r' *(\d*) (Blade_and_Soul_05\.ts).*?')

    ftp = FTPFactory().GetFTP()
    getor = Getor(ftp)
    listener = Listener(ftp, ck.Match)

    ck.Binding([listener], getor)
    ck.Start([listener], getor)
