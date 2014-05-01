#!/usr/bin/env python3
# encoding: utf-8


import settings
from Select import Selector
from Subject import Subject
from time import sleep
from FTP import FTP
try:
    import threading as _threading
except ImportError:
    import dummy_threading as _threading


class Listener(Subject, _threading.Thread):
    def __init__(self, ftp, match, fileListDir=settings.FTP_FileList_Dir):
        if not isinstance(ftp, FTP):
            raise TypeError

        #super(Listener, self).__init__()
        Subject.__init__(self)
        _threading.Thread.__init__(self)

        self._ftpFileListDir = fileListDir
        self._localFileList = []
        self._ftp = ftp
        self.__SetSelector(match)

    def __SetSelector(self, match):
        self._selector = Selector(match)

    def __GetList(self):
        return self._selector.Findall(self._ftp.GetList(self._ftpFileListDir))

    def Listen(self, time=5*60):
        while True:
            ftpFileList = self.__GetList()
            if ftpFileList != self._localFileList:
                self._localFileList = ftpFileList
                super(Listener, self).Notify(self._localFileList)
                break
            else:
                sleep(time)

    def run(self):
        self.Listen()

    @property
    def FtpFileListDir(self):
        return self._ftpFileListDir

    @FtpFileListDir.setter
    def FtpFileListDir(self, value):
        self._ftpFileListDir = value

    #@property
    #def FTP(self):
    #    return self._ftp

    #@FTP.setter
    #def FTP(self, value):
    #    if not isinstance(value, FTP):
    #        raise TypeError

    #    self._ftp = value

    @property
    def Selector(self):
        return self._selector

    @Selector.setter
    def Selector(self, value):
        self._selector = Selector(value)
