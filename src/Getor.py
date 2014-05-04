#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function
from Observer import Observer
import settings
from FTP import FTP
from Select import Selector
#import os


class Getor(Observer):
    def __init__(self, ftp, match, remoteDir, localDir=settings.Download_Dir):
        if not isinstance(ftp, FTP):
            raise TypeError

        super(Getor, self).__init__()

        self._ftp = ftp
        self._localDir = localDir
        self._remoteDir = remoteDir
        self._selector = Selector(r"^ *(\d*) ({filename})$".format(filename=match))

    def _Download(self, filename, size):
        flag = 0
        print("[Fileinfo]: {filename} {filesize}".format(filename=filename, filesize=size))
        while flag != 2:
            flag = self._ftp.GetFile(filename, size, self._localDir, self._remoteDir)

        return flag

    def Update(self, info):
        try:
            for size, filename in self._selector.Findall(info):
                self._Download(filename.strip(), int(size))
                #print(filename, size)
        except:
            print("[Error]: has some error in Getor.")
            self._KillSelf() # 自杀( 其实只是逃离工作而已

    #@property
    #def FTP(self):
    #    return self._ftp

    #@FTP.setter
    #def FTP(self, value):
    #    if not isinstance(value, FTP):
    #        raise TypeError

    #    self._ftp = value

    @property
    def DownloadDir(self):
        return self._localDir

    @DownloadDir.setter
    def DownloadDir(self, value):
        self._localDir = value

    @property
    def FTPDir(self):
        return self._remoteDir

    @FTPDir.setter
    def FTPDir(self, value):
        self._remoteDir = value
