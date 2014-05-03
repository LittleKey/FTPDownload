#!/usr/bin/env python3
#encoding: utf-8

import os
#import settings
#from time import sleep
from Listen import Listener
from FTP import FTPFactory
from Getor import Getor


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

def main(filename):
    ftp = FTPFactory().GetFTP()
    getor = Getor(ftp, filename)
    listener = Listener(ftp)

    listener.Attach(getor)

    listener.start()
    listener.join()

if __name__ == '__main__':
    filename = input("AnimeName: ")
    main(filename)
