#!/usr/bin/env python3
# encoding: utf-8

from Observer import Observer
import settings
from FTP import FTP
#import os


class Getor(Observer):
    def __init__(self, ftp, fileFilter, localDir=settings.Download_Dir, remoteDir=settings.FTP_FileList_Dir):
        if not isinstance(ftp, FTP):
            raise TypeError

        super(Getor, self).__init__()

        self._ftp = ftp
        self._localDir = localDir
        self._remoteDir = remoteDir
        self._filter = fileFilter

    def Download(self, filename, size):
        flag = 0
        while flag != 2:
            flag = self._ftp.GetFile(filename, size, self._localDir, self._remoteDir)
        
        return flag

    def Update(self, info):
        info = self._filter(info)
        if isinstance(info, (tuple, list)) and len(info) == 2:
            filename, size = info
            self.Download(filename, size)

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
