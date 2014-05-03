#!/usr/bin/env python
#encoding: utf-8

from __future__ import print_function
import os
#import settings
#from time import sleep
#from Listen import Listener
from FTP import FTPFactory
#from Getor import Getor
from Downloader import Downloader
try:
    import threading as _threading
except ImportError:
    import dummy_threading as _threading

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

def main(filenameList):
    lock = _threading.Lock()  # 获取线程锁，预防多个listener竞争lftp的使用
    ftp = FTPFactory().GetFTP()
    downloader = Downloader(ftp, lock, *filenameList)

    downloader.Run()

if __name__ == '__main__':
    filename = input("AnimeName: ")
    main(list(filename))
